import zmq
import sys


def broadcast(socket, players, ident, msg):
	for username in players:
		if username != ident:
			socket.send_multipart([username]+msg)

def main():

	UsersConnected = {}

	context=zmq.Context()
	socket=context.socket(zmq.ROUTER)
	socket.bind("tcp://*:6666")

	poller= zmq.Poller()
	poller.register(socket, zmq.POLLIN)

	while True:
		socks= dict(poller.poll())

		if socket in socks:
			ident, operation, *Mensaje = socket.recv_multipart()

			if operation == b"hello":
				socket.send_multipart([ident, bytes(str(UsersConnected), 'ascii')])
				# print(Mensaje[0])
				UsersConnected[ident] = eval(Mensaje[0].decode('ascii'))

				dataToSend = [b'new_user', ident] + Mensaje
				broadcast(socket, UsersConnected, ident, dataToSend)

			if operation == b"changepos":
				UsersConnected[ident] = eval(Mensaje[0])
				dataToSend = [b'user_change_position', ident, Mensaje[0]]

				broadcast(socket, UsersConnected, ident, dataToSend)

if __name__ == '__main__':
	main()
