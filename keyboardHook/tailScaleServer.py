
import asyncio
import os

from websockets.asyncio.server import serve

HOST = os.environ.get("WS_HOST", "127.0.0.1")
PORT = 8765

clients = set()


async def handler(websocket):
    clients.add(websocket)
    print(f"Connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received: {message}")

            # Send the message to every other connected client.
            recipients = clients - {websocket}

            if recipients:
                results = await asyncio.gather(
                    *(client.send(message) for client in recipients),
                    return_exceptions=True,
                )

                # Remove clients that failed to receive a message.
                for client, result in zip(recipients, results):
                    if isinstance(result, Exception):
                        clients.discard(client)
    except Exception as exc:
        print(f"Connection error: {exc}")
    finally:
        clients.discard(websocket)
        print("Disconnected")


async def main():
    async with serve(handler, HOST, PORT):
        print(f"WebSocket server listening on {HOST}:{PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
