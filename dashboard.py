import asyncio
import tkinter as tk
import tkinter.messagebox
import constants
import gamepad
import paths
import threading
import connectarara
import tk_async_execute as tae
import os

# Variável que indica a conexão com a placa
conectado = False

# Variável que controla o switch enable/disable
is_on = True

# Variável que controla qual código será instalado na placa
valor = " "

# Controle de caminho: Verifica se estamos executando o programa direto na IDE e organiza o caminho relativo dos
# arquivos É útil para debugar o programa
caminho_projeto = os.path.abspath('dashboard.py').lower()
if '\\araradashboard\\'.lower() in caminho_projeto:
    caminho_projeto = ""  # String vazia
else:
    caminho_projeto = "_internal\\"  # Pyinstaller coloca os arquivos dentr de uma pasta _internal

# Lista que possui todos os códigos que podem ser executados na placa
# Caso for adicionar uma nova pasta, lembre-se de colocar nessa lista o nome exato do diretório que possui o binário do
# código c++
item_listbox = ["ArcadeDrive", "Test"]

# Cria um objeto de loop principal, necessário para rodar todas partes do programa em um único gerenciador
runner = asyncio.Runner()

# Variável que define se o programa foi aberto
c = 0

estado_gamepad = False


def gamepad_events():
    global estado_gamepad
    while True:
        estado_gamepad = gamepad.event_gamepad()
        if estado_gamepad:
            imagem_gamepad.config(image=gamepad_icon_on, highlightthickness=0)
        else:
            imagem_gamepad.config(image=gamepad_icon_off, highlightthickness=0)


<<<<<<< HEAD
class WindowTest(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Esquema de funcionamento")
        self.imagem = tk.PhotoImage(file="Codes/imagens/test.png")
        self.configure(background="#1a1a1a", highlightthickness=0)
        self.geometry("750x600")
        self.resizable(False, False)
        self.canva = tk.Canvas(self, width=700, height=700)
        self.canva.pack(fill="both", expand=True)
        self.canva.create_image(0, 0, image=self.imagem, anchor="nw")


=======
>>>>>>> feat-ping
# Classe que abre uma janela para selecionar um código para dar upload na placa
class CodeJanela(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Códigos")
        self.configure(background="#1a1a1a", highlightthickness=0)
        self.geometry("200x200")
        self.resizable(False, False)
        self.listbox_codes = tk.Listbox(self, height=5, selectmode="SINGLE", highlightthickness=0)
        for i in item_listbox:
            self.listbox_codes.insert(tk.END, i)  # Indexa todos os elentos a listbox
        self.listbox_codes.pack()
        self.button_upload = tk.Button(self, text="Ok", command=self.upload, highlightthickness=0)
        self.button_upload.place(x=100, y=170)
        self.button_cancel = tk.Button(self, text="Cancel", command=self.destroy, highlightthickness=0)
        self.button_cancel.place(x=130, y=170)

    # Função que define qual objeto da lista deve ser instalado
    def upload(self):
        global valor
        curse_selection = self.listbox_codes.curselection()
        if curse_selection:
            valor = self.listbox_codes.get(curse_selection)
        upload_handler()


async def pingget():
    global conectado
    global c
    global is_on
    while conectado:
        try:
            await connectarara.getping()
            await asyncio.sleep(5)
        except connectarara.return_error_closed():
            tkinter.messagebox.showerror("Arara Error", "Verifique sua conexão Wi-Fi!")
            label_connection.config(text="Não conectado", fg="red")
            conectado = False
            is_on = True
            c = 0
            button_enable.config(image=off)
            break


async def connect():
    await connectarara.connect_wifi()
    await asyncio.sleep(0.02)
    connected_msg()
    button_enable.place(x=constants.ButtonEnable.POSICAO_X, y=constants.ButtonEnable.POSICAO_y)


def connected_msg():
    tkinter.messagebox.showinfo("Arara", "Conexão estabelecida")
    global conectado
    conectado = True
    label_connection.config(text="Arara Conectada", fg="green")


def connect_thread():
    threading.Thread(target=connect_handler, daemon=True).start()


# Função que lança uma co-rotina para conectar a placa
def connect_handler():
    try:
        runner.run(connect())
        if conectado:
            runner.run(pingget())
    except TimeoutError:
        tkinter.messagebox.showerror("Arara", "Timeout error")
    except ConnectionAbortedError:
        tkinter.messagebox.showerror("Arara", "A conexão foi anulada pelo sistema")
    except OSError:
        tkinter.messagebox.showerror("Arara", "Não é possível alcançar o local da rede")
    except RuntimeError:
        tkinter.messagebox.showerror("Arara", "Não é possível utilizar este comando!")


# Função que envia os valores do gamepad a placa
async def send_gamepad_values():
    global conectado
    global is_on
    global c
    while conectado:  # Verifica se placa está conectada (Loop só fecha quando a janela principal fecha)
        while not is_on and estado_gamepad:  # Verifica se a o estado do botão está em enable/disable
            try:
                data = gamepad.getgamepadvalues()  # Retorna os valores do gamepad (já codificado)
                await connectarara.sendvalues(data)  # Envia os valores para a placa
                await asyncio.sleep(0.025)  # Espera 25ms
            except connectarara.return_error_closed():
                tkinter.messagebox.showerror("Arara Error", "Verifique sua conexão Wi-Fi!")
                label_connection.config(text="Não conectado", fg="red")
                conectado = False
                is_on = True
                c = 0
                button_enable.config(image=off)
                break
        await asyncio.sleep(1)


def handler():
    runner.run(send_gamepad_values())


# Função que inicia uma co-rotina para obter os valores do gamepad
async def handlergamepadping():
    # await asyncio.gather(send_gamepad_values(), pingget())
    pass


# Função toggle que define o estado do botão Enable/Disable
async def switch():
    global is_on
    if is_on:
        try:
            button_enable.config(image=on)
            is_on = False
        except connectarara.return_error_closed():
            tkinter.messagebox.showerror(constants.AraraError.TITLE,
                                         constants.AraraError.MESSAGE_WIFI_DISCONNECT)
    else:
        try:
            button_enable.config(image=off)
            is_on = True
        except connectarara.return_error_closed():
            tkinter.messagebox.showerror(constants.AraraError.TITLE,
                                         constants.AraraError.MESSAGE_WIFI_DISCONNECT)


# Função que lança o toggle e inicia a enviar os valores do gamepad
def toggle():
    global c
    if conectado:
        tae.async_execute(switch(), wait=True, pop_up=True, callback=None, master=root)
    else:
        tkinter.messagebox.showerror("Arara Error", "Não é possivel utilizar esse comando")
    if c == 0:
        threading.Thread(target=handler, daemon=True).start()
        c = 1


# Função que fecha o dashboard
def close_dashboard():
    try:
        runner.run(quit_tk())
    finally:
        root.quit()
        runner.close()


# Função que faz o flash do código para a placa
async def upload_to_arara():
    if valor != " ":
        result = paths.flash_code_arara(name=valor, caminho=caminho_projeto)  # Aqui é feito o comando para upar
        if result == "Flash":
            tkinter.messagebox.showinfo("Arara", "O código foi passado com sucesso!")
        if result == "Fatal Exception":
            tkinter.messagebox.showerror("Arara", "Erro ao dar upload para Arara, tente novamente!")
    else:
        tkinter.messagebox.showwarning("Arara", "Nenhum código foi selecioando!")


# Função que chama as funções para dar o upload para a placa
def upload_handler():
    tae.async_execute(upload_to_arara(), wait=True, pop_up=True, callback=None, master=root)


# Função que desconecta e define as variáveis para fechar o programa
async def quit_tk():
    global conectado
    global is_on
    is_on = True
    if conectado:
        conectado = False
        await connectarara.disconnect_wifi()


# Janela principal
root = tk.Tk()
root.configure(background=constants.Janela.BACKGROUND, highlightthickness=constants.Janela.HIGHTLIGHTTHICKNESS)
# Define o tamanho da janela e o título
root.geometry(constants.Janela.SIZE)
root.resizable(False, False)
root.title(constants.Janela.TITLE)

# Imagens utilizadas no aplicativo
on = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/on.png")
off = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/off.png")
arara = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/arara.png")
arara_logo = tk.PhotoImage(file=(caminho_projeto + "Codes\\imagens/arara_icon.png"))
arara_text = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/arara_text.png")
wifi_icon = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/wifi.png")
exit_icon = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/exit.png")
transferir_icon = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/transferir.png")
gamepad_icon_off = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/gamepadoff.png")
gamepad_icon_on = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/gamepadon.png")

imagem_gamepad = tk.Label(root, image=gamepad_icon_off, background=constants.GamepadLabel.BACKGROUND)
imagem_gamepad.place(x=constants.GamepadLabel.POSICAO_X, y=constants.GamepadLabel.POSICAO_Y)

canvas = tk.Canvas(root, width=constants.MenuBar.WIDTH, height=constants.MenuBar.HEIGHT,
                   background=constants.MenuBar.BACKGROUND,
                   highlightthickness=constants.MenuBar.HIGHTLIGHTTHICKNESS,
                   highlightcolor=constants.MenuBar.HIGHLIGHT_COLOUR)
canvas.place(y=constants.MenuBar.POSICAO_Y, x=constants.MenuBar.POSICAO_X)

imagem_al = tk.Label(canvas, image=arara_logo, bg=constants.AraraLogo.BACKGROUND)
imagem_al.place(x=constants.AraraLogo.POSICAO_X_IMAGEM, y=constants.AraraLogo.POSICAO_Y_IMAGEM)
imagem_text = tk.Label(canvas, image=arara_text, bg=constants.AraraLogo.BACKGROUND)
imagem_text.place(x=constants.AraraLogo.POSICAO_X_TEXT, y=constants.AraraLogo.POSICAO_Y_TEXT)

root.iconphoto(True, arara)

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

label_connection = tk.Label(root, text="Não conectado", fg="red", bg="#1a1a1a", font=("Roboto", 16))
label_connection.place(x=30, y=410)

thread_gamepad = threading.Thread(target=gamepad_events, daemon=True)
thread_gamepad.start()
# Loop do tkinter e tk-async
tae.start()
root.protocol("WM_DELETE_WINDOW", close_dashboard)
root.mainloop()
tae.stop()
