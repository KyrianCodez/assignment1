"""
	Name: Egan Hernandez and Kyle Macintosh 
	Description:  
	Language: Python 3.9.7
"""

from socket import *
import os.path

def writeToFile(file, message):
	outFile = open(file, 'wb')
	outFile.write(bytes(message, 'UTF-8'))
	outFile.close()

def MainCode():


	s = socket(AF_INET, SOCK_STREAM)
	host = gethostbyname('127.0.0.1')
	port = 20007
	host_addr = (host, port)
	s.bind(host_addr)
	s.listen(10) ##the listen backlog is a socket setting telling the kernel how to limit the number of outstanding (as yet unaccapted) connections in the listen queue of a listening socket
	print('Server Started \nWaiting on connection...')

	c, addr = s.accept()

	print('Received Connection from: ' + str(addr))
	print('Waiting on message ... \n')
	
	file = c.recv(4096) ## Receive up to 4096 bytes from a peer
	message = c.recv(4096) 
	file = str(file, 'UTF-8')
	message = str(message, 'UTF-8') ##Unicode Transformation Format (UTF) - HTML 5 uses this standard
	print('File Received: \n' + file + '\n')
	print('message recieved; \n' + message + '\n')
	writeToFile(file, message)
	print('file')

	print('Server Socket Closed \n')
n = 0	
while(n == 0):
	MainCode()
