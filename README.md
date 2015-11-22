## Proyecto Juego RPG en Python

## Requerimientos

1. SO linux

2. Instalar libreria pygame:

        Sudo ape-get install python-pygame
3. Instalar libreria pyzmq:

        Sudo apt-get install libzmq-dev
     
        Sudo apt-get install python-zmq

## Modo de ejecucion

1. Ejecutar servidor con el numero de jugadores que se van a conectar (el servidor esperara todos los clientes antes de iniciar el juego):
    
        Python server5.py  2
2. Ejecutar Juego con un nombre de usuario cualquiera (no se pueden repetir nombres de usuario):
    
        Python Juego1.5.py username

# Problemas

1. detecta evento del mouse que crear errores en el juego
2. enemigos diferentes en cada juego (en desarrollo)
