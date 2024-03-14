import asyncio
import json
import websockets

global ws


async def connect_wifi():
    global ws
    ws = await websockets.connect('ws://192.168.4.1')
    await asyncio.sleep(0.010)


async def disconnect_wifi():
    await ws.close()


async def sendenable():
    mensagem = {"Estado": "Habilitado"}
    await ws.send(json.dumps(mensagem))


async def senddisable():
    mensagem = {"Estado": "Desabilitado"}
    await ws.send(json.dumps(mensagem))


async def receiveconnect():
    return await ws.recv()
