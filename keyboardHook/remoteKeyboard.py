import asyncio
import json
import threading
import tailScaleServer
from websockets.asyncio.client import connect


class RemoteKeyboardBridge:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.queue = asyncio.Queue()
        self.active = False

        # Protects state accessed by keyboard-hook callbacks.
        self._lock = threading.Lock()
        self._held_keys = set()

    def set_active(self, active: bool):
        """Call when your existing keyboard mode changes."""
        with self._lock:
            self.active = active

            # If leaving remote mode, release every key we forwarded.
            if not active:
                for vk in self._held_keys:
                    self._enqueue({"type": "key", "action": "up", "vk": vk})
                self._held_keys.clear()

    def _enqueue(self, message: dict):
        """Safe to call from a keyboard-hook thread."""
        self.loop.call_soon_threadsafe(
            self.queue.put_nowait,
            json.dumps(message),
        )

    def key_down(self, vk: int):
        """Forward a key-down event. vk is a Windows virtual-key code."""
        with self._lock:
            if not self.active:
                return

            # Avoid duplicate downs from the hook.
            if vk in self._held_keys:
                return

            self._held_keys.add(vk)
            self._enqueue({
                "type": "key",
                "action": "down",
                "vk": vk,
            })

    def key_up(self, vk: int):
        """Forward a key-up event, including after mode deactivation."""
        with self._lock:
            if vk not in self._held_keys:
                return

            self._held_keys.remove(vk)
            self._enqueue({
                "type": "key",
                "action": "up",
                "vk": vk,
            })

    async def send_loop(self, websocket):
        """Run as an asyncio task alongside your other connection tasks."""
        while True:
            message = await self.queue.get()
            try:
                await websocket.send(message)
            finally:
                self.queue.task_done()


class RemoteKeyboardSender:
    def __init__(self, computer_name, port=8765):
        self.computer_name = computer_name
        self.port = port
        self.websocket = None

        self.loop = None
        self.queue = None
        self.ready = threading.Event()
        self.error = None
        self.thread = threading.Thread(
            target=self._thread_main,
            daemon=True,
        )
        self._held_keys = set()
        self._key_lock = threading.Lock()

    def start(self):
        """Start the WebSocket connection in a background thread."""
        self.thread.start()

        if not self.ready.wait(timeout=15):
            raise RuntimeError(
                "Timed out connecting the remote keyboard sender."
            )

        if self.error is not None:
            raise RuntimeError(
                f"Could not start remote keyboard sender: {self.error}"
            )

        print("Remote keyboard sender connected.")

    def _thread_main(self):
        try:
            asyncio.run(self._run())
        except Exception as exc:
            self.error = exc
            self.ready.set()
            print(f"Remote keyboard connection error: {exc}")

    async def _run(self):
        server_ip = tailScaleServer.getTailscaleIP(self.computer_name)

        if server_ip is None:
            raise RuntimeError(
                f"Computer '{self.computer_name}' was not found in Tailscale status."
            )

        self.loop = asyncio.get_running_loop()
        self.queue = asyncio.Queue()
        server_url = f"ws://{server_ip}:{self.port}"

        async with connect(server_url, max_size=None) as websocket:
            self.websocket = websocket
            self.ready.set()

            print(f"Remote keyboard connected to {server_url}")

            send_task = asyncio.create_task(self._send_loop(websocket))
            receive_task = asyncio.create_task(self._receive_loop(websocket))

            try:
                await asyncio.wait(
                    [send_task, receive_task],
                    return_when=asyncio.FIRST_COMPLETED,
                )
            finally:
                for task in (send_task, receive_task):
                    task.cancel()

                await asyncio.gather(
                    send_task,
                    receive_task,
                    return_exceptions=True,
                )

                self.websocket = None

    def stop(self):
        if self.loop is None or self.websocket is None:
            return

        future = asyncio.run_coroutine_threadsafe(
            self.websocket.close(),
            self.loop,
        )

        future.result(timeout=5)
        self.thread.join(timeout=5)

    async def _send_loop(self, websocket):
        while True:
            message = await self.queue.get()
            try:
                await websocket.send(message)
            finally:
                self.queue.task_done()

    async def _receive_loop(self, websocket):
        # Drain messages from the relay connection. This connection
        # is used for sending keyboard events, not displaying images.
        async for _message in websocket:
            pass

    def send_key(self, vk, action):
        print(f"Sending key event: vk={vk}, action={action}")
        
        if action not in ("down", "up"):
            return

        if isinstance(vk, bool) or not isinstance(vk, int) or not 0 <= vk <= 255:
            return

        with self._key_lock:
            if action == "down":
                self._held_keys.add(vk)
            else:
                self._held_keys.discard(vk)

            if self.loop is None or self.queue is None:
                return

            message = json.dumps({
                "type": "key",
                "action": action,
                "vk": vk,
            })

            self.loop.call_soon_threadsafe(
                self.queue.put_nowait,
                message,
            )


