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
    img4=pygame.image.load("objetos/pj4.png")
    seleccionar1= pygame.image.load("objetos/botones/3.png")
    seleccionar12= pygame.image.load("objetos/botones/3.3.png")
    
    salir1= pygame.image.load("objetos/botones/2.png")
    salir2= pygame.image.load("objetos/botones/2.2.png")
    boton1= Boton(seleccionar1,seleccionar12,90,450)
    boton2= Boton(seleccionar1,seleccionar12,326,450)
    boton3= Boton(seleccionar1,seleccionar12,562,450)
    boton4= Boton(seleccionar1,seleccionar12,798,450)
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
                elif cursor.colliderect(boton4.rect):
                    pygame.mixer.music.stop()
                    Game(5)
                if cursor.colliderect(boton6.rect):
                    cerrar=True
                
        cursor.posicion()
        PANTALLA.blit(fondo,(0,0))
        PANTALLA.blit(img1,(30,150))
        PANTALLA.blit(img2,(266,150))
        PANTALLA.blit(img3,(502,150))
        PANTALLA.blit(img4,(738,150))
        boton1.accion(PANTALLA,cursor)
        boton2.accion(PANTALLA,cursor)
        boton3.accion(PANTALLA,cursor)
        boton4.accion(PANTALLA,cursor)
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
    def Cambiominimapa(self,x,y,fondo):
        self.image=pygame.image.load("fondos/mini/"+str(fondo)+".png")

class Jugador(pygame.sprite.Sprite):
    def __init__(self,nombre,direc,x,y,fondo,personaje):
        pygame.sprite.Sprite.__init__(self)
        self.nombre=nombre
        self.salud=100
        self.vidas=3
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
        self.muestramapa=False
        self.choqueobjetos=False
        self.copia=self.personaje
        self.gastarmana=False
        self.dano=5
        self.nombreinterfas=Nombre()
        self.manainterfas=Mana()
        self.vidainterfas=Vida()
        self.lastimar=False
        


    def chocar(self,ob):
        self.pasos=20
        for col in ob:
            if pygame.sprite.collide_rect(self,col):              
                if col.direc==4 and (self.direc==4 or self.direc==2 or self.direc==8):
                    self.pasos=20
                   

                elif col.direc==6 and (self.direc==6 or self.direc==2 or self.direc==8):
                    self.pasos=20

                elif col.direc==8 and (self.direc==4 or self.direc==8 or self.direc==6):
                    self.pasos=20

                elif col.direc==2 and (self.direc==4 or self.direc==2 or self.direc==6):
                    self.pasos=20

                else:
                    self.pasos=0
                if(self.lastimar):
                     col.vida-=self.dano
                     self.lastimar=False
           
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

    def chocarpvp(self,socket_server,ob):
    	    #self.pasos=20
            if pygame.sprite.collide_rect(self,ob):              
                    if ob.direc==4 and (self.direc==4 or self.direc==2 or self.direc==8):
                        self.pasos=20
                        
                        
                    elif ob.direc==6 and (self.direc==6 or self.direc==2 or self.direc==8):
                        self.pasos=20
                        

                    elif ob.direc==8 and (self.direc==4 or self.direc==8 or self.direc==6):
                        self.pasos=20
                        
                    elif ob.direc==2 and (self.direc==4 or self.direc==2 or self.direc==6):
                        self.pasos=20
                        
                    else:
                        self.pasos=0
                        
                    if(self.lastimar):
                        ob.vida-=self.dano
                        self.lastimar=False
                        if(ob.vida <= 0):
                            print ("perdio una vida")
                            ob.vidas-=1
                            ob.vida=100
                            valor=random.randint(1,18) 
                            ob.fondo=valor
                            action="dead"
                        else:
                        	action="dano"


                        dic={"mapa":ob.fondo,"vidas": ob.vidas,"vida": ob.vida,"username":ob.nombre}
                        socket_server.send_multipart([action,json.dumps(dic,sort_keys=True)])

            else:
            	self.lastimar=False 

    def transformar(self):
        self.personaje=4
        self.dano+=5
        self.gastarmana =True 
        

    def destransformar(self):
        self.personaje=self.copia
        self.dano-=5
        self.gastarmana =False 
                   
                         

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
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"personaje":self.personaje,"carpeta":"laterali"}
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
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"personaje":self.personaje,"carpeta":"laterald"}
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
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"personaje":self.personaje,"carpeta":"trasera"}
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
          dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":self.i,"personaje":self.personaje,"carpeta":"frontal"}
          socket_server.send_multipart(["move",json.dumps(dic,sort_keys=True)])


    def Orientacion(self):

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
         #dic={"username":username,"posx":self.rect.x,"posy":self.rect.y,"direc":self.direc,"i":0,"vida":self.vida,"personaje":self.personaje,"dano":self.dano,"gastarmana":self.gastarmana,"carpeta":carpeta}         
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
        if(self.direc==8):
            if(self.direc==8 and self.iy<=10):
                self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/trasero/"+str(self.iy)+".png")
                self.iy=self.iy+1
            else:
             self.iy=1
             self.animacion=False
             self.lastimar=True

        if(self.direc==2):
            if(self.direc==2 and self.iy<=10):
                self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/frontal/"+str(self.iy)+".png")
                self.iy=self.iy+1
            else:
                self.iy=1
                self.animacion=False
                self.lastimar=True

        if(self.direc==4 ):
            if(self.direc==4 and self.iy<=10):
             self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/laterali/"+str(self.iy)+".png")
             self.iy=self.iy+1
            else:
                self.iy=1
                self.animacion=False
                self.lastimar=True

        if(self.direc==6 ):
            if(self.direc==6 and self.iy<=10):
             self.Pj= pygame.image.load("Animaciones/"+str(ani)+"/laterald/"+str(self.iy)+".png")
             self.iy=self.iy+1
            else:
                self.iy=1
                self.animacion=False
                self.lastimar=True
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


        
    def Goanimacion(self,socket_server,fondo,players,enemigos,jugador,jugadores,objetos,retornar,nombre_vida_mana):
        
       #CARGAR ELEMENTOS DEL MAPA EN CUESTION
        retornar.add(objetos)     
        retornar.add(enemigos)
        
        aux=0
        iterador=0
        index=0
        
       #INTERFAS VIDA MANA NOMBRE
        """for col in enemigos:
            nombre_vida_mana.add(col.interfase())
            retornar.add(nombre_vida_mana)
            bandera=0
            bandera2=1
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
                col.ataca=False"""

        #COLICION JUGADORES
        jugador.pasos=20
        for col in jugadores:
            if col.nombre != jugador.nombre:
                jugador.chocarpvp(socket_server,col)



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
    if(player.muestramapa):
        fondo.Cambiominimapa(-330,0,player.fondo)
    dic={"mapa":fondo_aux,"username":player.nombre}
    socket_server.send_multipart(["mapeo",json.dumps(dic,sort_keys=True)])



def from_server(action,player,username,dic1,fondo): 
	if action=="move":
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
			player.personaje=dic1["personaje"]
			player.image=player.Pj
	if action == "golpe":
		player.anima(player.personaje)
	if action=="mapeo":
		player.fondo=dic1["mapa"]
	if action  == "dano" or action=="dead":
		
		player.vida=dic1["vida"]
		player.vidas=dic1["vidas"]
		player.fondo=dic1["mapa"]
		if player.nombre==username:
			fondo.Cambiomapa(-330,0,dic1["mapa"])
			fondo.fondo=dic1["mapa"]
	if action == "transformar":
		if dic1["morph"]:
			player.transformar()
		else:
			player.destransformar()








#_________________________________________INICIO DEL JUEGO_______________________________________
def Game(n):

  init =False
  players={}
  #____________________________________________________________Establecer conexion con el servidor
  ctx = zmq.Context()
  socket_server = ctx.socket(zmq.XREQ)
  socket_server.connect('tcp://'+sys.argv[2]+':5555')

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
  counter=True
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
          number_players=int(json.loads(socket_server.recv()))
          while j<number_players:
            dic=json.loads(socket_server.recv())
            jugador_temp=Jugador(dic["username"],dic["direc"],dic["posx"],dic["posy"],dic["fondo"],dic["personaje"])
            players[dic["username"]]=jugador_temp
            if 1==dic["fondo"]:
            	jugadores.add(jugador_temp)
                mapeo.add(jugador_temp)
                nombre_vida_manajugador.add(jugador_temp.interfase())
                mapeo.add(nombre_vida_manajugador)
            j+=1
          if counter:
              counter=False
              init=True
              #FONDO INICIAL
              fondos= pygame.sprite.Group()
              fondo= Fondos(-330,0,players[username].fondo)
              fondos.add(fondo)
              #INICIALIZARPERSONAJEPRINCIPAL
              AnimacionMapas=AnimacionMapa()
              #MAPA 1_____________________________________________________________INICIO MAPA 1
              enemigos= pygame.sprite.Group()
              objetos= pygame.sprite.Group()

              #__________________ENEMIGOS

              enemigo=Enemigo("Ronal",8,200,400,100,100,100,1,100,100,0)
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
              objetos1= pygame.sprite.Group()

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

              ob1= Objetosinvi(0,650,"50-50")
              ob2= Objetosinvi(50,650,"50-50")
              ob3= Objetosinvi(100,650,"50-50")
              ob4= Objetosinvi(420,660,"50-50")
              ob5= Objetosinvi(190,-50,"150-150")
              ob6= Objetosinvi(0,0,"50-50")
              ob7= Objetosinvi(30,-30,"50-50")
              ob8= Objetosinvi(350,330,"10-10")


              ob10= Objetosinvi(600,390,"10-10")
              ob11= Objetosinvi(620,410,"10-10")
              ob12= Objetosinvi(640,430,"10-10")
              ob13= Objetosinvi(660,450,"10-10")
              ob14= Objetosinvi(680,470,"10-10")
              ob15= Objetosinvi(700,480,"10-10")
              ob16= Objetosinvi(720,500,"10-10")
              ob17= Objetosinvi(740,490,"10-10")
              ob18= Objetosinvi(760,500,"10-10")
              ob19= Objetosinvi(780,510,"10-10")
              ob20= Objetosinvi(790,500,"10-10")

              ob22= Objetosinvi(1000,0,"1000")
              objetos1.add(ob22)


              objetos1.add(ob1)
              objetos1.add(ob2)
              objetos1.add(ob3)
              objetos1.add(ob4)
              objetos1.add(ob5)
              objetos1.add(ob6)
              objetos1.add(ob7)
              objetos1.add(ob8)

              objetos1.add(ob10)
              objetos1.add(ob11)
              objetos1.add(ob12)
              objetos1.add(ob13)
              objetos1.add(ob14)
              objetos1.add(ob15)
              objetos1.add(ob16)
              objetos1.add(ob17)
              objetos1.add(ob18)
              objetos1.add(ob19)
              objetos1.add(ob20)


              #____________________________________________________________________FIN DE MAPA 2



              #MAPA 3___________________________________________________________INICIO MAPA 3
              enemigos3= pygame.sprite.Group()
              objetos2= pygame.sprite.Group()
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


              ob21= Objetosinvi(0,750,"1000")
              objetos2.add(ob21)

              ob22= Objetosinvi(0,-750,"1000")
              objetos2.add(ob22)

              #____________________________________________________________________FIN DE MAPA 3




              #MAPA 4_______________________________________________________________INICIO MAPA 4
              enemigos4= pygame.sprite.Group()
              objetos4= pygame.sprite.Group()
              #__________________ENEMIGOS
              enemigo=Enemigo("ELPODEROSOYPITUDOBOSFINAL",8,500,450,400,400,200,5,1000,100,3)

              enemigos4.add(enemigo)


              #___________________OBJETOS


              ob23= Objetosinvi(0,700,"1000")


              objetos4.add(ob23)




              #______________________________________________________________________FIN DE MAPA 4


              #MAPA 5___________________________________________________________INICIO MAPA 5
              enemigos5= pygame.sprite.Group()
              objetos5= pygame.sprite.Group()
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
              #MAPA 5___________________________________________________________Fin MAPA 5






              #MAPA 6___________________________________________________________INICIO MAPA 6
              enemigos6= pygame.sprite.Group()
              objetos6= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("Feo1",8,200,400,100,100,100,1,100,100,0)
              enemigo1=Enemigo("Feo2",2,400,400,400,300,250,1,100,100,1)


              enemigos6.add(enemigo)
              enemigos6.add(enemigo1)



              #___________________OBJETOS 


              ob22= Objetosinvi(800,0,"1000")
              ob20= Objetosinvi(700,500,"1000")
              ob19= Objetosinvi(0,700,"1000")
              objetos6.add(ob19)
              objetos6.add(ob22)
              objetos6.add(ob20)

              #____________________________________________________________________FIN DE MAPA 6


              #MAPA 6___________________________________________________________INICIO MAPA 7
              enemigos7= pygame.sprite.Group()
              objetos7= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("sol",8,200,400,100,100,100,1,100,100,2)
              enemigo1=Enemigo("luna",2,400,400,400,300,250,1,100,100,2)

              enemigos7.add(enemigo)
              enemigos7.add(enemigo1)



              #___________________OBJETOS 

              ob19= Objetosinvi(740,-300,"1000")
              ob20= Objetosinvi(1000,400,"1000")
              objetos7.add(ob19)
              objetos7.add(ob20)

              #____________________________________________________________________FIN DE MAPA 7


              #MAPA 8___________________________________________________________INICIO MAPA 8
              enemigos8= pygame.sprite.Group()
              objetos8= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("nose",8,200,400,100,100,100,1,100,100,0)
              enemigo1=Enemigo("nose2",2,400,400,400,300,250,1,100,100,0)

              enemigos8.add(enemigo)
              enemigos8.add(enemigo1)



              #___________________OBJETOS 

              ob1= Objetosinvi(400,-650,"1000")
              ob3= Objetosinvi(0,-680,"1000")
              ob2= Objetosinvi(740,0,"1000")
              objetos8.add(ob1)
              objetos8.add(ob2)
              objetos8.add(ob3)




              #____________________________________________________________________FIN DE MAPA 8




              #MAPA 9___________________________________________________________INICIO MAPA 9
              enemigos9= pygame.sprite.Group()
              objetos9= pygame.sprite.Group()

              #__________________ENEMIGOS




              #___________________OBJETOS 

              ob1= Objetosinvi(0,700,"1000")
              ob3= Objetosinvi(0,-800,"1000")
              ob2= Objetosinvi(-200,200,"1000")
              objetos9.add(ob1)
              objetos9.add(ob2)
              objetos9.add(ob3)

              #____________________________________________________________________FIN DE MAPA 9


              #MAPA 10___________________________________________________________INICIO MAPA 10
              enemigos10= pygame.sprite.Group()
              objetos10= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("lool",8,200,400,100,100,100,1,100,100,2)
              enemigo1=Enemigo("leel",2,400,400,400,300,250,1,100,100,2)

              enemigos10.add(enemigo)
              enemigos10.add(enemigo1)



              #___________________OBJETOS 

              ob1= Objetosinvi(-1000,0,"1000")
              ob3= Objetosinvi(-540,-720,"1000")
              ob2= Objetosinvi(730,-720,"1000")

              objetos10.add(ob2)
              objetos10.add(ob1)
              objetos10.add(ob3)


              #MAPA 11___________________________________________________________INICIO DE MAPA 11


              enemigos11= pygame.sprite.Group()
              objetos11= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("zion",8,200,400,100,100,100,1,100,100,1)
              enemigo1=Enemigo("wid",2,400,400,400,300,250,1,100,100,0)

              enemigos11.add(enemigo)
              enemigos11.add(enemigo1)



              #___________________OBJETOS 

              ob1= Objetosinvi(-1000,0,"1000")
              ob2= Objetosinvi(1000,0,"1000")
              ob3= Objetosinvi(-850,550,"1000")
              ob10= Objetosinvi(550,270,"10-10")

              objetos11.add(ob3)
              objetos11.add(ob10)
              objetos11.add(ob2)
              objetos11.add(ob1)


              #____________________________________________________________________FIN DE MAPA 11


              #MAPA 12___________________________________________________________INICIO DE MAPA 12


              enemigos12= pygame.sprite.Group()
              objetos12= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("zion",8,200,400,100,100,100,1,100,100,2)
              enemigo1=Enemigo("wid",2,400,400,400,300,250,1,100,100,2)

              enemigos12.add(enemigo)
              enemigos12.add(enemigo1)


              #___________________OBJETOS 

              ob12= Objetosinvi(-1000,0,"1000")
              ob13= Objetosinvi(800,-400,"1000")
              ob14= Objetosinvi(1000,-0,"1000")

              objetos12.add(ob14)
              objetos12.add(ob13)
              objetos12.add(ob12)

              #____________________________________________________________________FIN DE MAPA 12


              #MAPA 13___________________________________________________________INICIO DE MAPA 13


              enemigos13= pygame.sprite.Group()
              objetos13= pygame.sprite.Group()

              #__________________ENEMIGOS


              #___________________OBJETOS 

              ob1= Objetosinvi(-1000,0,"1000")
              ob3= Objetosinvi(0,-720,"1000")
              ob2= Objetosinvi(800,-590,"1000")
              ob4= Objetosinvi(950,0,"1000")

              objetos13.add(ob2)
              objetos13.add(ob1)
              objetos13.add(ob3)
              objetos13.add(ob4)


              #____________________________________________________________________FIN DE MAPA 13



              #MAPA 14___________________________________________________________INICIO DE MAPA 14


              enemigos14= pygame.sprite.Group()
              objetos14= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("z",8,200,400,100,100,100,1,100,100,0)
              enemigo1=Enemigo("w",2,400,400,400,300,250,1,100,100,0)




              enemigos14.add(enemigo)
              enemigos14.add(enemigo1)


              #___________________OBJETOS


              ob2= Objetosinvi(-1000,0,"1000")


              objetos14.add(ob2)

              #MAPA 15___________________________________________________________INICIO DE MAPA 15


              enemigos15= pygame.sprite.Group()
              objetos15= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("zzzz",8,200,400,100,100,100,1,100,100,0)
              enemigo1=Enemigo("weri",2,400,400,400,300,250,1,100,100,0)

              enemigos15.add(enemigo)
              enemigos15.add(enemigo1)



              #___________________OBJETOS




              ob1= Objetosinvi(-1000,0,"1000")
              ob3= Objetosinvi(0,-750,"1000")
              ob20= Objetosinvi(200,600,"10-10")
              ob21= Objetosinvi(220,600,"10-10")
              ob5= Objetosinvi(900,370,"10-10")

              objetos15.add(ob5)
              objetos15.add(ob20)
              objetos15.add(ob21)
              objetos15.add(ob1)
              objetos15.add(ob3)




              #MAPA 16___________________________________________________________INICIO DE MAPA 16


              enemigos16= pygame.sprite.Group()
              objetos16= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("zion",8,200,400,100,100,100,1,100,100,1)
              enemigo1=Enemigo("xion",2,400,400,400,300,250,1,100,100,1)

              enemigos16.add(enemigo)
              enemigos16.add(enemigo1)


              #___________________OBJETOS


              ob5= Objetosinvi(-1000,0,"1000")
              ob6= Objetosinvi(20,390,"10-10")
              ob7= Objetosinvi(800,350,"50-50")
              objetos16.add(ob6)
              objetos16.add(ob5)
              objetos16.add(ob7)



              #MAPA 17_______________________________________________________________INICIO MAPA 17
              enemigos17= pygame.sprite.Group()
              objetos17= pygame.sprite.Group()
              #__________________ENEMIGOS
              enemigo=Enemigo("LEO",8,500,450,400,400,200,5,1000,100,3)
              enemigo1=Enemigo("LEO HIJO",8,600,350,400,400,200,5,500,100,3)
              enemigo2=Enemigo("ZION",8,300,650,400,400,200,5,500,100,3)

              enemigos17.add(enemigo)
              enemigos17.add(enemigo1)
              enemigos17.add(enemigo2)


              #___________________OBJETOS


              ob5= Objetosinvi(-1000,0,"1000")
              ob6= Objetosinvi(0,700,"1000")

              objetos17.add(ob6)
              objetos17.add(ob5)



              #______________________________________________________________________FIN DE MAPA 17




              #MAPA 18___________________________________________________________INICIO MAPA 18
              enemigos18= pygame.sprite.Group()
              objetos18= pygame.sprite.Group()

              #__________________ENEMIGOS
              enemigo=Enemigo("Ronal",8,200,300,100,100,100,1,100,100,2)
              enemigo1=Enemigo("Reinosa",2,600,300,500,300,250,1,100,100,2)
              enemigo2=Enemigo("Cristian",6,400,400,300,400,200,1,100,100,2)
              enemigo3=Enemigo("Risitas",4,400,500,400,400,150,1,100,100,2)
              enemigo4=Enemigo("Ronal",8,500,200,200,200,100,1,100,100,2)

              enemigos18.add(enemigo)
              enemigos18.add(enemigo1)
              enemigos18.add(enemigo2)
              enemigos18.add(enemigo3)
              enemigos18.add(enemigo4)


              #___________________OBJETOS


              ob5= Objetosinvi(-0,-790,"1000")
              ob6= Objetosinvi(0,700,"1000")
              ob7= Objetosinvi(1000,0,"1000")
              objetos18.add(ob7)
              objetos18.add(ob6)
              objetos18.add(ob5)


              #___________________________________________________________Fin MAPA 18


              




              #INTERFAS VIDA MANA NOMBRE
              nombre_vida_mana3= pygame.sprite.Group()
              nombre_vida_mana2= pygame.sprite.Group()
              nombre_vida_mana1= pygame.sprite.Group()
              nombre_vida_mana= pygame.sprite.Group()
              nombre_vida_mana4= pygame.sprite.Group()
              nombre_vida_mana6= pygame.sprite.Group()
              nombre_vida_mana7= pygame.sprite.Group()
              nombre_vida_mana8= pygame.sprite.Group()
              nombre_vida_mana9= pygame.sprite.Group()
              nombre_vida_mana10= pygame.sprite.Group()
              nombre_vida_mana11= pygame.sprite.Group()
              nombre_vida_mana12= pygame.sprite.Group()
              nombre_vida_mana13= pygame.sprite.Group()
              nombre_vida_mana14= pygame.sprite.Group()
              nombre_vida_mana15= pygame.sprite.Group()
              nombre_vida_mana16= pygame.sprite.Group()
              nombre_vida_mana17= pygame.sprite.Group()
              nombre_vida_mana18= pygame.sprite.Group()

              #INICIO MUSICA FONDO
              #pygame.mixer.music.load("musica/2.mp3")
              #pygame.mixer.music.play(-1)
              sumatoria =0
              perdimana =0
      if action == "disconnect":
             number_players=int(json.loads(socket_server.recv()))
             dic=json.loads(socket_server.recv())
             p=players[dic["username"]]
             del players[dic["username"]]
             mapeo.remove(p)
             mapeo.remove(p.interfase())
             nombre_vida_manajugador.remove(p.interfase())
             jugadores.remove(p)  
      if action=="move" or action=="golpe" or action =="mapeo" or action == "dano" or action=="dead" or action=="transformar":
            number_players=int(json.loads(socket_server.recv()))
            dic=json.loads(socket_server.recv())
            id_player = dic["username"]
            from_server(action,players[id_player],username,dic,fondo)


    if init:
      
      for event in pygame.event.get():
      	
         tecla= pygame.key.get_pressed()
         mouse=pygame.mouse.get_focused()
         if event.type==QUIT:
           pygame.quit()
           sys.exit()

         #FUNCIONES PERSONAJE PRINCIPAL INICIO   
         if tecla[K_ESCAPE]:
           terminar = True
           socket_server.send_multipart(["disconnect",username])
            
         for i in tecla:
           sumatoria =sumatoria+i

         if tecla[K_LEFT] :
           players[username].moverizquierda(socket_server,username)           

         elif tecla[K_RIGHT] :
           players[username].moverderecha(socket_server,username)      

         elif tecla[K_UP] :
           players[username].moverarriba(socket_server,username)         
 
         elif tecla[K_DOWN] :
           players[username].moverabajo(socket_server,username) 
         
         if(sumatoria == 0 ):
            players[username].Orientacion()
            
         sumatoria =0

         if tecla[K_SPACE] :
           q.animacion=True
           

         if tecla[K_z] :
            if(players[username].personaje == players[username].copia and players[username].mana>0): 
               players[username].transformar()
               dic={"username":players[username].nombre,"morph":True}
               socket_server.send_multipart(["transformar",json.dumps(dic,sort_keys=True)]) 
         if tecla[K_x]:
            if(players[username].personaje!=players[username].copia):
               players[username].destransformar()
               dic={"username":players[username].nombre,"morph":False}
               socket_server.send_multipart(["transformar",json.dumps(dic,sort_keys=True)]) 

         if tecla[K_m]:
           fondo.Cambiominimapa(-330,0,players[username].fondo)
           players[username].muestramapa=True 

         if tecla[K_n]:
           fondo.Cambiomapa(-330,0,players[username].fondo)
           players[username].muestramapa=False 
        
    #FUNCIONES PERSONAJE PRINCIPAL FIN
    #ANIMACIONES PERSONAJE PRINCIPAL INICIO
      q=players[username]
      if(q.animacion):
           q.anima(q.personaje)
           if q.direc==4:
             carpeta="laterali"
           if q.direc==6:
             carpeta="laterald"
           if q.direc==8:
             carpeta="trasera"
           if q.direc==2:
             carpeta="frontal"
           dic={"username":username}
           socket_server.send_multipart(["golpe",json.dumps(dic,sort_keys=True)])
       
      for p in jugadores:
       nombre_vida_manajugador.update(p.interfase())
       mapeo.update(nombre_vida_manajugador)

       
       if(perdimana>10 and p.gastarmana):
        p.mana-=1
        perdimana =0

       if(p.mana<=0):
        p.personaje=p.copia
        p.gastarmana=False 
        p.dano-=5     

      perdimana+=1

       
  #ANIMACIONES PERSONAJE PRINCIPAL FIN     

  #MODIFICADORES DE LOS MAPAS___________________________________________________________________________________________________-

     #MAPA 1 INICIO______________________________________________________MAPA 1 INICIO
      if(fondo.fondo==1):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos,players[username],jugadores,objetos,mapeo,nombre_vida_mana)) 
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos,objetos,mapeo,nombre_vida_mana)

  #MAPA 2 _________________________________________________________MAPA 2 INICIO
           
      if(fondo.fondo==2):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos2,players[username],jugadores,objetos1,mapeo,nombre_vida_mana1))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos2,objetos1,mapeo,nombre_vida_mana1)
           
  #MAPA 3 _________________________________________________________MAPA 3 INICIO
    
      if(fondo.fondo==3):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos3,players[username],jugadores,objetos2,mapeo,nombre_vida_mana2))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos3,objetos2,mapeo,nombre_vida_mana2)

  #MAPA 4______________________________________________________INICIO MAPA 4
      if(fondo.fondo==5):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos4,players[username],jugadores,objetos4,mapeo,nombre_vida_mana3))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos4,objetos4,mapeo,nombre_vida_mana3)     

  #MAPA 5______________________________________________________INICIO MAPA 5

      if(fondo.fondo==4):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos5,players[username],jugadores,objetos5,mapeo,nombre_vida_mana4))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos5,objetos5,mapeo,nombre_vida_mana4)
    #INICIO MAPA 6______________________________________________________INICIO MAPA 6

      if(fondo.fondo==6):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos6,players[username],jugadores,objetos6,mapeo,nombre_vida_mana6))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos6,objetos6,mapeo,nombre_vida_mana6)  

#INICIO MAPA 7______________________________________________________INICIO MAPA 7

      if(fondo.fondo==7):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos7,players[username],jugadores,objetos7,mapeo,nombre_vida_mana7))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos7,objetos7,mapeo,nombre_vida_mana7)  


#INICIO MAPA 8______________________________________________________INICIO MAPA 8

      if(fondo.fondo==8):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos8,players[username],jugadores,objetos8,mapeo,nombre_vida_mana8))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos8,objetos8,mapeo,nombre_vida_mana8)  


#INICIO MAPA 9______________________________________________________INICIO MAPA 9

      if(fondo.fondo==9):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos9,players[username],jugadores,objetos9,mapeo,nombre_vida_mana9))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos9,objetos9,mapeo,nombre_vida_mana9)  

#INICIO MAPA 10______________________________________________________INICIO MAPA 10

      if(fondo.fondo==10):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos10,players[username],jugadores,objetos10,mapeo,nombre_vida_mana10))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos10,objetos10,mapeo,nombre_vida_mana10)  

#INICIO MAPA 11______________________________________________________INICIO MAPA 11

      if(fondo.fondo==11):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos11,players[username],jugadores,objetos11,mapeo,nombre_vida_mana11))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos11,objetos11,mapeo,nombre_vida_mana11)  

#INICIO MAPA 12______________________________________________________INICIO MAPA 12

      if(fondo.fondo==12):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos12,players[username],jugadores,objetos12,mapeo,nombre_vida_mana12))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos12,objetos12,mapeo,nombre_vida_mana12)  


#INICIO MAPA 13______________________________________________________INICIO MAPA 13

      if(fondo.fondo==13):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos13,players[username],jugadores,objetos13,mapeo,nombre_vida_mana13))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos13,objetos13,mapeo,nombre_vida_mana13)


#INICIO MAPA 14______________________________________________________INICIO MAPA 14

      if(fondo.fondo==14):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos14,players[username],jugadores,objetos14,mapeo,nombre_vida_mana14))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos14,objetos14,mapeo,nombre_vida_mana14)


#INICIO MAPA 15______________________________________________________INICIO MAPA 15

      if(fondo.fondo==15):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos15,players[username],jugadores,objetos15,mapeo,nombre_vida_mana15))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos15,objetos15,mapeo,nombre_vida_mana15)

#INICIO MAPA 16______________________________________________________INICIO MAPA 16

      if(fondo.fondo==16):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos16,players[username],jugadores,objetos16,mapeo,nombre_vida_mana16))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos16,objetos16,mapeo,nombre_vida_mana16)

#INICIO MAPA 17______________________________________________________INICIO MAPA 17

      if(fondo.fondo==17):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos17,players[username],jugadores,objetos17,mapeo,nombre_vida_mana17))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos17,objetos17,mapeo,nombre_vida_mana17)


#INICIO MAPA 18______________________________________________________INICIO MAPA 17

      if(fondo.fondo==18):   
        mapeo=(AnimacionMapas.Goanimacion(socket_server,fondo,players,enemigos18,players[username],jugadores,objetos18,mapeo,nombre_vida_mana18))   
      else: 
        mapeo=AnimacionMapas.KillAnimacion(enemigos18,objetos18,mapeo,nombre_vida_mana18)

      
           
#INICIO MANEJO DE MAPAS _______________________________________________________________
      p=players[username]
      if(p.x>1000 or p.x<0 or p.y<0 or  p.y>0 ):
        if(1==p.fondo and p.y>ALTO):
            
            manejo_mapas(fondo,p,500,0,2,socket_server)
             

        if(1==p.fondo and p.x>1000):
            
            manejo_mapas(fondo,p,0,p.y,6,socket_server)

        if(6==p.fondo and p.x<0):
            
            manejo_mapas(fondo,p,1000,300,1,socket_server)

        if(6==p.fondo and p.y<0):
           
            manejo_mapas(fondo,p,400,680,7,socket_server)

        if(7==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,200,20,6,socket_server)

        if(7==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,200,680,8,socket_server)

        if(7==p.fondo and p.x<0):
            
            manejo_mapas(fondo,p,990,300,4,socket_server)

        if(4==p.fondo and p.x>1000):
            
            manejo_mapas(fondo,p,0,300,7,socket_server)

             

        if(7==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,200,680,8,socket_server)

        if(8==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,200,0,7,socket_server)


        if(8==p.fondo and p.x<0):
           
            manejo_mapas(fondo,p,1000,350,9,socket_server)

        if(9==p.fondo and p.x>1000):
           
            manejo_mapas(fondo,p,0,350,8,socket_server)

        if(9==p.fondo and p.x<0):
            
            manejo_mapas(fondo,p,1000,350,10,socket_server)             

        if(10==p.fondo and p.x>1000):
            
            manejo_mapas(fondo,p,0,40,9,socket_server)

        if(10==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,350,0,11,socket_server)


        if(10==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,p.x,680,13,socket_server)

        if(13==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,550,0,10,socket_server)



        if(11==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,350,680,10,socket_server)  


        if(11==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,350,0,12,socket_server)

        if(12==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,350,680,11,socket_server)

        if(12==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,430,0,4,socket_server)  

        if(4==p.fondo and p.y<0):
           
            manejo_mapas(fondo,p,300,680,12,socket_server)

        if(4==p.fondo and p.x<0):
            
            manejo_mapas(fondo,p,980,480,15,socket_server)  

        if(15==p.fondo and p.x>980):
            
            manejo_mapas(fondo,p,0,450,4,socket_server)           
 

        if(2==p.fondo and p.y<-20):
            
            manejo_mapas(fondo,p,250,700,1,socket_server)

        if(2==p.fondo and p.x<0):
            
            manejo_mapas(fondo,p,140,1000,16,socket_server)

        if(16==p.fondo and p.x>1000):
            
            manejo_mapas(fondo,p,0,350,2,socket_server) 


        if(1==p.fondo and p.x<0):
           
            manejo_mapas(fondo,p,1000,p.y,3,socket_server)

        if(3==p.fondo and p.x>1000):
           
            manejo_mapas(fondo,p,0,320,1,socket_server)

        if(3==p.fondo and p.x<0):
           
            manejo_mapas(fondo,p,980,320,14,socket_server)

        if(14==p.fondo and p.x>1000):
            
            manejo_mapas(fondo,p,0,320,3,socket_server)

        if(14==p.fondo and p.y>700):
           
            manejo_mapas(fondo,p,350,0,16,socket_server)

        if(16==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,350,689,14,socket_server)

        if(16==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,350,0,17,socket_server)

        if(17==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,350,689,16,socket_server)


        if(14==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,500,690,15,socket_server)

        if(15==p.fondo and p.y>700):
            
            manejo_mapas(fondo,p,500,0,14,socket_server)


             

        if(1==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,p.x,680,4,socket_server)  

        if(4==p.fondo and p.y>700):
           
            manejo_mapas(fondo,p,700,20,1,socket_server)       

        if(2==p.fondo and p.y>700):
           
            manejo_mapas(fondo,p,400,50,5,socket_server) 

        if(5==p.fondo and p.y<0):
            
            manejo_mapas(fondo,p,180,680,2,socket_server)

        if(17==p.fondo and p.x>1000):
            
            manejo_mapas(fondo,p,0,200,5,socket_server)

        if(5==p.fondo and p.x<0):
            
            manejo_mapas(fondo,p,990,200,17,socket_server)

        if(5==p.fondo and p.x>1000):
           
            manejo_mapas(fondo,p,0,200,18,socket_server)

        if(18==p.fondo and p.x<0):
            
            manejo_mapas(fondo,p,990,200,5,socket_server) 
            


        for p in players.values():
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
