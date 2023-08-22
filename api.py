import socket
import time

# Configuration du serveur et du port socket
SERVER_ADDRESS = '10.0.0.4'  # Adresse IP ou nom d'hôte du serveur socket
SERVER_PORT = 5000  # Port du serveur socket

def send_link(link):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
            client_socket.sendall(link.encode())
            print(f"Link sent: {link}")
    except Exception as e:
        print(f"Error sending link: {e}")

def main():
    last_modified = 0

    while True:
        try:
            file_stats = None
            try:
                file_stats = os.stat('links.txt')
            except FileNotFoundError:
                pass

            if file_stats and file_stats.st_mtime > last_modified:
                last_modified = file_stats.st_mtime

                with open('links.txt', 'r') as file:
                    link = file.read().strip()
                    if link:
                        send_link(link)
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)

if __name__ == '__main__':
    main()
