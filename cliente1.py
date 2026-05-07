import socket
import threading
import sys

TAM_BUFFER = 1024
MAXIMO_MENSAJE = 900
HOST_POR_DEFECTO = '127.0.0.1'
PUERTO_POR_DEFECTO = 12345


def mostrar_mensaje_recibido(mensaje):
    mensaje = mensaje.strip()
    if mensaje.startswith('[USUARIOS]'):
        lista_usuarios = mensaje.replace('[USUARIOS]', '').strip()
        print(f'\n[LISTA DE USUARIOS] {lista_usuarios}\n>> ', end='', flush=True)
        return
    if mensaje.startswith('[SISTEMA]'):
        print(f'\n{mensaje}\n>> ', end='', flush=True)
        return
    print(f'\n{mensaje}\n>> ', end='', flush=True)


def recibir_mensajes(socket_cliente):
    try:
        while True:
            datos = socket_cliente.recv(TAM_BUFFER)
            if not datos:
                print('\n[SERVIDOR] Conexión cerrada.')
                break
            mostrar_mensaje_recibido(datos.decode('utf-8', errors='replace'))
    except Exception as error:
        print(f'\nError recibiendo mensajes: {error}')
    finally:
        try:
            socket_cliente.close()
        except Exception:
            pass
        sys.exit(0)


def enviar_mensajes(socket_cliente):
    try:
        while True:
            try:
                mensaje = input('>> ')
            except EOFError:
                mensaje = 'salir'

            if mensaje.lower() == 'salir':
                try:
                    socket_cliente.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                socket_cliente.close()
                sys.exit(0)

            if len(mensaje.encode('utf-8')) > MAXIMO_MENSAJE:
                print('Mensaje muy largo; será truncado.')
                mensaje = mensaje.encode('utf-8')[:MAXIMO_MENSAJE].decode('utf-8', errors='ignore')

            try:
                socket_cliente.sendall(mensaje.encode('utf-8'))
            except Exception as error:
                print(f'No se pudo enviar el mensaje: {error}')
                break
    finally:
        try:
            socket_cliente.close()
        except Exception:
            pass
        sys.exit(0)


def iniciar_cliente(host=HOST_POR_DEFECTO, puerto=PUERTO_POR_DEFECTO):
    try:
        socket_cliente = socket.create_connection((host, puerto), timeout=5)
    except Exception as error:
        print(f'No se pudo conectar al servidor: {error}')
        return

    try:
        nombre = input('Ingresa tu nombre: ').strip()[:32]
        if not nombre:
            print('Nombre inválido. Cerrando.')
            socket_cliente.close()
            return

        socket_cliente.sendall(nombre.encode('utf-8'))

        hilo_recibir = threading.Thread(
            target=recibir_mensajes,
            args=(socket_cliente,),
            daemon=True,
        )
        hilo_recibir.start()

        print('--- Conectado al Chat Grupal ---')
        enviar_mensajes(socket_cliente)
    except Exception as error:
        print(f'Error en cliente: {error}')
    finally:
        try:
            socket_cliente.close()
        except Exception:
            pass


if __name__ == '__main__':
    iniciar_cliente()