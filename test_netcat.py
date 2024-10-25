import argparse
import socket
import sys
import threading

def handle_input(client_socket):
    while True:
        data = sys.stdin.readline()
        client_socket.sendall(data.encode())

def handle_output(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        sys.stdout.write(data.decode())

def netcat(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    input_thread = threading.Thread(target=handle_input, args=(client_socket,))
    output_thread = threading.Thread(target=handle_output, args=(client_socket,))

    input_thread.start()
    output_thread.start()

    input_thread.join()
    output_thread.join()

    client_socket.close()

def main():
    parser = argparse.ArgumentParser(description='Python Netcat Tool')
    parser.add_argument('-l', '--listen', action='store_true', help='Listen mode')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Port to connect or listen')
    parser.add_argument('host', type=str, help='Host to connect')

    args = parser.parse_args()

    if args.listen:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', args.port))
        server_socket.listen(1)
        client_socket, _ = server_socket.accept()
        handle_input(client_socket)
        handle_output(client_socket)
        server_socket.close()
    else:
        netcat(args.host, args.port)

if __name__ == '__main__':
    main()

