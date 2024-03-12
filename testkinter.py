import asyncio
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import ConnectEsp32
import tk_async_execute as tae
import os


async def connect():
    await ConnectEsp32.connectesp32()
    await asyncio.sleep(0.02)
    connectedmsg()
    button_enable.grid(column=0, padx=10, pady=10)


conectado = False


def connectedmsg():
    tkinter.messagebox.showinfo("Arara", "Conexão estabelecida")
    global conectado
    conectado = True
    status.config(text="Arara Conectada", fg="green")


def botaoclicado():
    tae.async_execute(connect(), wait=True, visible=True, pop_up=True, callback=None, master=root)


is_on = True


async def switch():
    global is_on
    # Determine is on or off
    if is_on:
        button_enable.config(image=on)
        await ConnectEsp32.sendenable()
        is_on = False
    else:
        button_enable.config(image=off)
        await ConnectEsp32.senddisable()
        is_on = True


def toggle():
    tae.async_execute(switch(), wait=True, pop_up=False, callback=None, master=root)


def close_tk():
    tae.async_execute(quit_tk(), wait=True, pop_up=True, callback=None, master=root)


listbox_codes = tk.Listbox(tk.Listbox(), height=5, selectmode="SINGLE")


def code_box():
    uploadwindow = tk.Toplevel(root)
    uploadwindow.title("Codes")
    uploadwindow.geometry("300x300")
    global listbox_codes
    listbox_codes = tk.Listbox(uploadwindow, height=5, selectmode="SINGLE")
    listbox_codes.insert(1, 'ArcadeDrive')
    listbox_codes.insert(2, 'Mecanum')
    listbox_codes.pack()
    button_ok = tk.Button(uploadwindow, text="Ok", command=upload)
    button_ok.pack()
    button_cancel = tk.Button(uploadwindow, text="Cancel", command=uploadwindow.destroy)
    button_cancel.pack()


async def uploadarara():
    global listbox_codes
    print(listbox_codes.get(listbox_codes.curselection(), tk.END))
    os.system(r'cmd /c "	python -m esptool --before default_reset --after '
              r'hard_reset write_flash  -z --flash_mode dio --flash_freq 80m 0x1000 '
              r'C:\Users\enzo\AppData\Local\Temp\arduino\sketches\A7D656D79A498BAB38BF28E196B7DB4E/testeFlash.ino'
              r'.bootloader.bin 0x8000 '
              r'C:\Users\enzo\AppData\Local\Temp\arduino\sketches\A7D656D79A498BAB38BF28E196B7DB4E/testeFlash.ino'
              r'.partitions.bin 0xe000 C:\Users\enzo\AppData\Local\Arduino15\packages\esp32\hardware\esp32\2.0.14'
              r'/tools/partitions/boot_app0.bin 0x10000 '
              r'C:\Users\enzo\AppData\Local\Temp\arduino\sketches\A7D656D79A498BAB38BF28E196B7DB4E/testeFlash.ino'
              r'.bin"')

    tkinter.messagebox.showinfo("Arara", "O código foi passado com sucesso!")


def upload(teste=tk.Listbox):
    tae.async_execute(uploadarara(teste), wait=True, pop_up=True, callback=None, master=root)


async def quit_tk():
    if conectado:
        await ConnectEsp32.desconnect()
    root.quit()


# root window
root = tk.Tk()

on = tk.PhotoImage(file="on.png")
off = tk.PhotoImage(file="off.png")
arara = tk.PhotoImage(file="arara.png")
root.iconphoto(True, arara)

button_connect = ttk.Button(root, text="Connect Arara", command=botaoclicado, width=15)
button_connect.grid(column=0)
button_upload = ttk.Button(root, text="Upload", command=code_box())
button_upload.grid(column=0, pady=100)

button_enable = ttk.Button(root, image=off, command=toggle)
status = tkinter.Label(root, text="Arara não conectada a Driver Station", font=("Helvetica", 18), fg="gray")
status.grid(column=1, row=0, padx=800)
root.state('zoomed')
root.resizable(True, True)
root.title('Arara Demo')

button_exit = ttk.Button(root, text="Disconnect", command=close_tk, width=15)
button_exit.grid(column=0)

tae.start()
root.mainloop()
tae.stop()
