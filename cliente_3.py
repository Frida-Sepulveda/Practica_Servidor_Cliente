import socket
import threading

def recibir_mensajes(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\n[Servidor cerrado]\n")
                break
            print(f"\n{data.decode().strip()}\n>> ", end="")
        except (OSError, ConnectionResetError):
            break

def cliente(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except socket.error as exc:
        print(f"No se pudo conectar al servidor: {exc}")
        return

    nombre = input("Ingresa tu nombre: ").strip() or "Anonimo"
    client_socket.sendall(nombre.encode())

    threading.Thread(target=recibir_mensajes, args=(client_socket,), daemon=True).start()

    print("--- Conectado al Chat Grupal ---")
    try:
        while True:
            mensaje = input(">> ")
            if mensaje.lower() == 'salir':
                break
            client_socket.sendall(mensaje.encode())
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        client_socket.close()

if __name__ == "__main__":
    cliente()