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
		response = os.listdir(bytes(b"."))
		response = str(response)
		c.send(bytes(response, 'UTF-8'))
		print('List of files in directory sent.\n')
		c.close()
	elif(message['cmd'] == 'show'):
		print('Command received.')
		if(validateFile(message['file']) == False):
			response = 'File does not exist on server'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		content = readFromFile(message['file'])
		print(content)
		c.send(bytes(content, 'UTF-8'))
		c.close()
		return
			
	elif(message['cmd'] == 'delete'):
		print('Command received.')
		if(validateFile(message['file']) == False):
			response = 'File does not exists on server'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		name, extension = os.path.splitext()
		if(extension == '.txt'):
			response = 'File found'
			print(response)
			print('Deleting file...')
			c.send(bytes(response, 'UTF-8'))
			os.remove(message['file'])
			confirmation = 'File deleted'
			print(confirmation)
			c.send(bytes(confirmation, 'UTF-8'))
			c.close()
			return
		response = 'File type incorrect'
		print(response)
		c.send(bytes(response, 'UTF-8'))
		c.close()
		return
		
	elif(message['cmd'] == 'wordcount'):
		print('Command received.')
		if(validateFile(message['file']) == False):
			response = 'File does not exist on server'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			c.close()
			return
		name = message['file']
		print(message['file'])
		print(name)
		content = readFromFile(message['file'])
		words = len(content.split())
		wordstring = str(words)
		print('Wordcount: '+wordstring)
		c.send(bytes(wordstring, 'UTF-8'))
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
		c.settimeout(None)
		contents = readFromFile(message['file'])
		index = contents.find(search.decode())
		search = search.decode()
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
