# Mejoras del Chat Cliente-Servidor

## Objetivo
Simplificar un chat grupal donde una computadora actúa como servidor y varias se conectan como clientes sin historial previo; cada cliente recibe únicamente los mensajes enviados después de conectarse.

## Cambios en `servidor.py`
- Se usa una lista de clientes protegida con un `Lock` para evitar condiciones de carrera al agregar o eliminar conexiones.
- La función `broadcast` envía mensajes solo a los sockets activos y limpia automáticamente clientes caídos.
- Cada cliente se maneja en un hilo daemon que registra la conexión, reenvía los mensajes al resto y publica avisos de entrada/salida sin conservar historial previo.
- Se habilita `SO_REUSEADDR` para poder reiniciar rápido el servidor local.

## Cambios en `cliente_3.py`
- El hilo receptor imprime solo mensajes nuevos, detecta desconexiones y no muestra mensajes anteriores.
- El bucle principal se encarga de enviar mensajes y cerrar el socket cuando el usuario escribe `salir` o interrumpe el proceso.
- Se añade manejo de excepciones y un nombre predeterminado `Anonimo` para reforzar la robustez.

## Resultado
El chat ahora permite múltiples clientes en tiempo real, mantiene el servidor activo sin historial y minimiza el código repetitivo para facilitar la extensión o integración posterior.

## Pruebas y despliegue
- **Requisitos:** Python 3.8+ en cada máquina, red local con conexión TCP entre ellas (firewall abierto para el puerto 12345) y la IP del servidor conocida por los clientes.
- **Topología sugerida:** una máquina dedicada como servidor (que puede ejecutar `servidor.py`) más al menos tres dispositivos cliente que ejecuten `cliente_3.py`. Opcionalmente, uno de esos clientes puede correr también el servidor para permitir que la misma máquina reciba y envíe mensajes.
- **Paso a paso:**
	1. En la máquina que actuará como servidor, ejecutar `python servidor.py` y verificar el mensaje de escucha `Servidor escuchando en 0.0.0.0:12345`.
	2. Desde cada cliente ejecutar `python cliente_3.py`, ingresar un nombre y confirmar que aparece el aviso de conexión.
	3. Escribir mensajes desde cualquier cliente; el servidor retransmitirá cada línea al resto del grupo sin mostrar lo que se envió antes de unirse.
	4. Para permitir que el servidor también envíe mensajes, arrancar `cliente_3.py` en la misma máquina servidor y usar el nombre escogido para participar en el chat.
	5. Probar cierres inesperados (Ctrl+C o `salir`) y confirmar que los demás clientes reciben el aviso de desconexión y pueden seguir escribiendo.

Este procedimiento comprueba que el chat global funciona con varios dispositivos y que no se comparte ningún historial anterior.
