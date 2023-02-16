import asyncio
import websockets
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

async def receive(websocket):
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            print(data)
        except:
            pass

async def corun():
    print("run")

async def main():
    async with websockets.connect("ws://127.0.0.1:65432") as websocket:
        await asyncio.gather(receive(websocket), corun())

if __name__ == '__main__':
    asyncio.run(main())
