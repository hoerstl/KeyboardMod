
import asyncio
import threading
import time

from PySide6.QtCore import QThread, QTimer, Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from websockets.asyncio.client import connect

import tailScaleServer


PORT = 8765
REFRESH_INTERVAL_MS = 33  # Approximately 30 display updates per second
MAX_MESSAGE_SIZE = 10 * 1024 * 1024  # 10 MB


class WebSocketWorker(QThread):
    status_changed = Signal(str)

    def __init__(self, server_ip):
        super().__init__()

        self.server_url = f"ws://{server_ip}:{PORT}"

        # Only retain the most recent frame.
        self._frame_lock = threading.Lock()
        self._latest_frame = None
        self._new_frame = False

        self.frames_received = 0
        self.bytes_received = 0

        self._loop = None
        self._stop_event = None
        self._websocket = None

    def take_latest_frame(self):
        """Return the latest frame once, if a new one arrived."""
        with self._frame_lock:
            if not self._new_frame:
                return None

            frame = self._latest_frame
            self._new_frame = False
            return frame

    def run(self):
        asyncio.run(self._main())

    async def _main(self):
        self._loop = asyncio.get_running_loop()
        self._stop_event = asyncio.Event()

        try:
            self.status_changed.emit("Connecting...")

            async with connect(
                self.server_url,
                max_size=MAX_MESSAGE_SIZE,
                open_timeout=10,
            ) as websocket:
                self._websocket = websocket
                self.status_changed.emit("Connected")

                receiver = asyncio.create_task(
                    self._receive_frames(websocket)
                )
                stopper = asyncio.create_task(
                    self._stop_event.wait()
                )

                done, pending = await asyncio.wait(
                    [receiver, stopper],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in pending:
                    task.cancel()

                await asyncio.gather(
                    *pending, return_exceptions=True
                )

                # Surface receiver errors instead of silently hiding them.
                if receiver in done:
                    receiver.result()

        except Exception as exc:
            self.status_changed.emit(f"Disconnected: {exc}")

        finally:
            self._websocket = None
            self._loop = None
            self.status_changed.emit("Stopped")

    async def _receive_frames(self, websocket):
        async for message in websocket:
            if not isinstance(message, bytes):
                # Ignore text/control messages for now.
                continue

            with self._frame_lock:
                self._latest_frame = message
                self._new_frame = True

            self.frames_received += 1
            self.bytes_received += len(message)

    def stop(self):
        """Request a clean shutdown from the GUI thread."""
        if self._loop is not None and self._stop_event is not None:
            self._loop.call_soon_threadsafe(self._stop_event.set)

            if self._websocket is not None:
                self._loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(
                        self._websocket.close()
                    )
                    if self._websocket is not None
                    else None
                )


class ScreenshotViewer(QMainWindow):
    def __init__(self, server_ip):
        super().__init__()

        self.setWindowTitle("Remote Screenshot Viewer")
        self.resize(1280, 800)

        self.image_label = QLabel("Waiting for screenshots...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(320, 240)
        self.image_label.setStyleSheet(
            "QLabel { background-color: #181818; color: #cccccc; }"
        )

        self.status_label = QLabel("Starting...")
        self.stats_label = QLabel("Frames: 0 | Received: 0 MB")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label, stretch=1)
        layout.addWidget(self.status_label)
        layout.addWidget(self.stats_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.worker = WebSocketWorker(server_ip)
        self.worker.status_changed.connect(
            self.status_label.setText
        )

        self.worker.start()

        self._last_stats_time = time.monotonic()
        self._last_frames = 0
        self._last_bytes = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(REFRESH_INTERVAL_MS)

    def update_display(self):
        frame = self.worker.take_latest_frame()

        if frame is not None:
            image = QImage.fromData(frame, "PNG")

            if image.isNull():
                self.status_label.setText(
                    "Received an invalid PNG image"
                )
            else:
                pixmap = QPixmap.fromImage(image)
                scaled = pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.FastTransformation,
                )

                self.image_label.setPixmap(scaled)

                self.status_label.setText(
                    f"Connected | {image.width()} x {image.height()}"
                )

        now = time.monotonic()
        elapsed = now - self._last_stats_time

        if elapsed >= 1.0:
            frames = self.worker.frames_received
            total_bytes = self.worker.bytes_received

            fps = (frames - self._last_frames) / elapsed
            mbps = (
                (total_bytes - self._last_bytes) * 8
                / elapsed
                / 1_000_000
            )

            self.stats_label.setText(
                f"Incoming: {fps:.1f} FPS | "
                f"Bandwidth: {mbps:.2f} Mbps | "
                f"Total: {total_bytes / (1024 * 1024):.1f} MB"
            )

            self._last_frames = frames
            self._last_bytes = total_bytes
            self._last_stats_time = now

    def closeEvent(self, event):
        self.timer.stop()
        self.worker.stop()

        if not self.worker.wait(3000):
            self.status_label.setText(
                "Waiting for network worker to stop..."
            )
            self.worker.wait()

        event.accept()


def main(computer_name=None):
    server_ip = tailScaleServer.getTailscaleIP(computer_name)

    if server_ip is None:
        raise RuntimeError(
            f"Computer '{computer_name}' was not found in Tailscale status."
        )

    app = QApplication([])
    viewer = ScreenshotViewer(server_ip)
    viewer.show()

    app.exec()


if __name__ == "__main__":
    main("jester-junction")
