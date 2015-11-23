import zmq
import json
import sys

class Player():
	def __init__(self,id_client,player,dic):
		self.id_client=id_client
		self.player="player"+str(player)
	 	self.dic=dic
	def Getid_client(self):
		return self.id_client

	def Getdic_nombre(self):
		return self.dic["nombre"]


def multicast(socket_clients,players,action,dic):
	i=0
	for addres in players:
		if dic["username"] != addres.dic["username"]:
			socket_clients.send_multipart([addres.Getid_client(),action,sys.argv[1]])
			while i <= (len(players)-1):
				if action == "connect":
					socket_clients.send_multipart([addres.Getid_client(),json.dumps(players[i].dic,sort_keys=True)])
				else:
					socket_clients.send_multipart([addres.Getid_client(),json.dumps(dic,sort_keys=True)])
				i+=1
			i=0





pos_init_x=600
pos_init_y=100
ctx = zmq.Context()
socket_clients = ctx.socket(zmq.XREP)
socket_clients.bind('tcp://*:5555')

number_players=int (sys.argv[1])


players=[]

poller = zmq.Poller()
poller.register(socket_clients, zmq.POLLIN)


while True:

	socks = dict(poller.poll())
	if socket_clients in socks and socks[socket_clients] == zmq.POLLIN:
		id_client=socket_clients.recv()
		action=socket_clients.recv()
		
		if action=="connect":
			username=socket_clients.recv()
			personaje=socket_clients.recv()
			dic={"username":username,"direc":4,"x":pos_init_x,"y":pos_init_y,"fondo":1,"personaje":personaje}
			gamer=Player(id_client,len(players)+1,dic)
			players.append(gamer)
			#personaje += 1
			pos_init_y += 100
			dic_aux={"username":""}
			if len(players) == number_players:
				multicast(socket_clients,players,action,dic_aux)
		else:
			dic1=json.loads(socket_clients.recv())
			multicast(socket_clients,players,action,dic1)		
		
		#if action == "morphing":
		#	dic4=json.loads(socket_clients.recv())
		#	multicast(socket_clients,players,action,dic4)	
			
    
