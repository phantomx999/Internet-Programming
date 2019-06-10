#!/usr/bin/env python3
# See https://docs.python.org/3.7/howto/sockets.html
# for a decscription of python socket and its parameters
# This program communicates at ISO-OSI level 6 - the socket layer
import socket

from threading import Thread
from argparse import ArgumentParser

BUFSIZE = 4096

#this is the function used to talk to the client
def client_talk(client_sock, client_addr):
    print('talking to {}'.format(client_addr))
    data = client_sock.recv(BUFSIZE)
    while data:
      print(data.decode('utf-8')) #print the data recieved from the client (encoded in utf-8)
      data = client_sock.recv(BUFSIZE)

    # clean up
    client_sock.shutdown(1)
    client_sock.close()
    print('connection closed.')

class EchoServer:
  def __init__(self, host, port):
    print('listening on port {}'.format(port))
    self.host = host
    self.port = port

    self.setup_socket()

    self.accept()

    self.sock.shutdown()
    self.sock.close()

  def setup_socket(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create internet streaming socket
    self.sock.bind((self.host, self.port)) #bind socket to host and port
    self.sock.listen(128) #queue up to 128 connect requests before refusing connections

  def accept(self):
    while True:
      (client, address) = self.sock.accept() #client is hostname or internet domain location, address is
                                             #port client is listening on
      th = Thread(target=client_talk, args=(client, address))#create a thread with client talk listening for
                                                             # messages from the client
      th.start() #start the thread

def parse_args():
  parser = ArgumentParser()
  parser.add_argument('--host', type=str, default='localhost',
                      help='specify a host to operate on (default: localhost)')
  parser.add_argument('-p', '--port', type=int, default=9001,
                      help='specify a port to operate on (default: 9001)')
  args = parser.parse_args()
  return (args.host, args.port)


if __name__ == '__main__':
  (host, port) = parse_args()
  EchoServer(host, port)

