
import asyncio
import os

from websockets.asyncio.server import serve
import subprocess


def getTailscaleIP(computerName: str) -> str | None:
    """
    Retrieve the Tailscale IP address for a computer by its hostname.
    """
    if not computerName or computerName == "localhost":
        return "127.0.0.1"

    try:
        result = subprocess.run(
            ["tailscale", "status"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve Tailscale status: {e.stderr}") from e
    except FileNotFoundError as e:
        raise RuntimeError(
            "Tailscale CLI was not found. Ensure it is installed and on PATH."
        ) from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("Tailscale status command timed out.") from e

    for line in result.stdout.splitlines():
        fields = line.split()

        # Expected format: IP hostname username OS status
        if len(fields) >= 2 and fields[1].lower() == computerName.lower():
            return fields[0]

    return None


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


async def main(computerName="localhost", port=8765):
    host = getTailscaleIP(computerName)

    if host is None:
        raise RuntimeError(
            f"Computer '{computerName}' was not found in Tailscale status."
        )
    
    async with serve(handler, host, port):
        print(f"WebSocket server listening on {host}:{port}", flush=True)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
