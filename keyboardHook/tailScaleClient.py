
import asyncio
import os
import tailScaleServer

from websockets.asyncio.client import connect

async def main(computerName=None):
    serverIP = tailScaleServer.getTailscaleIP(computerName)

    if serverIP is None:
        raise RuntimeError(
            f"Computer '{computerName}' was not found in Tailscale status."
        )

    serverURL = f"ws://{serverIP}:8765"

    print(f"Attempting connection to {serverURL=}")

    async with connect(serverURL) as websocket:
        print(f"Connected to {serverURL}")
        print("Type a message and press Enter.")

        async def receive():
            async for message in websocket:
                print(f"\nPeer: {message}")

        async def send():
            while True:
                message = await asyncio.to_thread(input, "> ")
                await websocket.send(message)

        await asyncio.gather(receive(), send())


if __name__ == "__main__":
    asyncio.run(main())
