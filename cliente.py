from Client import Cliente
from socket import *
import sys


def connection_setup(server_name, server_port):
    # Verifica se o endereço é IPv4 ou IPv6. Se o endereço não for IPv4 ele
    # joga uma exceção e tenta se conectar com IPv6
    try:
        inet_aton(server_name)
        client_socket = socket(AF_INET, SOCK_STREAM)
    except:
        client_socket = socket(AF_INET6, SOCK_STREAM)
    
    client_socket.connect((server_name, server_port))
    print("Connected on: ")
    print(client_socket.getsockname())
    return client_socket


def attack_received(cliente, client_socket):
    # Recebe a mensagem com o ataque
    rcv_msg = client_socket.recv(2048)
    rcv_msg = rcv_msg.decode().split(" ")
    x = rcv_msg[0]
    y = int(rcv_msg[1])
    print("Attack received at {}, {}".format(x, y))

    # Verifica se o ataque acertou
    ans = cliente.check_hit_taken(x, y)
    if(ans):
        response = "Hit"
    else:
        response = "Miss"

    # Devolve a resposta ao servidor com o resultado do ataque
    client_status = cliente.check_for_boats()
    client_socket.send((response + ";" + str(client_status)).encode())

    # Espera um sinal do servidor avisando que o cliente pode prosseguir com o ataque
    if(client_status):
        signal = client_socket.recv(2048)
    return not(client_status)


def send_attack(cliente, msg, client_socket):
    # Envia um ataque ao servidor
    client_socket.send(msg.encode())
    msg = msg.split(" ")
    x = msg[0]
    y = int(msg[1])
    print("Fire at {}, {}".format(x, y))

    # Recebe o resultado do ataque
    rcv_msg = client_socket.recv(2048)
    signal = "OK"
    if(rcv_msg.decode().split(";")[0] == "Hit"):
        cliente.hit(x, y)

        # Junto a mensagem de status do ataque também há uma mensagem de status do tabuleiro
        # Se a mensagem for True, quer dizer que ainda há navios no campo inimigo
        # Se a mensagem for False o jogo acaba
        server_status = rcv_msg.decode().split(";")[1]
        if(server_status == "True"):
            # Envia um sinal ao servidor avisando que ele pode fazer seu ataque
            client_socket.send(signal.encode())
            return False
        else:
            print("Server lost!")
            return True

    elif(rcv_msg.decode().split(";")[0] == "Miss"):
        cliente.miss(x, y)
        # Envia um sinal ao servidor avisando que ele pode fazer seu ataque
        client_socket.send(signal.encode())
        return False
    

def main():
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    client_socket = connection_setup(server_name, server_port)
    cliente = Cliente()

    game_over = False
    print("Game started")
    while(not(game_over)):
        msg = input("Where would you like to shoot: ")
        if(cliente.check_valid_play(msg.split(" "))):
            if(msg[0] == 'p' or msg[0] == 'P'):
                cliente.print_tables()
            else:
                # A variável game_over recebe a todo momento o status do jogo. Se o status for True
                # quer dizer que o jogo acabou.
                if(not(game_over)):
                    game_over = send_attack(cliente, msg, client_socket)
                if(not(game_over)):
                    game_over = attack_received(cliente, client_socket)
    
    client_socket.close()


if __name__ == "__main__":
    main()