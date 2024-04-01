import asyncio
import tkinter as tk
import tkinter.messagebox
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
item_listbox = ["ArcadeDrive", "Mecanum", "Teste", "Print"]

# Cria um objeto de loop principal, necessário para rodar todas partes do programa em um único gerenciador
runner = asyncio.Runner()

# Variável que define se o programa foi aberto
c = 0


# Classe que abre uma janela para selecionar um código para dar upload na placa
class CodeJanela(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Códigos")
        self.configure(background="#d3d3d3", highlightthickness=0)
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


async def connect():
    await connectarara.connect_wifi()
    await asyncio.sleep(0.02)
    connected_msg()
    button_enable.place(x=250, y=260)


def connected_msg():
    tkinter.messagebox.showinfo("Arara", "Conexão estabelecida")
    global conectado
    conectado = True
    # status.config(text="Arara Conectada", fg="green")


def connect_thread():
    threading.Thread(target=connect_handler, daemon=True).start()


# Função que lança uma co-rotina para conectar a placa
def connect_handler():
    try:
        runner.run(connect())
    except TimeoutError:
        tkinter.messagebox.showerror("Arara", "Timeout error")
    except ConnectionAbortedError:
        tkinter.messagebox.showerror("Arara", "A conexão foi anulada pelo sistema")
    except OSError:
        tkinter.messagebox.showerror("Arara", "Não é possível alcançar o local da rede")


# Função que envia os valores do gamepad a placa
async def send_gamepad_values():
    global conectado
    while conectado:  # Verifica se placa está conectada (Loop só fecha quando a janela principal fecha)
        while not is_on:  # Verifica se a o estado do botão está em enable/disable
            try:
                data = gamepad.getjson()  # Retorna os valores do gamepad (já codificado)
                await connectarara.sendvalues(data)  # Envia os valores para a placa
                await asyncio.sleep(0.025)  # Espera 25ms
            except connectarara.return_error_closed():
                # Caso a conexão caia mostra o seguinte aviso
                tkinter.messagebox.showerror("Arara", "Placa desconectada! Verifique o WiFi!")
                conectado = False
                break
    global c
    c = 0


# Função que inicia uma co-rotina para obter os valores do gamepad
def handler():
    runner.run(send_gamepad_values())


# Função toggle que define o estado do botão Enable/Disable
async def switch():
    global is_on
    if is_on:
        button_enable.config(image=on)
        is_on = False
        try:
            await connectarara.sendenable()
        except AssertionError as msg:
            print(msg)
    else:
        button_enable.config(image=off)
        is_on = True
        try:
            await asyncio.sleep(0.05)
            await connectarara.senddisable()
        except AssertionError as msg:
            print(msg)


def switch_handler():
    pass


# Função que lança o toggle e inicia a enviar os valores do gamepad
def toggle():
    global c
    tae.async_execute(switch(), wait=True, pop_up=False, callback=None, master=root, visible=False)
    if c == 0:
        thread = threading.Thread(target=handler, daemon=True)
        thread.start()
        c += 1


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
        result = paths.flash_code_arara(valor, caminho=caminho_projeto)  # Aqui é feito o comando para upar
        match result:
            case "Flash":
                tkinter.messagebox.showinfo("Arara", "O código foi passado com sucesso!")
            case "Fatal Exception":
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
root.configure(background="#d3d3d3", highlightthickness=0)

# Imagens utilizadas no aplicativo
on = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/on.png")
off = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/off.png")
arara = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/arara.png")
arara_logo = tk.PhotoImage(file=(caminho_projeto + "Codes\\imagens/arara_logo.png"))
wifi_icon = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/wifi.png")
exit_icon = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/exit.png")
transferir_icon = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/transferir.png")

root.iconphoto(True, arara)
canvas = tk.Canvas(root, width=470, height=100, background="#787878", highlightthickness=0, highlightcolor='black')
canvas.place(y=0, x=-5)
imagem_al = tk.Label(canvas, image=arara_logo, bg='#5c0a5c')
imagem_al.place(x=40, y=20)
canvas.create_rectangle(0, 0, 470, 100, fill='#5c0a5c')
text_stemos = tk.Label(text='stemOS', font=('Roboto', 45), fg='#fff', bg='#5c0a5c', width=10, highlightthickness=0)
text_stemos.place(y=10, x=150)
# Cria os botões de conexão e upload
button_connect = tk.Button(root, image=wifi_icon, command=connect_thread, width=80, highlightthickness=0,
                           borderwidth=0, bg="#d3d3d3")
button_connect.place(x=25, y=150)
button_upload = tk.Button(root, image=transferir_icon, command=CodeJanela, highlightthickness=0, width=80,
                          borderwidth=0, bg="#d3d3d3")
button_upload.place(x=25, y=250)

# Cria o botão de enable mas não mostra
button_enable = tk.Button(root, image=off, command=toggle, highlightthickness=0)

# status = tkinter.Label(root, text="Arara não conectada a Driver Station", font=("Helvetica", 13), fg="gray")
# status.grid(column=1, row=0, padx=50, pady=20)

# Define o tamanho da janela e o título
root.geometry("450x450")
root.resizable(False, False)
root.title('Arara v1.2')

# Botão de desconexão
button_exit = tk.Button(root, image=exit_icon, command=close_dashboard, width=70,
                        highlightthickness=0, borderwidth=0, bg="#d3d3d3")
button_exit.place(x=30, y=350)

# Loop do tkinter e tk-async
tae.start()
root.protocol("WM_DELETE_WINDOW", close_dashboard)
root.mainloop()
tae.stop()
