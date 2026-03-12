import socket
import threading

clientes = []
clientes_lock = threading.Lock()

def broadcast(mensaje, excluded=None):
    with clientes_lock:
        for cliente in clientes[:]:
            if cliente is excluded:
                continue
            try:
                cliente.sendall(mensaje)
            except (OSError, ConnectionResetError):
                clientes.remove(cliente)
                cliente.close()

def manejar_cliente(conn, addr):
    with conn:
        nombre = conn.recv(1024).decode().strip()
        if not nombre:
            return

        print(f"{nombre} se ha conectado desde {addr}")
        with clientes_lock:
            clientes.append(conn)

        broadcast(f"{nombre} se unió al chat\n".encode(), excluded=conn)

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                mensaje = f"{nombre}: {data.decode()}"
                print(mensaje)
                broadcast(mensaje.encode(), excluded=conn)
            except (OSError, ConnectionResetError):
                break

        with clientes_lock:
            if conn in clientes:
                clientes.remove(conn)

        broadcast(f"{nombre} se desconectó\n".encode(), excluded=conn)
        print(f"{nombre} se desconectó")

def servidor():
    host = '0.0.0.0'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Servidor escuchando en {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
        hilo.start()

if __name__ == "__main__":
    servidor()