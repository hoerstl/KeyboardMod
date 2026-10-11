
import asyncio
import os

from websockets.asyncio.client import connect

SERVER_IP = os.environ["WS_SERVER_IP"]
SERVER_URL = f"ws://{SERVER_IP}:8765"


async def main():
    async with connect(SERVER_URL) as websocket:
        print(f"Connected to {SERVER_URL}")
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
