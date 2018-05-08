from Server import Servidor
from socket import *
import sys


def connection_setup(server_port):
    server_socket = socket(AF_INET6, SOCK_STREAM)
    server_socket.bind(("", server_port))
    server_socket.listen(1)
    conn_socket, client_addr = server_socket.accept()
    return  conn_socket


def attack_received(servidor, conn_socket):
    # Recebe a mensagem com o ataque
    rcv_msg = conn_socket.recv(2048)
    rcv_msg = rcv_msg.decode().split(" ")
    x = rcv_msg[0]
    y = int(rcv_msg[1])
    print("Attack received at {}, {}".format(x, y))

    # Verifica se o ataque acertou
    ans = servidor.check_hit_taken(x, y)
    if(ans):
        response = "Hit"
    else:
        response = 'Miss'

    # Devolve a resposta ao cliente com o resultado do ataque
    server_status = servidor.check_for_boats()
    conn_socket.send((response + ";" + str(server_status)).encode())

    # Espera um sinal do cliente avisando que o servidor pode prosseguir com o ataque
    if(server_status):
        signal = conn_socket.recv(2048)
    return not(server_status)


def send_attack(servidor, conn_socket):
    # Envia um ataque ao cliente
    x, y = servidor.get_attack()
    print("Fire at {}, {}".format(x, y))
    attack = x + " " + str(y)
    conn_socket.send(attack.encode())

    # Recebe o resultado do ataque
    rcv_msg = conn_socket.recv(2048)
    signal = "OK"
    if(rcv_msg.decode().split(";")[0] == "Hit"):
        servidor.hit(x, y)

        # Junto a mensagem de status do ataque também há uma mensagem de status do tabuleiro
        # Se a mensagem for True, quer dizer que ainda há navios no campo inimigo
        # Se a mensagem for False o jogo acaba
        client_status = rcv_msg.decode().split(";")[1]
        if(client_status == "True"):
            # Envia um sinal ao cliente avisando que ele pode fazer seu ataque
            conn_socket.send(signal.encode())
            return False
        else:
            print("Client lost!")
            return True

    elif(rcv_msg.decode().split(";")[0] == "Miss"):
        servidor.miss(x, y)
        # Envia um sinal ao cliente avisando que ele pode fazer seu ataque
        conn_socket.send(signal.encode())
        return False
    

def main():
    server_port = int(sys.argv[1])
    conn_socket = connection_setup(server_port)
    servidor = Servidor()

    game_over = False
    print("Game Started")
    while(not(game_over)):
        if(not(game_over)):
            game_over = attack_received(servidor, conn_socket)
        if(not(game_over)):
            game_over = send_attack(servidor, conn_socket)

    conn_socket.close()
    

if __name__ == "__main__":
    main()