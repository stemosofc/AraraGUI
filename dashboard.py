import asyncio
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import paths
import connectarara
import tk_async_execute as tae
import os

conectado = False

is_on = True

valor = " "

caminho_projeto = os.path.abspath('dashboard.py').lower()
if '\\araradashboard\\'.lower() in caminho_projeto:
    caminho_projeto = ""
else:
    caminho_projeto = "_internal\\"


item_listbox = ["ArcadeDrive", "Mecanum", "Teste"]


class CodeJanela(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Code List")
        self.geometry("200x200")
        self.listbox_codes = tk.Listbox(self, height=5, selectmode="SINGLE")
        for i in item_listbox:
            self.listbox_codes.insert(tk.END, i)
        self.listbox_codes.pack()
        self.button_upload = tk.Button(self, text="Ok", command=self.upload)
        self.button_upload.place(x=100, y=170)
        self.button_cancel = tk.Button(self, text="Cancel", command=self.destroy)
        self.button_cancel.place(x=130, y=170)

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
    button_enable.place(x=250, y=50)


def connected_msg():
    tkinter.messagebox.showinfo("Arara", "Conexão estabelecida")
    global conectado
    conectado = True
    # status.config(text="Arara Conectada", fg="green")


def connect_handler():
    tae.async_execute(connect(), wait=True, visible=True, pop_up=True, callback=None, master=root)


async def switch():
    global is_on
    # Determine is on or off
    if is_on:
        button_enable.config(image=on)
        await connectarara.sendenable()
        is_on = False
    else:
        button_enable.config(image=off)
        await connectarara.senddisable()
        is_on = True


def toggle():
    tae.async_execute(switch(), wait=True, pop_up=False, callback=None, master=root)


def close_dashboard():
    tae.async_execute(quit_tk(), wait=True, pop_up=True, callback=None, master=root)


async def upload_to_arara():
    if valor != " ":
        result = paths.flash_code_arara(valor, caminho=caminho_projeto)
        match result:
            case "Flash":
                tkinter.messagebox.showinfo("Arara", "O código foi passado com sucesso")
            case "Fatal Exception":
                tkinter.messagebox.showerror("Arara", "Erro ao dar upload para Arara, tente novamente!")
    else:
        tkinter.messagebox.showwarning("Arara", "Nenhum código foi selecioando!")


def upload_handler():
    tae.async_execute(upload_to_arara(), wait=True, pop_up=True, callback=None, master=root)


async def quit_tk():
    if conectado:
        await connectarara.disconnect_wifi()
    root.quit()


# root window
root = tk.Tk()

on = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/on.png")
off = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/off.png")
arara = tk.PhotoImage(file=caminho_projeto + "Codes\\imagens/arara.png")
root.iconphoto(True, arara)

button_connect = ttk.Button(root, text="Connect Arara", command=connect_handler, width=15)
button_connect.place(x=15, y=50)
button_upload = ttk.Button(root, text="Upload", command=CodeJanela)
button_upload.place(x=15, y=200)

button_enable = ttk.Button(root, image=off, command=toggle)
# status = tkinter.Label(root, text="Arara não conectada a Driver Station", font=("Helvetica", 13), fg="gray")
# status.grid(column=1, row=0, padx=50, pady=20)
root.geometry("450x450")
root.resizable(False, False)
root.title('Arara Demo')

button_exit = ttk.Button(root, text="Disconnect", command=close_dashboard, width=15)
button_exit.place(x=15, y=350)
tae.start()
root.protocol("WM_DELETE_WINDOW", close_dashboard)
root.mainloop()
tae.stop()
