import asyncio
import websockets

clientes = set()

async def chat(websocket, path):
    clientes.add(websocket)
    try:
        async for message in websocket:
            for cliente in clientes:
                await cliente.send(message)
    finally:
        clientes.remove(websocket)

start_server = websockets.serve(chat, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()