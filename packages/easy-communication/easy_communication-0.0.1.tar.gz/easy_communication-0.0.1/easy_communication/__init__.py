import socket
import pickle


"""
import threading

t = threading.Thread(target=worker)
		threads.append(t)
		t.start()
"""

END_SUFIX =  b"<end_data>"

class Server():
	def __init__(self, host="127.0.0.1", port=65432):
		self.host = host
		self.port = port
		self.__function = lambda x: x

	@property
	def handler(self):
		return self.__function


	@handler.setter
	def handler(self, value):
		self.__function = value

	def start(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((self.host, self.port))
			s.listen()
			while True:
				conn, addr = s.accept()
				self.__connection__(conn, addr)

	def __connection__(self, conn, addr):
		with conn:
			data = b''
			end = False
			while not end:
				data += conn.recv(1024)
				end = data.endswith(END_SUFIX)

			data = pickle.loads(data[:-len(END_SUFIX)])
			x = self.handler(data)
			x = pickle.dumps(x)+END_SUFIX
			conn.sendall(x)

def send_data(data, host="127.0.0.1", port=65432):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))

		data = pickle.dumps(data)+END_SUFIX
		s.sendall(data)
		
		data = b''
		end = False
		while not end:
			data += s.recv(1024)
			end = data.endswith(END_SUFIX)
		data = pickle.loads(data[:-len(END_SUFIX)])
		return data

if __name__ == '__main__':
	s = Server()
	def echo(x):
		print(x)
	s.handler = echo
	s.start()