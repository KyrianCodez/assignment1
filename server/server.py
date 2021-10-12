"""
	Name: Egan Hernandez and Kyle Macintosh 
	Description:  
	Language: Python 3.9.7
"""

from os import path
from socket import *
import os.path
import json
import sys

#Returns false if file does not exist
def validateFile(file):
   
	return os.path.isfile(file)
#Reads data from file into a string variable
def readFromFile(file):
	inFile = open(file, 'rb')
	message = inFile.read()
	message = str(message, 'UTF-8')
	inFile.close()
	return message	
def writeToFile(file, message):
	outFile = open(file, 'wb')
	outFile.write(bytes(message, 'UTF-8'))
	outFile.close()
def handleCommand(s):
	#accepts connection from client and stores client instance information
	c, addr = s.accept()
	print('Received Connection from: ' + str(addr))
	print('Waiting on message ... \n')
	message = c.recv(4096)
	if not message:
		print('No data recieved. Closing outstanding connection!')
		c.close()
		return
	message = json.loads(message)

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
			response = 'File already exists'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		writeToFile(message['file'], message['text'])
		response = "File: "+ message['file'] + ' created successfully!'
		print(response)	
		c.send(bytes(response, 'UTF-8'))
		c.close()
	elif(message['cmd'] == 'list'):
		print('Command received.')
		response = os.listdir(".")
		response = str(response)
		c.send(bytes(response, 'UTF-8'))
		print('List of files in directory sent.\n')
		c.close()
	elif(message['cmd'] == 'show'):
		print('Command received.')
		if(validateFile(message['file']) == False):
			response = '404'
			print(response)
			c.send(bytes(response, 'UTF-8'))
		
			c.close()
			return
		response = readFromFile(message['file'])
		print(response)
		c.send(bytes(response, 'UTF-8'))
		c.close()
			
	elif(message['cmd'] == 'delete'):
		if(validateFile(message['file']) == False):
			response = '404'
			print('File does not exist')
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		print('File found\nDeleting file...')
		try:
			os.remove(message['file'])
			confirmation = 'File '+message['file']+' has been removed successfully'
			print(confirmation)
			c.send(bytes(confirmation, 'UTF-8'))
			c.close()
			return
		except OSError as e:
			print(e)
			error = bytes(e,'UTF-8')
			c.send(error)
			c.close()
			return
		
	elif(message['cmd'] == 'wordcount'):
	
		if(validateFile(message['file']) == False):
			response = '404'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		print(message['file'])
		content = readFromFile(message['file'])
		words = len(content.split())
		words = str(words)
		print('Wordcount: ', words)
		c.send(bytes(words, 'UTF-8'))
		c.close()
		return


	elif(message['cmd'] == 'search'):
		if(validateFile(message['file']) == False):
			response = 'File does not exists on server'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		response = 'Enter search term: \n'
		c.send(bytes(response, 'UTF-8'))
		print('Awaiting response from client...')
		c.settimeout(60.0)
	
		search = c.recv(4096)
		search = search.decode()
		c.settimeout(None)
		contents = readFromFile(message['file'])
		index = contents.find(search)
		
		if(index == -1):
			response = search+' is not in '+message['file']
			print(response)
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		response = 'Term: '+search+' found in file '+message['file']+' at index '+str(index)
	
		print(response)
		c.send(bytes(response, 'UTF-8'))
		c.close()
		return
	elif(message['cmd']=='exit'):
	
		response = "I'm sorry Dave I can't let you do that.(2001 space oddessey) Just kidding Shutting down."
		c.send(bytes(response, 'UTF-8'))
		sys.exit(response)
		
		
			
				
	
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
