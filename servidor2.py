import socket
import threading

# Ahora usamos un diccionario para asociar el socket con el nombre del usuario
clientes = {} 

def enviar_lista_usuarios():
    """Envía a todos los clientes la lista actualizada de quiénes están conectados."""
    lista_nombres = ", ".join(clientes.values())
    mensaje_lista = f"USUARIOS_CONECTADOS|{lista_nombres}".encode()
    for sock in clientes.keys():
        try:
            sock.sendall(mensaje_lista)
        except:
            pass

def broadcast(mensaje, conn_origen):
    """Envía un mensaje a todos excepto al que lo originó."""
    for sock in clientes.keys():
        if sock != conn_origen:
            try:
                sock.sendall(mensaje)
            except:
                # Si falla, el cliente se desconectó
                eliminar_cliente(sock)

def eliminar_cliente(conn):
    """Limpia el diccionario cuando alguien se va."""
    if conn in clientes:
        nombre = clientes[conn]
        print(f"{nombre} se desconectó.")
        del clientes[conn]
        conn.close()
        broadcast(f"SISTEMA|{nombre} ha salido del chat.".encode(), None)
        enviar_lista_usuarios()

def manejar_cliente(conn, addr):
    try:
        # Lo primero que recibimos es el nombre
        nombre = conn.recv(1024).decode()
        clientes[conn] = nombre
        print(f"{nombre} se conectó desde {addr}")

        # Avisos de conexión y actualización de lista
        broadcast(f"SISTEMA|{nombre} se unió al chat.".encode(), conn)
        enviar_lista_usuarios()

        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # Formateamos el mensaje con el nombre y una etiqueta de notificación
            mensaje_full = f"MENSAJE|{nombre}: {data.decode()}"
            print(mensaje_full)
            broadcast(mensaje_full.encode(), conn)

    except:
        pass
    finally:
        eliminar_cliente(conn)

def servidor():
    host = '0.0.0.0'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Servidor API de Chat escuchando en {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        # El registro se hace dentro de manejar_cliente tras recibir el nombre
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()

if __name__ == "__main__":
    servidor()