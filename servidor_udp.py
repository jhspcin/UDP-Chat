# Importando as bibliotecas necessárias
import socket
import threading
import queue
from datetime import datetime

# obter a data e hora
datahora = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

# Configurando uma fila para armazenar mensagens e uma lista para os clientes
messages = queue.Queue()
clientes = []

# Configurando o servidor UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

# função para escutar mensagens dos clientes e adicionar à fila
def escutar():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

# função para transmitir mensagens e gerenciar a lista de clientes
def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(f"{addr[0]}:{addr[1]}/~{message.decode()} {datahora}")
            
            if addr not in clientes:
                clientes.append(addr)
                
                # Notificando todos os clientes sobre a chegada de um novo membro
                for client in clientes:
                    try:
                        if message.decode().startswith("NewUser"):
                            name = message.decode()[message.decode().index(":") + 1:]
                            server.sendto(f"{name} uniu-se!".encode(), client)
                        elif message.decode().startswith("Chegou!"):
                            name = message.decode()[message.decode().index(":") + 1:]
                            server.sendto(f"{name} você está logado".encode(), client)
                        else:
                            server.sendto(message, client)
                    except:
                        clientes.remove(client)

# Iniciando as duas funções ao mesmo tempo
t1 = threading.Thread(target=escutar)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
