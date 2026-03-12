import socket
import threading
import sys

def recibir_mensajes(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\n[SERVIDOR] Conexión cerrada.")
                break
            print(f"\n{data.decode()}\n>> ", end="")
        except:
            break

def enviar_mensajes(client_socket):
    while True:
        mensaje = input(">> ")
        if mensaje.lower() == 'salir':
            client_socket.close()
            sys.exit()
        client_socket.sendall(mensaje.encode())

def cliente():
    # MAÑANA: Cambia esto por la IP de tu compañera
    host = '192.168.218.179' 
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"No se pudo conectar al servidor: {e}")
        return

    nombre = input("Ingresa tu nombre : ")
    client_socket.sendall(nombre.encode())

    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(client_socket,), daemon=True)
    hilo_recibir.start()

    print("--- Conectado al Chat Grupal ---")
    enviar_mensajes(client_socket)

if __name__ == "__main__":
    cliente()