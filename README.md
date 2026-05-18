# Chat cliente-servidor

## Descripción
Esta práctica implementa un chat grupal con sockets TCP en Python. El servidor acepta varias conexiones al mismo tiempo, pide un nombre de usuario a cada cliente y mantiene una lista de usuarios conectados para compartirla con todos.

## Integrantes y distribución
**Integrantes:**
- Frida Paulina Sepúlveda Becerra
- Roxana Irías Hernández
- Martha Elizabeth Castorena Rivera
- Pablo Alberto Reyes Gutiérrez

**Distribución:**
Cada integrante sube su archivo `.py` a GitHub para dejar evidencia de su parte del trabajo en el desarrollo del servidor y los clientes.

## Fecha de entrega
- Entrega de avance: 11 de mayo.

## Qué hace la aplicación
- Permite conectar varios clientes al mismo servidor.
- Cada cliente escribe su nombre al entrar.
- El servidor guarda una lista de usuarios conectados.
- Cuando alguien entra o sale, todos reciben un aviso.
- Cuando alguien envía un mensaje, se notifica a los demás usuarios.

## Archivos en el repositorio
* `servidor.py`: Atiende las conexiones y difunde mensajes.
* `servidor2.py`: Segunda versión o respaldo del servidor para el control de pruebas.
* `cliente1.py`: Cliente adicional para uno de los integrantes.
* `Cliente2.py`: Cliente preparado para conectarse a otra IP de red de forma remota.
* `cliente_3.py`: Cliente local para pruebas en la misma computadora.
* `cliente_Pablo.py`: Código de cliente con la evidencia de desarrollo de Pablo.
* `cliente_Roxana.py`: Código de cliente con la evidencia de desarrollo de Roxana.

## Requisitos
No necesitas instalar paquetes extra. Solo Python 3 y el módulo estándar `socket`.

## Cómo ejecutar
1. Abre una terminal en esta carpeta.
2. Ejecuta primero el servidor principal:

```bash
python servidor.py
Abre otra terminal y ejecuta un cliente local para pruebas:

Bash
python cliente_3.py
Si quieres conectar otro equipo de la red, utiliza el cliente configurado para IP externa:

Bash
python Cliente2.py
Qué debes escribir
Al iniciar el cliente, primero escribe tu nombre. Después puedes enviar mensajes libremente. Para salir, escribe salir.

Mensajes que muestra el sistema
[SISTEMA] Bienvenido, Nombre

[SISTEMA] Nombre se unió al chat.

[SISTEMA] Nombre se desconectó.

[USUARIOS] Ana, Luis, Pedro

Estructura lógica
El servidor mantiene una lista interna llamada usuarios_conectados. Ahí guarda el nombre, socket y dirección de cada cliente conectado. Con esa lista:

Muestra quién está conectado.

Envía avisos a todos.

Comparte la lista de usuarios cuando hay cambios.

Requisitos que cumple
Servidor y clientes

Múltiples conexiones

Nombre de usuario

Aviso de conexión

Servidor con lista de usuarios

Notificación de mensajes

Observación
Si el cliente remoto no conecta, revisa la dirección IP declarada dentro de Cliente2.py y cámbiala por la IP privada real de la máquina donde se está ejecutando el archivo servidor.py.
