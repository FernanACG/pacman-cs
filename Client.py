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


	imagen=Recortar("pacmanS.png",6,4)

	#Pj.nriv = Clientes-1

	Corn = pg.image.load('corn.png')
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
				if ran >= 0:
					sb = Semilla(Seed)
					sb.rect.x = ne*32
					sb.rect.y = nf*32
					Semillas.add(sb)

			ne += 1
			#print ('Iteracion',enumf, enume)
		nf += 1
		ne = 0


	Bf1 = BuffoR(Corn)
	Bf1.rect.x = 1*32
	Bf1.rect.y = 1*32
	Buffosr.add(Bf1)

	Bf2 = BuffoR(Corn)
	Bf2.rect.x = 1*32
	Bf2.rect.y = 17*32
	Buffosr.add(Bf2)

	Bf3 = BuffoR(Corn)
	Bf3.rect.x = 33*32
	Bf3.rect.y = 1*32
	Buffosr.add(Bf3)

	Bf4 = BuffoR(Corn)
	Bf4.rect.x = 33*32
	Bf4.rect.y = 17*32
	Buffosr.add(Bf4)

	Bf5 = BuffoR(Corn)
	Bf5.rect.x = 17*32
	Bf5.rect.y = 7*32
	Buffosr.add(Bf5)

	players[idplayer] = Jugador(imagen,0,0, 17*32, 9*32)
	players[idplayer].muros = Muros
	players[idplayer].premios = Buffosr

	Personajes = pg.sprite.Group()
	Personajes.add(players[idplayer])


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
			players[usernameInBytes].premios = Buffosr
			Rivales.add(players[usernameInBytes])


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
				Rivales.add(players[ident])

			elif operation == b'user_change_position':
				ident = message[0]
				pos = eval(message[1].decode('ascii'))

				x = pos[0]
				y = pos[1]

				players[ident].setPos(x, y)

		except zmq.ZMQError as e:
			pass

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

					players[idplayer].setPos(x, y-16) # ubica la posicion en la que este

					players[idplayer].dir = 1
					players[idplayer].var_y = -5
					players[idplayer].var_x = 0
					bPOSPlayer = bytes(str(players[idplayer].GetPos()), 'ascii')
					Socket.send_multipart([b"changepos", bPOSPlayer])
					#Cambiar de direccion
				if event.key== pg.K_DOWN:
					x = players[idplayer].GetPos()[0]
					y = players[idplayer].GetPos()[1]

					players[idplayer].setPos(x, y+16)
					players[idplayer].dir = 3
					players[idplayer].var_y = 5
					players[idplayer].var_x = 0
					bPOSPlayer = bytes(str(players[idplayer].GetPos()), 'ascii') #
					Socket.send_multipart([b"changepos", bPOSPlayer])#
					#Cambiar de direccion
				if event.key== pg.K_LEFT:
					x = players[idplayer].GetPos()[0]
					y = players[idplayer].GetPos()[1]

					players[idplayer].setPos(x-16, y)

					players[idplayer].dir = 2
					players[idplayer].var_y = 0
					players[idplayer].var_x = -5
					bPOSPlayer = bytes(str(players[idplayer].GetPos()), 'ascii')
					Socket.send_multipart([b"changepos", bPOSPlayer])
					#Cambiar de direccion
				if event.key== pg.K_RIGHT:
					x = players[idplayer].GetPos()[0]
					y = players[idplayer].GetPos()[1]

					players[idplayer].setPos(x+16, y)

					players[idplayer].dir = 0
					players[idplayer].var_y = 0
					players[idplayer].var_x = 5
					bPOSPlayer = bytes(str(players[idplayer].GetPos()), 'ascii')
					Socket.send_multipart([b"changepos", bPOSPlayer])

				if event.key == pg.K_k:
					players[idplayer].GetPos()

						#Cambiar de direccion
			# if event.type == pg.KEYUP:
			# 	players[idplayer].var_y = 0
			# 	players[idplayer].var_x = 0

		#
		for Buffo in Buffosr:
			ls_bf = pg.sprite.spritecollide(Buffo, Personajes, False)
			for m in ls_bf:
				Buffosr.remove(Buffo)
				m.Buffado()
				if m.cont > 0:
					m.cont -= 1
				else:
					m.i = 3
					m.b = 3
					m.buff = False

			ls_bf = pg.sprite.spritecollide(Buffo, Rivales, False)
			for m in ls_bf:
				Buffosr.remove(Buffo)
				m.Buffado()
				if m.cont > 0:
					m.cont -= 1
				else:
					m.i = 3
					m.b = 3
					m.buff = False

		for Pj in Personajes:
			ls_se = pg.sprite.spritecollide(Pj, Semillas, True)

			if Pj.buff:
				ls_rc = pg.sprite.spritecollide(Pj, Rivales, True)
				for m in ls_rc:
					m.BajarVida()

		for Pj in Rivales:
			ls_ser = pg.sprite.spritecollide(Pj, Semillas, True)

			if Pj.buff:
				ls_rcr = pg.sprite.spritecollide(Pj, Personajes, True)
				for m in ls_rcr:
					m.BajarVida()


		Personajes.update()
		Rivales.update()
		Muros.draw(Pantalla)
		Mapping(fondo, mapa, interprete, Pantalla)
		Semillas.draw(Pantalla)
		Buffosr.draw(Pantalla)
		General.draw(Pantalla)
		Personajes.draw(Pantalla)
		Rivales.draw(Pantalla)
		# Rivales.draw(Pantalla)

		pg.display.flip()
		Reloj.tick(20)

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
