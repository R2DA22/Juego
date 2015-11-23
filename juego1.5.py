import pygame,sys,time,random
from pygame.locals import *
import zmq
import math
import json
import GIFImage


class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    def posicion(self):
        self.left,self.top=pygame.mouse.get_pos()

class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1, imagen2,x,y):
        self.imagen_normal= imagen1
        self.imagen_seleccion= imagen2
        self.imagen_actual=self.imagen_normal
        self.rect=self.imagen_actual.get_rect()
        self.rect.left,self.rect.top=x,y

    def accion(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual= self.imagen_seleccion
        else:
            self.imagen_actual=self.imagen_normal
        pantalla.blit(self.imagen_actual,self.rect)



    

def seleccionar_personaje(cursor):
    fondo=pygame.image.load("objetos/seleccion.png")
    img1=pygame.image.load("objetos/pj1.png")
    img2=pygame.image.load("objetos/pj2.png")
    img3=pygame.image.load("objetos/pj3.png")
    seleccionar1= pygame.image.load("objetos/botones/3.png")
    seleccionar12= pygame.image.load("objetos/botones/3.3.png")
    seleccionar2= pygame.image.load("objetos/botones/3.png")
    seleccionar22= pygame.image.load("objetos/botones/3.3.png")
    seleccionar3= pygame.image.load("objetos/botones/3.png")
    seleccionar32= pygame.image.load("objetos/botones/3.3.png")
    salir1= pygame.image.load("objetos/botones/2.png")
    salir2= pygame.image.load("objetos/botones/2.2.png")
    boton1= Boton(seleccionar1,seleccionar12,160,450)
    boton2= Boton(seleccionar2,seleccionar22,396,450)
    boton3= Boton(seleccionar3,seleccionar32,630,450)
    boton6= Boton(salir1,salir2,800,550)

    cerrar= False

    while not cerrar:
        tecla= pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==QUIT:
                cerrar=True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton1.rect):
                    pygame.mixer.music.stop()
                    Game(2)
                elif cursor.colliderect(boton2.rect):
                    pygame.mixer.music.stop()
                    Game(0)
                elif cursor.colliderect(boton3.rect):
                    pygame.mixer.music.stop()
                    Game(1)
                if cursor.colliderect(boton6.rect):
                    cerrar=True
                
        cursor.posicion()
        PANTALLA.blit(fondo,(0,0))
        PANTALLA.blit(img1,(110,150))
        PANTALLA.blit(img2,(346,150))
        PANTALLA.blit(img3,(582,150))
        boton1.accion(PANTALLA,cursor)
        boton2.accion(PANTALLA,cursor)
        boton3.accion(PANTALLA,cursor)
        boton6.accion(PANTALLA,cursor)
        pygame.display.flip()

    pygame.quit()



def inicio():
    fondo=pygame.image.load("objetos/inicio.png")
    jugar1= pygame.image.load("objetos/botones/1.png")
    jugar2= pygame.image.load("objetos/botones/1.1.png")
    salir1= pygame.image.load("objetos/botones/2.png")
    salir2= pygame.image.load("objetos/botones/2.2.png")
    cursor= Cursor()
    boton1= Boton(jugar1,jugar2,700,100)
    boton2= Boton(salir1,salir2,700,200)

    cerrar= False

    while not cerrar:
        tecla= pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==QUIT:
                cerrar=True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton1.rect):
                    seleccionar_personaje(cursor)
                if cursor.colliderect(boton2.rect):
                    cerrar=True
                
        cursor.posicion()
        PANTALLA.blit(fondo,(0,0))
        boton1.accion(PANTALLA,cursor)
        boton2.accion(PANTALLA,cursor)
        pygame.display.flip()
    pygame.quit()
    


class Objetosinvi (pygame.sprite.Sprite):
    def __init__(self,x,y,objeto):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("objetos/"+objeto+".png")
        self.posx= x
        self.posy= y
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y= self.posx,self.posy
       
class Objetos (pygame.sprite.Sprite):
    def __init__(self,x,y,objeto):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("objetos/"+str(objeto)+".png")
        self.posx= x
        self.posy= y
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y= self.posx,self.posy

class Fondos (pygame.sprite.Sprite):
    def __init__(self,x,y,fondo):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("fondos/"+str(fondo)+".png")
        self.posx= x
        self.posy= y
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y= self.posx,self.posy
        self.fondo=fondo
        
    def Cambiomapa(self,x,y,fondo):
        self.image=pygame.image.load("fondos/"+str(fondo)+".png")

class Jugador(pygame.sprite.Sprite):
    def __init__(self,nombre,direc,x,y,fondo,personaje):
        pygame.sprite.Sprite.__init__(self)
        self.nombre=nombre
        self.salud=100
        self.vida=self.salud
        self.manatotal=100
        self.mana=self.manatotal
        self.x=x
        self.y=y
        self.i=1
        self.iy=1
        self.direc=direc
        self.pasos=20
        self.pasosy=10
        self.Pj= pygame.image.load("Personajes/"+str(personaje)+"/frontal/"+str(self.i)+".png")
        self.animacionsalto=False
        self.animacion=False
        self.personaje=personaje
        self.image=self.Pj
        self.ancho_image,self.alto_image= self.image.get_size()
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=self.x,self.y
        self.direcchoque=0
        self.choque=False
        self.fondo=fondo
        self.choqueobjetos=False
        self.copia=self.personaje
        self.gastarmana=False
        self.dano=5
        self.nombreinterfas=Nombre()
        self.manainterfas=Mana()
        self.vidainterfas=Vida()

    def chocar(self,ob):
        self.pasos=20
        for col in ob:
            if pygame.sprite.collide_rect(self,col):              
                if col.direc==4 and (self.direc==4 or self.direc==2 or self.direc==8):
                    self.pasos=20
                    if(self.animacion):
                     col.vida=col.vida-self.dano

                elif col.direc==6 and (self.direc==6 or self.direc==2 or self.direc==8):
                    self.pasos=20
                    if(self.animacion):
                     col.vida=col.vida-self.dano

                elif col.direc==8 and (self.direc==4 or self.direc==8 or self.direc==6):
                    self.pasos=20
                    if(self.animacion):
                     col.vida=col.vida-self.dano

                elif col.direc==2 and (self.direc==4 or self.direc==2 or self.direc==6):
                    self.pasos=20
                    if(self.animacion):
                     col.vida=col.vida-self.dano

                else:
                    self.pasos=0
                    if(self.animacion):
                     col.vida=col.vida-self.dano
           
    def chocarpbjetos(self,ob):
        activado=True
        for col in ob:
            if pygame.sprite.collide_rect(self,col):
                if self.direc==8 and activado:
                    self.y=self.y+25
                    activado=False
                    
                if self.direc==2 and activado:
                    self.y=self.y-25
                    activado=False
                    
                if self.direc==6 and activado:
                    self.x=self.x-25
                    activado=False

                if self.direc==4 and activado:
                    self.x=self.x+25
                    activado=False

                self.rect.x=self.x
                self.rect.y=self.y
                self.image=self.Pj

    def perdidavida(self):
      if(self.vida <= self.salud-10):
        self.vida=self.vida-10

    def perdidamana(self):
        self.mana=self.mana-10

    def aumentovida(self):
        if(self.vida <= self.salud-10):
            self.vida=self.vida+10
            self.perdidamana()
        else:
            self.perdidamana()

    def aumentomana(self):
        if(self.mana <= self.manatotal-10):
            self.vida=self.mana+10

    def moverizquierda(self,socket_server,username):
          if(10>=self.i):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterali/"+str(self.i)+".png")
            self.x-=self.pasos
            self.i+=1
            self.direc=4
          else: self.i=1
          self.rect.x=self.x
          self.rect.y=self.y
          self.image=self.Pj
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"vida":self.vida,"personaje":self.personaje,"dano":self.dano,"gastarmana":self.gastarmana,"carpeta":"laterali","bandera":True}
          socket_server.send_multipart(["move",json.dumps(dic,sort_keys=True)])
         
    def moverderecha(self,socket_server,username):
          if(10>=self.i):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterald/"+str(self.i)+".png")
            self.x+=self.pasos
            self.i+=1
            self.direc=6
          else: self.i=1
          self.rect.x=self.x
          self.rect.y=self.y
          self.image=self.Pj
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"vida":self.vida,"personaje":self.personaje,"dano":self.dano,"gastarmana":self.gastarmana,"carpeta":"laterald","bandera":True}
          socket_server.send_multipart(["move",json.dumps(dic,sort_keys=True)])

    def moverarriba(self,socket_server,username):
          if(10>=self.i):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/trasera/"+str(self.i)+".png")
            self.y-=self.pasos
            self.i+=1
            self.direc=8
          else: self.i=1
          self.rect.x=self.x
          self.rect.y=self.y
          self.image=self.Pj
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"vida":self.vida,"personaje":self.personaje,"dano":self.dano,"gastarmana":self.gastarmana,"carpeta":"trasera","bandera":True}
          socket_server.send_multipart(["move",json.dumps(dic,sort_keys=True)])

    def moverabajo(self,socket_server,username):
          if(10>=self.i):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/frontal/"+str(self.i)+".png")
            self.y+=self.pasos
            self.i+=1
            self.direc=2
          else: self.i=1
          self.rect.x=self.x
          self.rect.y=self.y
          self.image=self.Pj
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"vida":self.vida,"personaje":self.personaje,"dano":self.dano,"gastarmana":self.gastarmana,"carpeta":"frontal","bandera":True}
          socket_server.send_multipart(["move",json.dumps(dic,sort_keys=True)])


    def Horienta(self):

         if(self.direc==4):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterali/0.png")
            carpeta="laterali"

         if(self.direc==6):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterald/0.png")
            carpeta="laterald"

         if(self.direc==8):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/trasera/0.png")
            carpeta="trasera"

         if(self.direc==2):
            self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/frontal/0.png")
            carpeta="frontal"

         if(self.direc==3):
           self.Pj= pygame.image.load("diagonal_id/"+str(0)+".png")

         if(self.direc==1):
           self.Pj= pygame.image.load("diagonal_ii/"+str(0)+".png")

         if(self.direc==9):
           self.Pj= pygame.image.load("diagonal_sd/"+str(0)+".png")

         if(self.direc==7):
           self.Pj= pygame.image.load("diagonal_si/"+str(0)+".png")

         self.rect.x=self.x
         self.rect.y=self.y
         self.image=self.Pj
         #dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":0,"vida":self.vida,"personaje":self.personaje,"dano":self.dano,"gastarmana":self.gastarmana,"carpeta":carpeta,"bandera":True}         
         #socket_server.send_multipart(["move",json.dumps(dic,sort_keys=True)])

    def interfase(self):
         propiedades= pygame.sprite.Group()
         self.vidainterfas.vid(self.vida,self.rect.x,self.rect.y)
         self.manainterfas.man(self.mana,self.rect.x,self.rect.y)
         self.nombreinterfas.nom(self.nombre,self.rect.x,self.rect.y)
         propiedades.add(self.vidainterfas)
         propiedades.add(self.manainterfas)
         propiedades.add(self.nombreinterfas)
         return propiedades
        
    def anima(self,ani):
        self.animacion=True
        if(self.direc==8):
            if(self.direc==8 and self.iy<=10):
                self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/trasero/"+str(self.iy)+".png")
                self.iy=self.iy+1
            else:
             self.iy=1
             self.animacion=False

        if(self.direc==2):
            if(self.direc==2 and self.iy<=10):
                self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/frontal/"+str(self.iy)+".png")
                self.iy=self.iy+1
            else:
                self.iy=1
                self.animacion=False

        if(self.direc==4 ):
            if(self.direc==4 and self.iy<=10):
             self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/laterali/"+str(self.iy)+".png")
             self.iy=self.iy+1
            else:
                self.iy=1
                self.animacion=False

        if(self.direc==6 ):
            if(self.direc==6 and self.iy<=10):
             self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/laterald/"+str(self.iy)+".png")
             self.iy=self.iy+1
            else:
                self.iy=1
                self.animacion=False
        self.rect.x=self.x
        self.rect.y=self.y
        self.image=self.Pj

class Enemigo(pygame.sprite.Sprite):
    def __init__(self,nombre,direc,x,y,cx,cy,peligro,dano,vida,mana,personaje):
        pygame.sprite.Sprite.__init__(self)
        self.nombre=nombre
        self.vida=vida
        self.mana=mana
        self.x=x
        self.y=y
        self.Cx=cx
        self.Cy=cy
        self.xaux=x
        self.yaux=y
        self.i=1
        self.direc=direc
        self.pasos=5
        self.dano=dano

        if(direc==4):
         self.Pj=pygame.image.load("Personajes/"+str(personaje)+"/laterali/"+str(0)+".png")
        if(direc==2):
         self.Pj=pygame.image.load("Personajes/"+str(personaje)+"/frontal/"+str(0)+".png")
        if(direc==6):
         self.Pj=pygame.image.load("Personajes/"+str(personaje)+"/laterald/"+str(0)+".png")
        if(direc==8):
         self.Pj=pygame.image.load("Personajes/"+str(personaje)+"/trasera/"+str(0)+".png")

        self.Peligro=peligro
        self.iy=1
        self.animacion=True
        self.personaje=personaje
        self.image=self.Pj
        self.ancho_image,self.alto_image= self.image.get_size()
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=self.x,self.y
        self.choque=True
        self.ataca=False
        self.bajarvida=0
        self.nombreinterfas=Nombre()
        self.manainterfas=Mana()
        self.vidainterfas=Vida()


    def atacar(self,jugador):
        self.anima(self.personaje)
        self.ataca=True

    def distancia(self,jugadorx,jugadory):
        aux=math.sqrt(math.pow((jugadorx-self.x),2)+math.pow((jugadory-self.y),2))
        return aux        

    def interfase(self):
         propiedades= pygame.sprite.Group()
         self.vidainterfas.vid(self.vida,self.rect.x,self.rect.y)
         self.manainterfas.man(self.mana,self.rect.x,self.rect.y)
         self.nombreinterfas.nom(self.nombre,self.rect.x,self.rect.y)
         propiedades.add(self.vidainterfas)
         propiedades.add(self.manainterfas)
         propiedades.add(self.nombreinterfas)
         return propiedades

    def perseguir(self,jugadorx,jugadory,direc):
            if(jugadorx<self.x):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterali/"+str(self.i)+".png")
                    self.x-=self.pasos
                    self.i+=1
                    self.direc=4
                  else: self.i=1

            if(jugadorx>self.x):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterald/"+str(self.i)+".png")
                    self.x+=self.pasos
                    self.i+=1
                    self.direc=6
                  else: self.i=1

            if(jugadory>self.y):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/frontal/"+str(self.i)+".png")
                    self.y+=self.pasos
                    self.i+=1
                    self.direc=2
                  else: self.i=1

            if(jugadory<self.y):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/trasera/"+str(self.i)+".png")
                    self.y-=self.pasos
                    self.i+=1
                    self.direc=8
                  else: self.i=1
            self.rect.x=self.x
            self.rect.y=self.y
            self.image=self.Pj

    def rutina(self):
            if((self.xaux-self.Cx<=self.x  and  self.yaux<=self.y) or (self.yaux-self.Cy<=self.y and self.xaux-self.Cx>=self.x  ) or (self.yaux-self.Cy>=self.y and self.xaux>=self.x  ) or (self.xaux <= self.x and self.yaux>=self.y )):

              if(self.xaux-self.Cx<=self.x  and  self.yaux<=self.y):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterali/"+str(self.i)+".png")
                    self.x-=self.pasos
                    self.i+=1
                    self.direc=4
                  else: self.i=1

              if(self.yaux-self.Cy<=self.y and self.xaux-self.Cx>=self.x  ):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/trasera/"+str(self.i)+".png")
                    self.y-=self.pasos
                    self.i+=1
                    self.direc=8
                  else: self.i=1

              if(self.yaux-self.Cy>=self.y and self.xaux>=self.x  ):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterald/"+str(self.i)+".png")
                    self.x+=self.pasos
                    self.i+=1
                    self.direc=6
                  else: self.i=1

              if(self.xaux <= self.x and self.yaux>=self.y ):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/frontal/"+str(self.i)+".png")
                    self.y+=self.pasos
                    self.i+=1
                    self.direc=2
                  else: self.i=1

            else:
              if(self.xaux<=self.x ):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterali/"+str(self.i)+".png")
                    self.x-=self.pasos
                    self.i+=1
                    self.direc=4
                  else: self.i=1

              elif(self.yaux>=self.y):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/frontal/"+str(self.i)+".png")
                    self.y+=self.pasos
                    self.i+=1
                    self.direc=2
                  else: self.i=1

              elif(self.xaux>=self.x):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/laterald/"+str(self.i)+".png")
                    self.x+=self.pasos
                    self.i+=1
                    self.direc=6
                  else: self.i=1

              elif(self.yaux<=self.y  ):
                  if(10>=self.i):
                    self.Pj= pygame.image.load("Personajes/"+str(self.personaje)+"/trasera/"+str(self.i)+".png")
                    self.y-=self.pasos
                    self.i+=1
                    self.direc=8
                  else: self.i=1
            self.rect.x=self.x
            self.rect.y=self.y
            self.image=self.Pj
          
    def anima(self,ani):
        self.animacion=True
        self.bajarvida=0
        if(self.direc==2):
            if(self.direc==2 and self.iy<=10):
                self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/frontal/"+str(self.iy)+".png")
                self.iy=self.iy+1
                self.direc=2
            else:
             self.iy=1
             self.animacion=False
             self.direc=2
             self.bajarvida=1

        if(self.direc==8):
            if(self.direc==8 and self.iy<=10):
                self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/trasero/"+str(self.iy)+".png")
                self.iy=self.iy+1
                self.direc=8
            else:
                self.iy=1
                self.animacion=False
                self.direc=8
                self.bajarvida=1

        if(self.direc==4 ):
            if(self.direc==4 and self.iy<=10):
             self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/laterali/"+str(self.iy)+".png")
             self.iy=self.iy+1
             self.direc=4
            else:
                self.iy=1
                self.animacion=False
                self.direc=4
                self.bajarvida=1

        if(self.direc==6 ):
            if(self.direc==6 and self.iy<=10):
             self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/laterald/"+str(self.iy)+".png")
             self.iy=self.iy+1
             self.direc=6
            else:
                self.iy=1
                self.animacion=False
                self.direc=6
                self.bajarvida=1
                
        self.rect.x=self.x
        self.rect.y=self.y
        self.image=self.Pj
        
    def __del__(self):
        print("muerto")

class Vida (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.display.set_caption("Modulo de fuentes")
        fuente =pygame.font.SysFont("Arial", 30)
        texto1 = fuente.render("",0,(255, 0, 0))
        self.image=texto1
        self.rect=self.image.get_rect()
        
    def vid(self,vida,x,y):
        pygame.display.set_caption("Modulo de fuentes")
        fuente =pygame.font.SysFont("Arial", 20)
        texto2 = fuente.render(str(vida),0,(255, 0, 0))
        self.image=texto2
        self.rect.x=x
        self.rect.y=y
        self.vida=vida
        
class Mana (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.display.set_caption("Modulo de fuentes")
        fuente =pygame.font.SysFont("Arial", 30)
        texto1 = fuente.render("",0,(255, 0, 0))
        self.image=texto1
        self.rect=self.image.get_rect()
        
    def man(self,vida,x,y):
        pygame.display.set_caption("Modulo de fuentes")
        fuente =pygame.font.SysFont("Arial", 20)
        texto2 = fuente.render(str(vida),0,(255, 255, 0))
        self.image=texto2
        self.rect.x=x+110
        self.rect.y=y
        
class Nombre (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.display.set_caption("Modulo de fuentes")
        fuente =pygame.font.SysFont("Arial", 30)
        texto1 = fuente.render("",0,(255, 255, 0))
        self.image=texto1
        self.rect=self.image.get_rect()
        
    def nom(self,vida,x,y):
        pygame.display.set_caption("Modulo de fuentes")
        fuente =pygame.font.SysFont("Arial", 20)
        texto2 = fuente.render(str(vida),0,(255, 0, 255))
        self.image=texto2
        self.rect.x=x+50
        self.rect.y=y-30


class AnimacionMapa (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


        
    def Goanimacion(self,players,enemigos,jugadores,objetos,retornar,nombre_vida_mana):
        
       #CARGAR ELEMENTOS DEL MAPA EN CUESTION
        retornar.add(objetos)     
        retornar.add(enemigos)
        bandera2=1
        aux=0
        iterador=0
        index=0
        bandera=0
       #INTERFAS VIDA MANA NOMBRE
        for col in enemigos:
            nombre_vida_mana.add(col.interfase())
            retornar.add(nombre_vida_mana)
        #SI SE DESTRUYE UN ENEMIGO SAQUELO DE LISTA ENEMIGOS LISTA MAPA Y QUITE LA INTERFAS
            if(col.vida<=0):
                retornar.remove(col)
                enemigos.remove(col)
                retornar.remove(col.interfase())
                nombre_vida_mana.remove(col.interfase()) 
        #COLICION ENEMIGOS CON JUGADORES
            for jugador in jugadores:
          #SI JUGADOR ESTA COLISIONANDO CON ENEMIGO 
                if pygame.sprite.collide_rect(col,jugador):    
                    col.atacar(jugador)
                    bandera2=1
                    bandera=1
                    if(col.bajarvida):
                        jugador.vida=jugador.vida-col.dano
                elif(jugador.x+col.Peligro>col.x and jugador.y+col.Peligro>col.y and jugador.y<col.y+col.Peligro and jugador.x<col.x+col.Peligro ): 
                        temp=col.distancia(jugador.x,jugador.y)
                        if aux==0: 
                            aux=temp
                            index=jugador.personaje
                        elif temp < aux:
                            aux=temp
                            index=jugador.personaje
                        bandera2=0
                        bandera=1   
            
            if bandera2==0:                      
                for jugador in jugadores:
                    if jugador.personaje == index:
                        atacar_jugador=players[jugador.nombre]        
                col.perseguir(atacar_jugador.x,atacar_jugador.y,atacar_jugador.direc)
            if bandera==0:
                col.choque=True
                col.rutina()
                col.ataca=False
               
            
            
         
             

        #COLICION JUGADORES CON ENEMIGOS
        for jugador in jugadores:
         jugador.chocar(enemigos)   
        #COLICION JUGADORES CON OBJETOS
         jugador.chocarpbjetos(objetos)
         

        return retornar

    def KillAnimacion(self,enemigos,objetos,retornar,nombre_vida_mana):
         retornar.remove(enemigos)
         retornar.remove(objetos)
         retornar.remove(nombre_vida_mana)
         return retornar

def manejo_mapas(fondo,player,x,y,fondo_aux,socket_server):
    fondo.Cambiomapa(-330,0,fondo_aux)
    player.x=x
    player.y=y
    player.fondo=fondo_aux
    fondo.fondo=fondo_aux
    dic={"mapa":fondo_aux,"username":player.nombre,"bandera":False}
    socket_server.send_multipart(["mapeo",json.dumps(dic,sort_keys=True)])

def Metamorfosis(player,personaje,dano,gastarmana):
    players[username].personaje=personaje
    players[username].dano=players[username].dano+dano
    players[username].gastarmana =gastarmana  


def from_server(action,player,username,dic1): 
	if  dic1["bandera"]:
		if player.nombre != username:
			if(dic1["i"] <= 10):  
				player.i=dic1["i"]
			else:
				player.i=1
			player.Pj= pygame.image.load("Personajes/"+str(dic1["personaje"])+"/"+dic1["carpeta"]+"/"+str(player.i)+".png")
			player.rect.x=dic1["posx"]
			player.rect.y=dic1["posy"]
			player.x=dic1["posx"]
			player.y=dic1["posy"]
			player.direc=dic1["direc"]
			player.dano=dic1["dano"]
			player.vida=dic1["vida"]
			player.gastarmana=dic1["gastarmana"]
			player.personaje=dic1["personaje"]
			player.image=player.Pj
			if action == "golpe":
				player.anima(player.personaje)
	else:
		player.fondo=dic1["mapa"]








#_________________________________________INICIO DEL JUEGO_______________________________________
def Game(n):

  init =False
  players={}
  #____________________________________________________________Establecer conexion con el servidor
  ctx = zmq.Context()
  socket_server = ctx.socket(zmq.XREQ)
  socket_server.connect('tcp://localhost:5555')

  msg="connect"
  username=sys.argv[1]
  socket_server.send_multipart([msg,username,json.dumps(n,sort_keys=True)])
  poller = zmq.Poller()
  poller.register(socket_server, zmq.POLLIN)
  ANCHO = int(1000)
  ALTO = int(700)
  pygame.init()
  pygame.key.set_repeat(1,50)
  PANTALLA= pygame.display.set_mode([ANCHO,ALTO])
  #MAPEO
  mapeo= pygame.sprite.Group()
  jugadores= pygame.sprite.Group()
  nombre_vida_manajugador= pygame.sprite.Group()
  terminar= False
  fondo=pygame.image.load("fondos/fondoEspera.png")
  c = GIFImage.GIFImage("fondos/buscando.gif")
  PANTALLA.blit(fondo,(0,0))
  while not terminar:
    
    if not init:
     for event in pygame.event.get():
           if event.type == QUIT:
                pygame.quit()
                return
     c.render(PANTALLA, (350, 200))
     pygame.display.flip()
    socks = dict(poller.poll(1))
    if socket_server in socks and socks[socket_server] == zmq.POLLIN:
      j=0
      action=socket_server.recv()
      if action=="connect":
          number_players=int(socket_server.recv())
          while j<number_players:
            dic=json.loads(socket_server.recv())
            jugador_temp=Jugador(dic["username"],dic["direc"],dic["x"],dic["y"],dic["fondo"],dic["personaje"])
            players[dic["username"]]=jugador_temp
            jugadores.add(jugador_temp)
            mapeo.add(jugador_temp)
            nombre_vida_manajugador.add(jugador_temp.interfase())
            mapeo.add(nombre_vida_manajugador)
            j+=1
          init=True

          #INICIALIZARPERSONAJEPRINCIPAL
          AnimacionMapas=AnimacionMapa()
          #MAPA1_____________________________________________________________INICIOMAPA1
          enemigos=pygame.sprite.Group()
          objetos=pygame.sprite.Group()

          #__________________ENEMIGOS

          enemigo=Enemigo("Ronal",8,200,400,100,100,250,1,100,100,0)
          enemigos.add(enemigo)
          mapeo.add(enemigos)

          #___________________OBJETOS 
          ob1= Objetosinvi(850,550,"150-150")
          ob2= Objetosinvi(700,580,"150-150")
          ob3= Objetosinvi(550,600,"150-150")
          ob4= Objetosinvi(400,620,"150-150")
          ob5= Objetosinvi(-30,620,"150-150")
          ob6= Objetosinvi(-30,550,"150-150")
          ob7= Objetosinvi(300,-70,"50-50")
          ob8= Objetosinvi(400,-80,"150-150")
          ob9= Objetosinvi(840,190,"50-50")
          ob10= Objetosinvi(460,260,"10-10")

          objetos.add(ob1)
          objetos.add(ob2)
          objetos.add(ob3)
          objetos.add(ob4)
          objetos.add(ob5)
          objetos.add(ob6)
          objetos.add(ob7)
          objetos.add(ob8)
          objetos.add(ob9)
          objetos.add(ob10)

          mapeo.add(objetos)
          #_________________________________________________________________FIN DE MAPA 1

          #MAPA 2___________________________________________________________INICIO MAPA 2
          enemigos2= pygame.sprite.Group()
          objetos1=pygame.sprite.Group()

          #__________________ENEMIGOS
          enemigo=Enemigo("Ronal",8,200,400,100,100,100,1,100,100,0)
          enemigo1=Enemigo("Reinosa",2,400,400,400,300,250,1,100,100,0)
          enemigo2=Enemigo("Cristian",6,500,500,400,400,200,1,100,100,0)
          enemigo3=Enemigo("Risitas",4,400,500,400,400,150,1,100,100,0)
          enemigo4=Enemigo("Ronal",8,550,530,400,400,100,1,100,100,0)

          enemigos2.add(enemigo)
          enemigos2.add(enemigo1)
          enemigos2.add(enemigo2)
          enemigos2.add(enemigo3)
          enemigos2.add(enemigo4)


          #___________________OBJETOS

          #____________________________________________________________________FINDEMAPA2



          #MAPA3___________________________________________________________INICIOMAPA3
          enemigos3=pygame.sprite.Group()

          #__________________ENEMIGOS
          enemigo=Enemigo("Ronal",8,200,400,100,100,100,1,100,100,1)
          enemigo1=Enemigo("Reinosa",2,400,400,400,400,250,1,100,100,1)
          enemigo2=Enemigo("Cristian",6,400,500,300,400,200,1,100,100,1)
          enemigo3=Enemigo("Risitas",4,400,600,400,400,150,1,100,100,1)
          enemigo4=Enemigo("Ronal",8,500,300,200,200,100,1,100,100,1)

          enemigos3.add(enemigo)
          enemigos3.add(enemigo1)
          enemigos3.add(enemigo2)
          enemigos3.add(enemigo3)
          enemigos3.add(enemigo4)


          #___________________OBJETOS

          #____________________________________________________________________FINDEMAPA3




          #MAPA4_______________________________________________________________INICIOMAPA4
          enemigos4=pygame.sprite.Group()
          objetos2=pygame.sprite.Group()

          #__________________ENEMIGOS
          enemigo=Enemigo("ELPODEROSOYPITUDOBOSFINAL",8,500,450,400,400,200,5,1000,100,3)

          enemigos4.add(enemigo)


          #___________________OBJETOS


          #______________________________________________________________________FINDEMAPA4


          #MAPA5___________________________________________________________INICIOMAPA5
          enemigos5=pygame.sprite.Group()

          #__________________ENEMIGOS
          enemigo=Enemigo("Ronal",8,200,300,100,100,100,1,100,100,2)
          enemigo1=Enemigo("Reinosa",2,600,300,500,300,250,1,100,100,2)
          enemigo2=Enemigo("Cristian",6,400,400,300,400,200,1,100,100,2)
          enemigo3=Enemigo("Risitas",4,400,500,400,400,150,1,100,100,2)
          enemigo4=Enemigo("Ronal",8,500,200,200,200,100,1,100,100,2)

          enemigos5.add(enemigo)
          enemigos5.add(enemigo1)
          enemigos5.add(enemigo2)
          enemigos5.add(enemigo3)
          enemigos5.add(enemigo4)


          #___________________OBJETOS

          #FONDOINICIAL
          fondos=pygame.sprite.Group()
          fondo=Fondos(-330,0,1)
          fondos.add(fondo)


          #INTERFASVIDAMANA NOMBRE
          nombre_vida_mana3= pygame.sprite.Group()
          nombre_vida_mana2= pygame.sprite.Group()
          nombre_vida_mana1= pygame.sprite.Group()
          nombre_vida_mana= pygame.sprite.Group()
          nombre_vida_mana4 = pygame.sprite.Group()

          #INICIO MUSICA FONDO
          pygame.mixer.music.load("musica/2.mp3")
          pygame.mixer.music.play(-1)
          sumatoria =0
          perdimana =0
          
      if action== "move" or action=="mapeo"  or action=="golpe":#or action=="morphing":
          number_players =int(socket_server.recv())
          while j < number_players:
            dic1 =json.loads(socket_server.recv())
            id_player = dic1["username"]
            from_server(action,players[id_player],username,dic1)
            j+=1


    if init:

      for event in pygame.event.get():
      	
         tecla= pygame.key.get_pressed()

         if event.type==QUIT:
           pygame.quit()
           sys.exit()

         #FUNCIONES PERSONAJE PRINCIPAL INICIO   
         if tecla[K_ESCAPE]:
           terminar = True
            
         for i in tecla:
           sumatoria =sumatoria+i

         if tecla[K_LEFT]:
           players[username].moverizquierda(socket_server,username)           

         elif tecla[K_RIGHT]:
           players[username].moverderecha(socket_server,username)      

         elif tecla[K_UP]:
           players[username].moverarriba(socket_server,username)         
 
         elif tecla[K_DOWN] :
           players[username].moverabajo(socket_server,username) 
         
         if(sumatoria == 0):
            players[username].Horienta()
            #dic={"username":username,"posx":players[username].rect.x,"posy":players[username].rect.y,"i":0,"personaje":players[username].personaje,"carpeta":"carpeta","bandera":True}
            #socket_server.send_multipart(["Horienta",json.dumps(dic,sort_keys=True)])
         sumatoria =0

         if tecla[K_SPACE]:
         
           q=players[username]
           q.anima(q.personaje)
           if q.direc==4:
             carpeta="laterali"
           if q.direc==6:
             carpeta="laterald"
           if q.direc==8:
             carpeta="trasera"
           if q.direc==2:
             carpeta="frontal"
           dic={"username":username,"posx":q.rect.x,"posy":q.rect.y,"direc":q.direc,"i":q.i,"vida":q.vida,"personaje":q.personaje,"dano":q.dano,"gastarmana":q.gastarmana,"carpeta":carpeta,"bandera":True}
           socket_server.send_multipart(["golpe",json.dumps(dic,sort_keys=True)])

         if tecla[K_z]:
            if(players[username].personaje ==players[username].copia and players[username].mana>0): 
               Metamorfosis(players[username],4,players[username].dano+5,True)
         if tecla[K_x]:
            if(players[username].personaje!=players[username].copia):
               Metamorfosis(players[username],players[username].copia,players[username].dano-5,False)
        
    #FUNCIONES PERSONAJE PRINCIPAL FIN 
        
  #ANIMACIONES PERSONAJE PRINCIPAL INICIO 
      for p in jugadores:
       nombre_vida_manajugador.update(p.interfase())
       mapeo.update(nombre_vida_manajugador)
       if(p.animacion):
        p.anima(p.personaje)
       
       if(perdimana>10 and p.gastarmana):
        p.mana-=1
        perdimana =0

       if(p.mana<=0):
        p.personaje=p.copia
        p.gastarmana=False      

      perdimana+=1

       
  #ANIMACIONES PERSONAJE PRINCIPAL FIN     

  #MODIFICADORES DE LOS MAPAS___________________________________________________________________________________________________-

     #MAPA 1 INICIO______________________________________________________MAPA 1 INICIO
      if(fondo.fondo==1):   
        mapeo=(AnimacionMapas.Goanimacion(players,enemigos,jugadores,objetos,mapeo,nombre_vida_mana)) 
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos,objetos,mapeo,nombre_vida_mana)

  #MAPA 2 _________________________________________________________MAPA 2 INICIO
           
      if(fondo.fondo==2):   
        mapeo=(AnimacionMapas.Goanimacion(players,enemigos2,jugadores,objetos1,mapeo,nombre_vida_mana1))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos2,objetos1,mapeo,nombre_vida_mana1)
           
  #MAPA 3 _________________________________________________________MAPA 3 INICIO
    
      if(fondo.fondo==3):   
        mapeo=(AnimacionMapas.Goanimacion(players,enemigos3,jugadores,objetos1,mapeo,nombre_vida_mana2))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos3,objetos1,mapeo,nombre_vida_mana2)

  #MAPA 4______________________________________________________INICIO MAPA 4
      if(fondo.fondo==5):   
        mapeo=(AnimacionMapas.Goanimacion(players,enemigos4,jugadores,objetos1,mapeo,nombre_vida_mana3))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos4,objetos1,mapeo,nombre_vida_mana3)     

  #MAPA 5______________________________________________________INICIO MAPA 5

      if(fondo.fondo==4):   
        mapeo=(AnimacionMapas.Goanimacion(players,enemigos5,jugadores,objetos1,mapeo,nombre_vida_mana4))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos5,objetos1,mapeo,nombre_vida_mana4)
        
        
           
#INICIO MANEJO DE MAPAS _______________________________________________________________
      p=players[username]
      if(p.x>1000 or p.x<0 or p.y<0 or  p.y>0 ):
        if(1==p.fondo and p.y>ALTO):
          manejo_mapas(fondo,p,500,0,2,socket_server)
          
        if(2==p.fondo and p.y<-20):
          manejo_mapas(fondo,p,250,700,1,socket_server)
         
        if(1==p.fondo and p.x<0):
          manejo_mapas(fondo,p,1000,p.y,3,socket_server)

        if(3==p.fondo and p.x>ANCHO):
          manejo_mapas(fondo,p,0,p.y,1,socket_server)
          
        if(1==p.fondo and p.y<0):
          manejo_mapas(fondo,p,p.x,680,4,socket_server)

        if(4==p.fondo and p.y>700):
          manejo_mapas(fondo,p,p.x,20,1,socket_server)

        if(2==p.fondo and p.y>700):
          manejo_mapas(fondo,p,p.x,0,5,socket_server)

        if(5==p.fondo and p.y<0):
          manejo_mapas(fondo,p,p.x,700,2,socket_server)


        for iterador,p in players.iteritems():
            if p.fondo != fondo.fondo:
                mapeo.remove(p)
                mapeo.remove(p.interfase())
                nombre_vida_manajugador.remove(p.interfase())
                jugadores.remove(p)
            if p.fondo== fondo.fondo and not mapeo.has(p):
                mapeo.add(p)
                mapeo.add(p.interfase())
                jugadores.add(p)
                nombre_vida_manajugador.add(p.interfase())
        


      #FIN MANEJO DE MAPAS _______________________________________________________________

      fondos.draw(PANTALLA)
      mapeo.draw(PANTALLA)
      time.sleep(0.005)
      pygame.display.flip()
  pygame.quit()
    

if __name__=="__main__":
 ALTO= 640
 ANCHO= 1000

 pygame.init()

 PANTALLA= pygame.display.set_mode([ANCHO,ALTO])
 pygame.key.set_repeat(100,10)
 inicio()
