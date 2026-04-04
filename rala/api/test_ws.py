import asyncio
import websockets

async def test():
    try:
        async with websockets.connect("ws://localhost:8000/ws/sensors") as ws:
            print("Connected to WS successfully!")
            for _ in range(3):
                msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                print("Received payload ID:", msg[10:40]) # snippet
            print("WebSocket stream is completely functional!")
    except asyncio.TimeoutError:
        print("Timeout! No data received from WebSocket within 5 seconds.")
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
