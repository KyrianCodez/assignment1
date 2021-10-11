"""
	Name: Egan Hernandez and Kyle Macintosh 
	Description:  
	Language: Python 3.9.7
"""

from os import path
from socket import *
import os.path
import json
#Returns false if file does not exist
def validateFile(file):
   
	return os.path.isfile(file)
#Reads data from file into a string variable
def writeToFile(file, message):
	outFile = open(file, 'wb')
	outFile.write(bytes(message, 'UTF-8'))
	outFile.close()
def handleCommand(s):
	#accepts connection from client and stores client instance information
	c, addr = s.accept()
	print('Received Connection from: ' + str(addr))
	print('Waiting on message ... \n')
	message = json.loads(c.recv(4096))
	
	# message = str(message, 'UTF-8') ##Unicode Transformation Format (UTF) - HTML 5 uses this standard
	if(message['cmd'] == 'put'):
		print('File Received: \n' + message['file'] + '\n')
		print('Text recieved; \n' + message['text'] + '\n')
		writeToFile(message['file'], message['text'])
		response = "File: "+ message['file'] + ' recieved successfully!'
		print(response)
		c.send(bytes(response, 'UTF-8'))
		c.close()
		
	elif(message['cmd'] == 'create'):
		if(validateFile(message['file']) == True):
			return print('File already exists')
		writeToFile(message['file'], message['text'])
		response = "File: "+ message['file'] + ' created successfully!'
		print(response)	
		c.send(bytes(response, 'UTF-8'))
		c.close()
	
def MainCode():


	s = socket(AF_INET, SOCK_STREAM)
	host = gethostbyname('127.0.0.1')
	port = 20007
	host_addr = (host, port)
	s.bind(host_addr)
	s.listen(10) ##the listen backlog is a socket setting telling the kernel how to limit the number of outstanding (as yet unaccapted) connections in the listen queue of a listening socket
	print('Server Started \nWaiting on connection...')
	handleCommand(s)
	
n = 0	
while(n == 0):
	MainCode()
