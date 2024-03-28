import asyncio
import json
import websockets

global ws


# Cria o objeto de websockets
async def connect_wifi():
    global ws
    ws = await websockets.connect('ws://192.168.4.1', ping_interval=None)
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
    mensagem = {"Estado": "Habilitado"}
    await ws.send(json.dumps(mensagem))


# Envia disable
async def senddisable():
    mensagem = {"Estado": "Desabilitado"}
    await ws.send(json.dumps(mensagem))


# Função que recebe a conexão da placa
async def receiveconnect():
    return await ws.recv()


# Envia valores para a placa
async def sendvalues(mensagem):
    await ws.send(mensagem)


# Retorna um erro de queda de conexão
def return_error_closed():
    return websockets.exceptions.ConnectionClosedError
