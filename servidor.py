import socket
import threading

clientes = []

def broadcast(mensaje, conn_origen):
    for cliente in clientes:
        if cliente != conn_origen:
            try:
                cliente.sendall(mensaje)
            except:
                clientes.remove(cliente)

def manejar_cliente(conn, addr):
    nombre = conn.recv(1024).decode()
    print(f"{nombre} se ha conectado desde {addr}")

    mensaje_bienvenida = f"{nombre} se unió al chat\n".encode()
    broadcast(mensaje_bienvenida, conn)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            mensaje = f"{nombre}: {data.decode()}"
            print(mensaje)

            broadcast(mensaje.encode(), conn)

        except:
            break

    print(f"{nombre} se desconectó")
    clientes.remove(conn)
    conn.close()

def servidor():
    host = '0.0.0.0'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Servidor escuchando en {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        clientes.append(conn)

        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()

if __name__ == "__main__":
    servidor()