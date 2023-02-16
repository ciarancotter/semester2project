import asyncio
import websockets
import json
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

data = {"HandInfront": False}
json_data = json.dumps(data).encode('utf-8')

async def send(websocket, path):
        await websocket.send(json_data)

async def main():
    async with websockets.serve(send, "127.0.0.1", 65432):
        await asyncio.Future()  # Run forever

if __name__ == '__main__':
    asyncio.run(main())