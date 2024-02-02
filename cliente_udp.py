# Importando bibliotecas necessárias
import socket
import threading
import random
from datetime import datetime

# Obtendo a data e hora atual 
datahora = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

# Configurando o cliente UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.bind(("localhost", random.randint(8000, 9000)))

# Solicitando o nome de usuário
nome = input("UserName: ")

# Função para receber mensagens
def receber():
    while True:
        try:
            # Recebendo mensagens e endereço do remetente
            mensagens, addr = cliente.recvfrom(1024)
            print(f"\n{addr[0]}:{addr[1]}/~{mensagens.decode()} {datahora}")
        except Exception as e:
            print(f"Erro ao receber: {e}")

# Iniciando uma thread para a função receber
t = threading.Thread(target=receber)
t.start()

# Bloco principal do programa
try:
    # Verificando se o nome começa com "hi, meu nome eh"
    if nome.startswith("hi, meu nome eh"):
        # Enviando mensagem de novo usuário ao servidor
        cliente.sendto(f"NewUser:{nome[nome.index('h')+1:]}".encode(), ("localhost", 9999))
    else:
        # Enviando mensagem de chegada ao servidor
        cliente.sendto(f"Chegou!:{nome}".encode(), ("localhost", 9999))

    # Loop para enviar mensagens
    while True:
        mensagem = input("Mensagem: ")
        if mensagem == "bye":
            exit()
        else:
            # Enviando mensagem ao servidor
            cliente.sendto(f"{nome}: {mensagem}".encode(), ("localhost", 9999))

# Tratando interrupção do usuário (Ctrl+C)
except KeyboardInterrupt:
    print("PROGRAMA INTERROMPIDO")