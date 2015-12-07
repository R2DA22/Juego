import zmq
import json
import sys

class Player():
	def __init__(self,id_client,player,dic):
		self.id_client=id_client
		self.player="player"+str(player)
	 	self.dic=dic
	 	self.Online=False
	def Getid_client(self):
		return self.id_client



def multicast(socket_clients,id_client,players,action,dic,n):
	i=0
	for addres in players.values():
		if id_client != addres.Getid_client:
			socket_clients.send_multipart([addres.Getid_client(),action,json.dumps(n,sort_keys=True),json.dumps(dic,sort_keys=True)])





pos_init_x=600
pos_init_y=100
ctx = zmq.Context()
socket_clients = ctx.socket(zmq.XREP)
socket_clients.bind('tcp://*:5555')
fondo=1

players={}

poller = zmq.Poller()
poller.register(socket_clients, zmq.POLLIN)
n_online=0
while True:

	socks = dict(poller.poll())
	if socket_clients in socks and socks[socket_clients] == zmq.POLLIN:
		id_client=socket_clients.recv()
		action=socket_clients.recv()
		
		if action=="connect":
			username=socket_clients.recv()
			personaje=json.loads(socket_clients.recv())
			dic={"username":username,"direc":4,"posx":pos_init_x,"posy":pos_init_y,"fondo":fondo,"personaje":personaje}
			gamer=Player(id_client,len(players)+1,dic)
			players[username]=gamer
			#fondo += 1
			
			print username + " Online"
			
			for addres in players.values():	
					if addres.Online:
						n=len(players)-n_online
						flag=True
					else:
						flag=False
						n=len(players)
					
					socket_clients.send_multipart([addres.Getid_client(),action,json.dumps(n)])
					for aux in players.values():	
						if flag:
							if not aux.Online:
								socket_clients.send_multipart([addres.Getid_client(),json.dumps(aux.dic,sort_keys=True)])
						else:
							socket_clients.send_multipart([addres.Getid_client(),json.dumps(aux.dic,sort_keys=True)])

			players[username].Online=True
			n_online+=1
		else:
			dic1=json.loads(socket_clients.recv())
			nombre=dic1["username"]
			if action=="move" or action=="golpe":
				players[nombre].dic["direc"]=dic1["direc"]
				players[nombre].dic["posx"]=dic1["posx"]
				players[nombre].dic["posy"]=dic1["posy"]
				players[nombre].dic["personaje"]=dic1["personaje"]
			if action=="mapeo":
				players[nombre].dic["fondo"]=dic1["mapa"]
			multicast(socket_clients,id_client,players,action,dic1,len(players)-1)		
		
		#if action == "morphing":
		#	dic4=json.loads(socket_clients.recv())
		#	multicast(socket_clients,players,action,dic4)	
			
    
