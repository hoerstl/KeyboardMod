import asyncio
from io import BytesIO

from PIL import ImageGrab
from websockets.asyncio.client import connect

import tailScaleServer


def capture_screenshot() -> bytes:
    """Capture the screen and return PNG bytes."""
    screenshot = ImageGrab.grab()

    img_io = BytesIO()
    screenshot.save(img_io, format="PNG")

    return img_io.getvalue()


async def stream_screenshots(websocket, fps=10):
    """Stream screenshots at the target frames per second."""
    interval = 1.0 / fps
    loop = asyncio.get_running_loop()
    next_frame = loop.time()

    while True:
        # Capture and encode off the event loop so receiving
        # messages can continue while the screenshot is prepared.
        screenshot = await asyncio.to_thread(capture_screenshot)

        size_bytes = len(screenshot)
        size_kb = size_bytes / 1024
        size_mb = size_bytes / (1024 * 1024)

        print(f"Screenshot size: {size_bytes:,} bytes ({size_kb:.2f} KB, {size_mb:.2f} MB)")

        # Send the PNG as a binary WebSocket message.
        await websocket.send(screenshot)

        # Schedule the next frame using a monotonic clock.
        next_frame += interval
        remaining = next_frame - loop.time()

        if remaining > 0:
            await asyncio.sleep(remaining)
        else:
            # We missed the deadline. Skip the missed frames
            # rather than sending screenshots in a burst.
            next_frame = loop.time()


async def main(computerName=None, fps=10):
    serverIP = tailScaleServer.getTailscaleIP(computerName)

    if serverIP is None:
        raise RuntimeError(
            f"Computer '{computerName}' was not found in Tailscale status."
        )

    serverURL = f"ws://{serverIP}:8765"

    print(f"Attempting connection to {serverURL}")

    async with connect(serverURL, max_size=None) as websocket:
        print(f"Connected to {serverURL}")
        print(f"Streaming screenshots at {fps} FPS.")

        async def receive():
            async for message in websocket:
                if isinstance(message, bytes):
                    # print(f"Received binary message: {len(message)} bytes")
                    pass
                else:
                    # print(f"Received text message: {message}")
                    pass

        await asyncio.gather(
            receive(),
            stream_screenshots(websocket, fps=fps),
        )


if __name__ == "__main__":
    asyncio.run(main("jester-junction", fps=10))
