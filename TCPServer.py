from threading import Thread
import socket
host = "127.0.0.1"
port = 59000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)
        
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message=message)
        except Exception as e:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} has left the chat room!".encode())
            aliases.remove(alias)
            break
        
def receive():
    while True:
        print("Server is runnig and Listening....")
        client,address = server.accept()
        print(client)
        print(f"Connection has been established with {str(address)}")
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        print("Received :",alias)
        aliases.append(alias)
        clients.append(client)
        print(f"The alias of this client is {alias}".encode('utf-8'))
        broadcast(f"{alias} has been connected to the chat room".encode())
        thread = Thread(target=handle_client,args=(client,))
        thread.start()
        
if __name__ == "__main__":
    receive()