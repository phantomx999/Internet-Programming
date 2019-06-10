import socket
import os
import sys
import stat
import datetime
import urllib.parse

from threading import Thread
from argparse import ArgumentParser

BUFSIZE = 4096

NEWLINE = '\r\n'
OK_MESSAGE = 'HTTP/1.1 200 OK{}{}{}'.format(NEWLINE, NEWLINE,NEWLINE)
MOVED_MESSAGE = 'HTTP/1.1 301 MOVED LOCATION.  LOCATION: http://www.cs.umn.edu/{}'.format(NEWLINE)
FORBIDDEN_MESSAGE = 'HTTP/1.1 403 FORBIDDEN REQUEST{}'.format(NEWLINE)
NOT_FOUND_MESSAGE = 'HTTP/1.1 404 NOT FOUND{}'.format(NEWLINE)
NOT_ALLOWED_MESSAGE = 'HTTP/1.1 405 METHOD NOT ALLOWED{}'.format(NEWLINE)
NOT_ACCEPTED_MESSAGE = 'HTTP/1.1 406 METHOD NOT ALLOWED{}{}{}'.format(NEWLINE, NEWLINE, NEWLINE)

def permission_check(resource):
    stmode = os.stat(resource).st_mode
    return (getattr(stat, 'S_IROTH') & stmode) > 0
	
class myServer:
	def __init__(self, host, port):
		print("Listening on port {}", format(port))
		self.host = host
		self.port = port
		
		self.initialize_socket()
		
		self.accept()
		
		self.sock.shutdown(1)
		self.sock.close()	
	
	def head_call(self, head):
		path = os.path.join('.', head)
		if (head == 'csumn'):
			ret = MOVED_MESSAGE
		elif not os.path.exists(head):
			ret = NOT_FOUND_MESSAGE
		elif not permission_check(head):
			ret = FORBIDDEN_MESSAGE
		else:
			ret = OK_MESSAGE
		return ret

	def check_forbidden(self, resource):
			file = open('403.html', 'rb')
			content = file.read()
			file.close()
			response = self.head_call(resource)
			response = response.rstrip('\r\n')
			response = response + "\r\nContent-Type: text/html\r\n" + "\r\n<!DOCTYPE html>\n" + content.decode('utf-8')
			print("reponse in 403 = " + response)
			return response

	def get_call(self, host, port, resource, type_file, client_sock):
		path = os.path.join('.', resource)
		print("path equals: " + path)
		if(resource == 'private.html'):
			return self.check_forbidden(resource)
		if os.path.exists(path):
			file = open(path, 'rb')
			content = file.read()
			file.close()
			header = self.head_call(resource)
			if(header == OK_MESSAGE):
				head = header.rstrip('\r\n')
				response = head
				if(type_file[1] == 'html' or type_file[1] == 'htm'):
					response += "\r\nContent-Type: text/html\r\n" + NEWLINE 
					response = response + content.decode('utf-8')
					print("reponse in 200 = " + response)
					return response
				elif(type_file[1] == 'png'):
					response += "\r\nContent-Type: image/png\r\n" + NEWLINE
					client_sock.send(bytes(response, 'utf-8'))
					client_sock.send(content)
					return ''
				elif(type_file[1] == 'mp3'):
					response += "\r\nContent-Type: audio/mpeg\r\n" + NEWLINE
					client_sock.send(bytes(response, 'utf-8'))
					client_sock.send(content)
					return response
				elif(type_file[1] == 'mp4'):				
					response += "\r\nContent-Type: video/mp4\r\n" + NEWLINE
					client_sock.send(bytes(response, 'utf-8'))
					client_sock.send(content)
					return response
				else:
					return self.check_forbidden(resource)
			else:
				return header
		else:
			#return ''
			#head = NOT_FOUND_MESSAGE
			head = OK_MESSAGE
			response = head.rstrip('\r\n')
			file = open('404.html', 'rb')
			content = file.read()
			file.close()
			response = response + "\r\nContent-Type: text/html\r\n" + "\r\n<!DOCTYPE html>\n" + content.decode('utf-8')
			print("reponse in 404 = " + response)
			return response

	def parse_data(self, data, client_sock):
		list_of_lines = data.strip().split(NEWLINE)
		first_line = list_of_lines[0].split()
		resource = first_line[1][1:]
		print("resource = " + resource)
		if(len(first_line[0]) == 0):
			return ''
		elif(first_line[0] == 'HEAD'):
			return self.head_call(resource) 
		elif(first_line[0] =='GET'):
			if(resource == '/favicon.ico' or resource == 'favicon.ico'):
				print("made it here2323232")
				return ''
			type_file = resource.split('.')
			print("made it hereaefavfafgvagfagfagfag")
			return self.get_call(self.host, self.port, resource, type_file, client_sock)
		elif(first_line[0] == 'POST'):
			return post_call(resource)
		else:
			return NOT_ALLOWED_MESSAGE	
		
	def read_request(self, client_sock, client_addr):
		print("Talking to {}", format(client_addr))
		print("Accepting Request")
		input = client_sock.recv(BUFSIZE)
		data = input.decode('utf-8')
		print("\n###########################")
		print(data)
		print("###########################\n\n\n")
		if(data != ''):
			response = self.parse_data(data, client_sock)
			if(response != ''):
				client_sock.send(bytes(response, 'utf-8'))
		client_sock.shutdown(1)
		client_sock.close()
		print("Connection closed")
		print("Client send another request or 'ctrl-z' to end server program") 
		
	def initialize_socket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.host, self.port))
		self.sock.listen(5)
		
	def accept(self):
		while True:
			(client, address) = self.sock.accept()
			print("Connected to:", address)
			th = Thread(target=self.read_request, args=(client, address))
			th.start()
			
def parse_args():
  parser = ArgumentParser()
  parser.add_argument('--host', type=str, default='localhost', help='specify host to operate on (default=localhost)')
  parser.add_argument('-p', '--port', type=int, default=9001, help='specify port to operate on (default=9001)')
  args = parser.parse_args()
  return (args.host, args.port)
  

if __name__ == '__main__':
	(host, port) = parse_args()
	myServer(host, port)
