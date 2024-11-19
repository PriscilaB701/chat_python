import socket
import threading
import tkinter as tk
from tkinter import Button, scrolledtext
from tkinter import messagebox

HOST = '192.168.5.101'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER]: Conectado com sucesso")
    except:
        messagebox.showerror("Erro", "Erro ao se conectar")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("User inválido", "User não pode estar vazio")

    threading.Thread(target=listen_for_msg_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    message = message_textbox.get().strip()  #strip p/ remover espaços extras
    if message:
        try:
            client.sendall(message.encode())
            if message == '/quit':
                client.close()  
                root.destroy()  
            else:
                message_textbox.delete(0, tk.END)  #limpa a caixa de entrada
        except Exception as e:
            messagebox.showerror("Erro", "Não foi possível enviar a mensagem.")
            print(f"Erro ao enviar mensagem: {e}")
    else:
        messagebox.showerror("Mensagem vazia", "Mensagem não pode estar vazia")
