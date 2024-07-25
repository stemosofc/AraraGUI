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
    ws = await websockets.connect('ws://192.168.4.1/ws', ping_interval=5, ping_timeout=7)
    await asyncio.sleep(0.010)


async def getping():
    pong = await ws.ping()
    latency = await pong
    return latency


# Fecha a conexão
async def disconnect_wifi():
    await ws.close()


# Envia valores para a placa
async def sendvalues(mensagem):
    await ws.send(mensagem)


# Retorna um erro de queda de conexão
def return_error_closed():
    return websockets.exceptions.ConnectionClosedError
