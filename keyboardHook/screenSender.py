
import asyncio
import json
import random
from io import BytesIO

from PIL import ImageGrab
from websockets.asyncio.client import connect

import tailScaleServer
import remoteInput


# Reconnection settings
INITIAL_RETRY_DELAY = 1.0
MAX_RETRY_DELAY = 5.0
SCREENSHOT_SEND_TIMEOUT = 10.0

# Avoid flooding logs if screen capture repeatedly fails.
CAPTURE_ERROR_LOG_INTERVAL = 5.0


def log(message):
    print(f"[screenSender] {message}", flush=True)


def handle_keyboard_message(message: str):
    try:
        data = json.loads(message)

        if not isinstance(data, dict) or data.get("type") != "key":
            return

        action = data.get("action")
        vk = data.get("vk")

        if (
            action not in ("down", "up")
            or isinstance(vk, bool)
            or not isinstance(vk, int)
            or not 0 <= vk <= 255
        ):
            log(f"Invalid keyboard event: {data}")
            return

        log(f"Injecting key event: vk={vk}, action={action}")
        remoteInput.inject_key(vk, action)

    except json.JSONDecodeError as exc:
        log(f"Invalid JSON message: {exc}")

    except Exception as exc:
        # One malformed message or injection failure must not kill
        # the receiving task.
        log(f"Failed to handle keyboard message: {exc!r}")


def capture_screenshot() -> bytes:
    """Capture and encode a screenshot. Exceptions are handled by the caller."""
    screenshot = ImageGrab.grab()

    img_io = BytesIO()
    screenshot.save(img_io, format="PNG")

    return img_io.getvalue()


async def stream_screenshots(websocket, fps=4):
    """
    Stream screenshots without accumulating a backlog.

    Capture failures skip the current frame.
    Send failures propagate so the connection can be restarted.
    """
    if fps <= 0:
        raise ValueError("fps must be greater than zero")

    interval = 1.0 / fps
    loop = asyncio.get_running_loop()
    next_frame = loop.time()
    last_capture_error_log = 0.0

    while True:
        try:
            # Capture and encode off the event loop so incoming
            # keyboard messages can still be processed.
            screenshot = await asyncio.to_thread(capture_screenshot)

        except Exception as exc:
            now = loop.time()

            if now - last_capture_error_log >= CAPTURE_ERROR_LOG_INTERVAL:
                log(f"Screenshot capture failed; skipping frame: {exc!r}")
                last_capture_error_log = now

            # Skip this frame and continue trying.
            next_frame += interval
            now = loop.time()

            if next_frame <= now:
                next_frame = now + interval

            await asyncio.sleep(max(0, next_frame - now))
            continue

        try:
            # Bound send time so a stalled connection eventually
            # gets closed and retried.
            await asyncio.wait_for(
                websocket.send(screenshot),
                timeout=SCREENSHOT_SEND_TIMEOUT,
            )

            size_kb = len(screenshot) / 1024
            log(f"Screenshot sent: {size_kb:.2f} KB")

        except asyncio.CancelledError:
            raise

        except Exception as exc:
            # The connection manager will close and reconnect.
            raise ConnectionError(
                f"Screenshot transmission failed: {exc}"
            ) from exc

        # Maintain the target frame rate without catching up in bursts.
        next_frame += interval
        now = loop.time()

        if next_frame <= now:
            # Missed one or more deadlines; discard them.
            next_frame = now + interval

        await asyncio.sleep(max(0, next_frame - loop.time()))


async def receive_keyboard(websocket):
    """Receive and process keyboard messages."""
    async for message in websocket:
        if isinstance(message, bytes):
            # Ignore binary messages on this client.
            continue

        handle_keyboard_message(message)

    # A normally closed receive stream also requires reconnection.
    raise ConnectionError("WebSocket receive stream closed")


async def run_connection(server_url, fps):
    """Run both tasks for one connection; restart if either fails."""
    async with connect(
        server_url,
        max_size=None,
        open_timeout=10,
        ping_interval=20,
        ping_timeout=20,
    ) as websocket:
        log(f"Connected to {server_url}; streaming at {fps} FPS")

        tasks = {
            asyncio.create_task(
                receive_keyboard(websocket),
                name="receive-keyboard",
            ),
            asyncio.create_task(
                stream_screenshots(websocket, fps),
                name="stream-screenshots",
            ),
        }

        try:
            # Either task ending means this connection is no longer
            # healthy enough to keep running.
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in done:
                # Propagate errors to the reconnect loop.
                task.result()

            raise ConnectionError("A WebSocket task stopped unexpectedly")

        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)

    # Reaching here unexpectedly is treated as a connection failure.
    raise ConnectionError("WebSocket connection closed")


async def main(computerName=None, fps=4):
    """
    Retry indefinitely when discovery, connection, or streaming fails.
    """
    retry_delay = INITIAL_RETRY_DELAY

    while True:
        try:
            server_ip = await asyncio.to_thread(
                tailScaleServer.getTailscaleIP,
                computerName,
            )

            if server_ip is None:
                raise RuntimeError(
                    f"Computer '{computerName}' was not found in Tailscale status"
                )

            server_url = f"ws://{server_ip}:8765"
            log(f"Connecting to {server_url}")

            await run_connection(server_url, fps)

            # Normally run_connection never returns.
            retry_delay = INITIAL_RETRY_DELAY

        except asyncio.CancelledError:
            # Allow deliberate shutdown to work correctly.
            raise

        except Exception as exc:
            log(f"Connection/streaming error: {exc!r}")

        # Retry forever, increasing the delay up to MAX_RETRY_DELAY.
        # Jitter prevents repeated retries from syncing with other clients.
        delay = min(retry_delay, MAX_RETRY_DELAY)
        delay *= random.uniform(0.8, 1.2)

        log(f"Retrying in {delay:.1f} seconds")
        await asyncio.sleep(delay)

        retry_delay = min(
            retry_delay * 2,
            MAX_RETRY_DELAY,
        )


if __name__ == "__main__":
    try:
        asyncio.run(main("jester-junction", fps=4))
    except KeyboardInterrupt:
        log("Stopped by user")
