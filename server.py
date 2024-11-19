import socket
import threading

HOST = '192.168.5.101'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []

def separaae(message, username):

    if message.startswith('@'):
        message = message[1:].strip()  #separa o @ do nome do destinatario

    #divide a mensagem em duas partes: o nome do destinatário e o conteudo
    parts = message.split(' ', 1)
    if len(parts) < 2:
        return None, None

    target_user = parts[0].strip()  #destinatário
    private_message = parts[1].strip()  #conteudo da mensagem privada


    return target_user, private_message


def mandanadm(target_user, private_message, username): #percorre todos os clientes para encontrar o destinatário
    
    for user, client in active_clients:
        if user.lower() == target_user.lower():
            msg_to_client(client, f"DM de {username}: {private_message}")
    for sender_user, sender_client in active_clients:
        if sender_user.lower() == username.lower():
            msg_to_client(sender_client, f"Você enviou para {target_user}: {private_message}")
            return

    #se o usuário não for encontrado, envia uma mensagem de erro
    for user, client in active_clients:
        if user.lower() == username.lower():
            msg_to_client(client, f"Usuário {target_user} não encontrado.")
            return
