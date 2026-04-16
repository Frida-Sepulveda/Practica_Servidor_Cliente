import socket
import threading
import sys

def recibir_mensajes(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            # Separamos el tipo de notificación por el pipe '|'
            partes = data.split('|')
            tipo = partes[0]
            contenido = partes[1]

            if tipo == "USUARIOS_CONECTADOS":
                print(f"\n[EN LÍNEA]: {contenido}")
            elif tipo == "SISTEMA":
                print(f"\n🔔 NOTIFICACIÓN: {contenido}")
            elif tipo == "MENSAJE":
                # Agregamos un carácter de campana \a para notificación sonora
                print(f"\a\n{contenido}") 
            
            print(">> ", end="", flush=True)
        except:
            print("\n[ERROR] Conexión perdida con el servidor.")
            break

def enviar_mensajes(client_socket):
    while True:
        mensaje = input(">> ")
        if mensaje.lower() == 'salir':
            client_socket.close()
            sys.exit()
        client_socket.sendall(mensaje.encode())

def cliente():
    # RECUERDA: Mañana en el ITL cambia '127.0.0.1' por la IP de Frida
    host = '127.0.0.1' 
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f"No se pudo conectar: {e}")
        return

    nombre = input("Ingresa tu nombre: ")
    client_socket.sendall(nombre.encode())

    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(client_socket,), daemon=True)
    hilo_recibir.start()

    print(f"--- Bienvenido {nombre}, estás en el Chat Grupal ---")
    enviar_mensajes(client_socket)

if __name__ == "__main__":
    cliente()