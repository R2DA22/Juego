## Proyecto Juego RPG en Python

## Requerimientos

1. SO linux

2. Instalar libreria pygame
     sudo ape-get install python-pygame
3. Instalar libreria pyzmq
     sudo apt-get install libzmq-dev
     sudo apt-get install python-zmq

## Modo de ejecucion

1. Ejecutar servidor con el numero de jugadores que se van a conectar (el servidor esperara todos los clientes antes de iniciar el juego)
    
     python server5.py  2
2. Ejecutar Juego con un nombre de usuario cualquiera (no se pueden repetir nombres de usuario)
    
     python Juego1.5.py username

# Problemas

1. detecta evento del mouse que crear errores en el juego
2. enemigos diferentes en cada juego (en desarrollo)
