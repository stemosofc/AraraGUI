import asyncio
import json
import websockets
import logging
import tkinter 

# Configuração do logger
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class EasySteam:
    def __init__(self):
        self.ws = None
        self.connection = False
        self.uri = 'ws://192.168.4.1/ws'
        self.ping_interval = 5
        self.ping_timeout = 7
    
    async def connect(self):
        try:
            self.ws = await websockets.connect(self.uri, ping_interval=self.ping_interval, ping_timeout=self.ping_timeout)
            await asyncio.sleep(0.010)
            self.connection = True
            tkinter.messagebox.showinfo("EasySTEAM", "Conexão estabelecida")
        except TimeoutError:
            tkinter.messagebox.showerror("EasySTEAM Error", "Timeout error")
        except ConnectionAbortedError:
            tkinter.messagebox.showerror("EasySTEAM Error", "A conexão foi anulada pelo sistema")
        except OSError:
            tkinter.messagebox.showerror("EasySTEAM Error", "Não é possível alcançar o local da rede")
        except RuntimeError:
            tkinter.messagebox.showerror("EasySTEAM Error", "Não é possível utilizar este comando!")
        
        
    async def getping(self):
        pong = await self.ws.ping()
        self.latency = await pong
        print(round(self.latency * 1000, 2))
        await asyncio.sleep(5)
        return self.latency


    def getconnection(self):
        return self.connection
    
    
    async def disconnect(self):
        await self.ws.close()
        self.connection = False


    async def sendvalues(self, mensagem):
        await self.ws.send(json.dumps(mensagem))
        await asyncio.sleep(0.025)
        
    
    def wifierror(self):
        tkinter.messagebox.showerror("EasySTEAM Error", "Verifique sua conexão Wi-Fi!")
        self.connection = False

