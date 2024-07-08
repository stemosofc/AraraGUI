import asyncio
import json
import websockets
import logging


global ws
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# Cria o objeto de websockets
async def connect_wifi():
    global ws
    ws = await websockets.connect('ws://192.168.4.1/ws', ping_interval=5)
    await asyncio.sleep(0.010)


# Função não utilizada
async def connect_wifi_debugging():
    global ws
    ws = await websockets.connect('ws://localhost')
    await asyncio.sleep(0.010)


# Fecha a conexão
async def disconnect_wifi():
    await ws.close()


# Envia enable para a placa
async def sendenable():
    mensagem = {"estado": "h"}
    await ws.send(json.dumps(mensagem))


# Envia disable
async def senddisable():
    mensagem = {"estado": "d"}
    await ws.send(json.dumps(mensagem))


# Função que recebe a conexão da placa
async def receive():
    return await ws.recv()


# Envia valores para a placa
async def sendvalues(mensagem):
    await ws.send(mensagem)


# Retorna um erro de queda de conexão
def return_error_closed():
    return websockets.exceptions.ConnectionClosedError
