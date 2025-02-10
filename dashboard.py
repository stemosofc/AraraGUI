import asyncio
import time
import tkinter as tk
import tkinter.ttk
import tkinter.messagebox

import websockets.exceptions
from easysteam import EasySteam
import constants
import errors
from gamepad import Gamepad
import paths
import threading
import easysteam


easyBoard = EasySteam()
gamepad = Gamepad()
runner = asyncio.Runner()

# Variável que controla o switch enable/disable
is_on = True

# Variável que controla qual código será instalado na placa
valor = " "


def gamepad_events():
    while root.winfo_exists():
        gamepad.event_gamepad()
        if gamepad.geteventgamepad():
            imagem_gamepad.config(image=gamepad_icon_on, highlightthickness=0)
        else:
            imagem_gamepad.config(image=gamepad_icon_off, highlightthickness=0)


class Loading(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.geometry("100x50")
        self.progressbar = tkinter.ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.pack(pady=10)
        self.progressbar.start()

    def stop(self):
        self.progressbar.stop()
        self.destroy()


class WindowTest(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Esquema de funcionamento")
        self.imagem = tk.PhotoImage(file=paths.abpath + "\\imagens/test.png")
        self.configure(background="#1a1a1a", highlightthickness=0)
        self.geometry("750x600")
        self.resizable(False, False)
        self.canva = tk.Canvas(self, width=700, height=700)
        self.canva.pack(fill="both", expand=True)
        self.canva.create_image(0, 0, image=self.imagem, anchor="nw")


# Classe que abre uma janela para selecionar um código para dar upload na placa
class CodeJanela(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.load = None
        self.title("Códigos")
        self.configure(background="#1a1a1a", highlightthickness=0)
        self.geometry("200x200")
        self.resizable(False, False)
        self.listbox_codes = tk.Listbox(self, height=5, selectmode="SINGLE", highlightthickness=0)
        for i in paths.codes:
            self.listbox_codes.insert(tk.END, i)  # Indexa todos os elentos a listbox
        self.listbox_codes.pack()
        self.button_upload = tk.Button(self, text="Ok", command=self.upload, highlightthickness=0)
        self.button_upload.place(x=100, y=170)
        self.button_cancel = tk.Button(self, text="Cancel", command=self.destroy, highlightthickness=0)
        self.button_cancel.place(x=130, y=170)

    # Função que define qual objeto da lista deve ser instalado
    def upload(self):
        self.load = Loading()
        global valor
        curse_selection = self.listbox_codes.curselection()
        if curse_selection:
            valor = self.listbox_codes.get(curse_selection)
        threading.Thread(target=self.upload_to_arara, daemon=True).start()

    # Função que faz o flash do código para a placa
    def upload_to_arara(self):
        if valor != " ":
            try:
                result = paths.flash_code_arara(name=valor)  # Aqui é feito o comando para upar
                if result == "Flash":
                    tkinter.messagebox.showinfo("Arara", "O código foi passado com sucesso!")
                    if valor == "Test":
                        WindowTest()
            except errors.NoSerialAvaible:
                tkinter.messagebox.showerror("Arara Error", "Conecte a Arara ao computador!")
            except errors.NotOpenCOM4:
                tkinter.messagebox.showerror("Arara Error", "Porta serial não disponível!")
            except errors.DisconnectDevice:
                tkinter.messagebox.showerror("Arara Error", "O dispositivo foi desconectado!")
            except errors.FatalError:
                tkinter.messagebox.showerror("Arara Error", "Não foi possível passar o código, "
                                                            "tente novamente!")
            except errors.WrongPath:
                tkinter.messagebox.showerror("Arara Error", "O caminho dos arquivos não foi encontrado!")
            except errors.WrongBootMode:
                tkinter.messagebox.showerror("Arara Error", "Segure o botão BOOT quando for passar o código")
        else:
            tkinter.messagebox.showwarning("Arara", "Nenhum código foi selecioando!")
        self.load.stop()


async def pingget():
    global is_on
    while easyBoard.connection:
        try:
            await easyBoard.getping()
        except:
            imagem_conected.config(image=connect_off)
            is_on = True
            button_enable.config(image=off)
            easyBoard.wifierror()


async def connect():
    await easyBoard.connect()
    connected_msg()
    button_enable.place(x=constants.ButtonEnable.POSICAO_X, y=constants.ButtonEnable.POSICAO_y)


def connected_msg():
    imagem_conected.config(image=connect_on)


def gamepadping():
    runner.run(gamepadping_async())


async def gamepadping_async():
    await asyncio.gather(send_gamepad_values(), pingget())


def connect_thread():
    threading.Thread(target=connect_handler, daemon=True).start()


# Função que lança uma co-rotina para conectar a placa
def connect_handler():
    try:
        if not easyBoard.connection:
            runner.run(connect())
            threading.Thread(target=gamepadping, daemon=True).start()
    except TimeoutError:
        tkinter.messagebox.showerror("EasySTEAM", "Timeout error")
    except ConnectionAbortedError:
        tkinter.messagebox.showerror("EasySTEAM", "A conexão foi anulada pelo sistema")
    except OSError:
        tkinter.messagebox.showerror("EasySTEAM", "Não é possível alcançar o local da rede")
    except RuntimeError:
        tkinter.messagebox.showerror("EasySTEAM", "Não é possível utilizar este comando!")


def handler():
    runner.run(send_gamepad_values())


async def send_gamepad_values():
    global is_on
    while easyBoard.connection:  # Verifica se placa está conectada (Loop só fecha quando a janela principal fecha)
        while gamepad.geteventgamepad():  # Verifica se a o estado do botão está em enable/disable
            try:
                data = gamepad.getgamepadvalues()  
                data["EN"] = not is_on
                await easyBoard.sendvalues(data)
            except:
                imagem_conected.config(image=connect_off)
                is_on = True
                button_enable.config(image=off)
                easyBoard.wifierror()
                break
        await asyncio.sleep(1)


# Função que lança o toggle e inicia a enviar os valores do gamepad
def toggle():
    if easyBoard.getconnection():
        switch()
    else:
        tkinter.messagebox.showerror("EasySTEAM Error", "Não é possivel utilizar esse comando")


# Função toggle que define o estado do botão Enable/Disable
def switch():
    global is_on
    if is_on:
        try:
            button_enable.config(image=on)
            is_on = False
        except easysteam.return_error_closed():
            tkinter.messagebox.showerror(constants.AraraError.TITLE,
                                         constants.AraraError.MESSAGE_WIFI_DISCONNECT)
    else:
        try:
            button_enable.config(image=off)
            is_on = True
        except easysteam.return_error_closed():
            tkinter.messagebox.showerror(constants.AraraError.TITLE,
                                         constants.AraraError.MESSAGE_WIFI_DISCONNECT)

# Função que fecha o dashboard
def close_dashboard():
    try:
        runner.run(quit_tk())
    finally:
        root.quit()
        runner.close()


# Função que desconecta e define as variáveis para fechar o programa
async def quit_tk():
    global is_on
    is_on = True
    if easyBoard.connection:
        await easyBoard.disconnect()
        is_on = False


# Janela principal
root = tk.Tk()
root.configure(background=constants.Janela.BACKGROUND, highlightthickness=constants.Janela.HIGHTLIGHTTHICKNESS)
# Define o tamanho da janela e o título
root.geometry(constants.Janela.SIZE)
root.resizable(False, False)
root.title(constants.Janela.TITLE)

# Imagens utilizadas no aplicativo
on = tk.PhotoImage(file=paths.abpath + "\\imagens/on.png")
off = tk.PhotoImage(file=paths.abpath + "\\imagens/off.png")
araraimage = tk.PhotoImage(file=paths.abpath + "\\imagens/arara.png")
arara_logo = tk.PhotoImage(file=(paths.abpath + "\\imagens/arara_icon.png"))
arara_text = tk.PhotoImage(file=paths.abpath + "\\imagens/arara_text.png")
wifi_icon = tk.PhotoImage(file=paths.abpath + "\\imagens/wifi.png")
exit_icon = tk.PhotoImage(file=paths.abpath + "\\imagens/exit.png")
transferir_icon = tk.PhotoImage(file=paths.abpath + "\\imagens/transferir.png")
gamepad_icon_off = tk.PhotoImage(file=paths.abpath + "\\imagens/gamepadoff.png")
gamepad_icon_on = tk.PhotoImage(file=paths.abpath + "\\imagens/gamepadon.png")
connect_on = tk.PhotoImage(file=paths.abpath + "\\imagens/connecton.png")
connect_off = tk.PhotoImage(file=paths.abpath + "\\imagens/desconectado.png")
imagem_gamepad = tk.Label(root, image=gamepad_icon_off, background=constants.GamepadLabel.BACKGROUND)
imagem_gamepad.place(x=20, y=constants.GamepadLabel.POSICAO_Y)

imagem_conected = tk.Label(root, image=connect_off, background=constants.GamepadLabel.BACKGROUND)
imagem_conected.place(x=270, y=293)

canvas = tk.Canvas(root, width=constants.MenuBar.WIDTH, height=constants.MenuBar.HEIGHT,
                   background=constants.MenuBar.BACKGROUND,
                   highlightthickness=constants.MenuBar.HIGHTLIGHTTHICKNESS,
                   highlightcolor=constants.MenuBar.HIGHLIGHT_COLOUR)
canvas.place(y=constants.MenuBar.POSICAO_Y, x=constants.MenuBar.POSICAO_X)

imagem_al = tk.Label(canvas, image=arara_logo, bg=constants.AraraLogo.BACKGROUND)
imagem_al.place(x=constants.AraraLogo.POSICAO_X_IMAGEM, y=constants.AraraLogo.POSICAO_Y_IMAGEM)
imagem_text = tk.Label(canvas, image=arara_text, bg=constants.AraraLogo.BACKGROUND)
imagem_text.place(x=constants.AraraLogo.POSICAO_X_TEXT, y=constants.AraraLogo.POSICAO_Y_TEXT)

root.iconphoto(True, araraimage)

# Botão de desconexão
button_exit = tk.Button(root, image=exit_icon, command=close_dashboard,
                        highlightthickness=constants.ButtonExit.HIGHTLIGHTTHICKNESS,
                        borderwidth=constants.ButtonExit.BORDER_WIDTH,
                        bg=constants.ButtonExit.BACKGROUND)
button_exit.place(x=constants.ButtonExit.POSICAO_X, y=constants.ButtonExit.POSICAO_Y)

# Cria os botões de conexão e upload
button_connect = tk.Button(root, image=wifi_icon, command=connect_thread,
                           highlightthickness=constants.ButtonConnect.HIGHTLIGHTTHICKNESS,
                           borderwidth=constants.ButtonConnect.BORDER_WIDTH, bg=constants.ButtonConnect.BACKGROUND)
button_connect.place(x=constants.ButtonConnect.POSICAO_X, y=constants.ButtonConnect.POSICAO_Y)

button_upload = tk.Button(root, image=transferir_icon, command=CodeJanela,
                          highlightthickness=constants.ButtonUpload.HIGHTLIGHTTHICKNESS,
                          borderwidth=constants.ButtonConnect.BORDER_WIDTH, bg=constants.ButtonUpload.BACKGROUND)
button_upload.place(x=constants.ButtonUpload.POSICAO_X, y=constants.ButtonUpload.POSICAO_Y)

# Cria o botão de enable mas não mostra
button_enable = tk.Button(root, image=off, command=toggle,
                          highlightthickness=constants.ButtonEnable.HIGHTLIGHTTHICKNESS,
                          bg=constants.ButtonEnable.BACKGROUND, borderwidth=constants.ButtonConnect.BORDER_WIDTH)

thread_gamepad = threading.Thread(target=gamepad_events, daemon=True)
thread_gamepad.start()
# Loop do tkinter e tk-async
root.protocol("WM_DELETE_WINDOW", close_dashboard)
root.mainloop()
