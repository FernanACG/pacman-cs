import pygame as pg
import zmq
import sys
import random
import configparser as cp
from Clases import *
from Funciones import *

Ancho = 32 * 35
Alto = 32 * 19

def lobby(Mensaje):

	waiting = True
	while waiting:
		if int(Mensaje) > 1:
			waiting = False
			main(Mensaje)
		else:
			last()


def main(idplayer):

	Pantalla = pg.display.set_mode([Ancho, Alto])
	bIDPPlayer = bytes(idplayer, 'ascii')
	players = {}


	imagen=Recortar("pacmanR.png",3,4)

	players[idplayer] = Jugador(imagen,0,0, 550, 400)

	Personajes = pg.sprite.Group()
	Personajes.add(players[idplayer])
	#Pj.nriv = Clientes-1

	Corn = pg.image.load('corn.png')
	Corn = pg.transform.scale(Corn, (32,41))
	Seed = pg.image.load('seed.png')

	Archivo = "Mapa.map"
	interprete = cp.ConfigParser()
	interprete.read(Archivo)
	mapa = interprete.get('Nivel1','mapa')
	mapa = mapa.split('\n')
	fondo = Recortar('terrenogen.png', 32, 12)



	Muros = pg.sprite.Group()
	Buffosr = pg.sprite.Group()
	Semillas = pg.sprite.Group()
	nf = 0
	for enumf, f in enumerate(mapa):
		ne = 0
		for enume, e in enumerate(f):
			m = int(interprete.get(e, 'col'))
			if m == 1:
				mb = Muro()
				mb.rect.x = ne*32
				mb.rect.y = nf*32
				Muros.add(mb)
			else:
				if enumf == 16 and enume > 2 and enume < 32:
					ne += 1
					continue
				if enumf == 17 and enume > 1 and enume < 34 :
					ne += 1
					continue
				ran = random.randint(0,100)
				if ran < 3:
					Bf1 = BuffoR(Corn)
					Bf1.rect.x = ne*32
					Bf1.rect.y = nf*32
					Buffosr.add(Bf1)
				else:
					sb = Semilla(Seed)
					sb.rect.x = ne*32
					sb.rect.y = nf*32
					Semillas.add(sb)
			ne += 1
			#print ('Iteracion',enumf, enume)
		nf += 1
		ne = 0


	players[idplayer].muros = Muros

#---------------------------------------------#

	General = pg.sprite.Group()
	Rivales = pg.sprite.Group()

	Marco = Bloque()
	Marco.x = 750
	Marco.y = 350
	General.add(Marco)

	bPOSPlayer = bytes(str(players[idplayer].GetPos()), 'ascii')
	Socket.send_multipart([b"hello", bPOSPlayer])

	player = Socket.recv_multipart()
	playersConnected = eval(player[0])

	x = 550
	y = 400

	for usernameInBytes in playersConnected:
		if usernameInBytes != bIDPPlayer:
			posplayer=playersConnected[usernameInBytes]

			x = posplayer[0]
			y = posplayer[1]

			players[usernameInBytes] = Jugador(imagen,0,0, x, y)
			players[usernameInBytes].muros = Muros
			Personajes.add(players[usernameInBytes])
	Running=True

	while Running:

		try:
			operation, *message = Socket.recv_multipart(zmq.NOBLOCK)

			if operation == b'new_user':
				ident = message[0]
				pos = eval(message[1].decode('ascii'))

				x = pos[0]
				y = pos[1]

				players[ident] = Jugador(imagen,0,0, x, y)
				players[ident].muros = Muros
				Personajes.add(players[ident])

			# print(operation, message)
		except zmq.ZMQError as e:
			pass

		bPOSPlayer = bytes(str(players[idplayer].GetPos()), 'ascii')
		for event in pg.event.get(): # Cierre
			if event.type == pg.QUIT:
				Running = False
				break
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					Running = False

				if event.key == pg.K_UP:
					x = players[idplayer].GetPos()[0]
					y = players[idplayer].GetPos()[1]

					players[idplayer].setPos(x, y-10)

					players[idplayer].dir = 1
					players[idplayer].var_y = -5
					players[idplayer].var_x = 0
					Socket.send_multipart([b"changepos", bIDPPlayer, bPOSPlayer])
					#Cambiar de direccion
				if event.key== pg.K_DOWN:
					x = players[idplayer].GetPos()[0]
					y = players[idplayer].GetPos()[1]

					players[idplayer].setPos(x, y+10)

					players[idplayer].dir = 3
					players[idplayer].var_y = 5
					players[idplayer].var_x = 0
					Socket.send_multipart([b"changepos", bIDPPlayer, bPOSPlayer])
					#Cambiar de direccion
				if event.key== pg.K_LEFT:
					x = players[idplayer].GetPos()[0]
					y = players[idplayer].GetPos()[1]

					players[idplayer].setPos(x-10, y)

					players[idplayer].dir = 2
					players[idplayer].var_y = 0
					players[idplayer].var_x = -5
					Socket.send_multipart([b"changepos", bIDPPlayer, bPOSPlayer])
					#Cambiar de direccion
				if event.key== pg.K_RIGHT:
					x = players[idplayer].GetPos()[0]
					y = players[idplayer].GetPos()[1]

					players[idplayer].setPos(x+10, y)

					players[idplayer].dir = 0
					players[idplayer].var_y = 0
					players[idplayer].var_x = 5
					Socket.send_multipart([b"changepos", bIDPPlayer, bPOSPlayer])
				if event.key == pg.K_k:
					players[idplayer].GetPos()
					#Cambiar de direccion
			# if event.type == pg.KEYUP:
			# 	players[idplayer].var_y = 0
			# 	players[idplayer].var_x = 0

		#

		# Rivales.update()
		Muros.draw(Pantalla)
		Mapping(fondo, mapa, interprete, Pantalla)
		Semillas.draw(Pantalla)
		Buffosr.draw(Pantalla)
		General.draw(Pantalla)
		Personajes.draw(Pantalla)
		# Rivales.draw(Pantalla)

		pg.display.flip()
		Reloj.tick(60)

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print("Must be called with a player")
		print("Sample call: python ftclient <idplayer>")
		exit()

	idplayer = sys.argv[1]

	pg.init()
	Run=True

	FontS = pg.font.Font(None, 20)
	Pantalla2 = pg.display.set_mode([Ancho, Alto])

	context=zmq.Context()
	Socket=context.socket(zmq.DEALER)
	Socket.identity = bytes(idplayer, 'ascii')
	Socket.connect("tcp://localhost:6666")


	Reloj = pg.time.Clock()
	# while Run:
	# 	for event in pg.event.get(): # Cierre
	# 			if event.key == pg.K_e:
	# 				Socket.send_multipart(b"hola")
	# 				Mensaje=Socket.recv()
	# 				lobby(Mensaje)
	# 			if event.key == pg.K_ESCAPE:
	# 				Run=False
	# 				break

	main(idplayer)
