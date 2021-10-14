"""
	Name: Egan Hernandez (816028176) and Kyle Macintosh (816023362) 
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
	#whites message into file. Creates the file if it doesn't exist	
def writeToFile(file, message):
	outFile = open(file, 'wb')
	outFile.write(bytes(message, 'UTF-8'))
	outFile.close()
	#handles all processing for server application
def handleCommand(c):
    #recieves data from  client to populate json 
	message = c.recv(4096)
	#Checks if json object has data exits to head of loop if not
	if not message:
		print('No data recieved. Closing outstanding connection!')
		c.close()
		return
	#decodes json data into string readable format
	message = json.loads(message)
	#process put command
	if(message['cmd'] == 'put'):
		print('File Received: \n' + message['file'] + '\n')
		print('Text recieved: \n' + message['text'] + '\n')
		#calls write to file func
		writeToFile(message['file'], message['text'])
		response = "File: "+ message['file'] + ' recieved successfully!'
		print(response)
		#send server response to client
		c.send(bytes(response, 'UTF-8'))
		return
		#process create command
	elif(message['cmd'] == 'create'):
		#checks if file already exists. sends a response to client and exits code block if it does 
		if(validateFile(message['file']) == True):
			response = 'File already exists'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			 
			return
		writeToFile(message['file'], message['text'])
		response = "File: "+ message['file'] + ' created successfully!'
		print(response)	
		c.send(bytes(response, 'UTF-8'))
	#processes list command	 
	elif(message['cmd'] == 'list'):
		print('Command received.')
		#calls os function to check andlist all files in directory '.'
		response = os.listdir(".")
		#stringifies response from os.listdir
		response = str(response)
		c.send(bytes(response, 'UTF-8'))
		print('List of files in directory sent.\n')
		return
	#processing for show command show
	elif(message['cmd'] == 'show'):
		print('Command received.')
		if(validateFile(message['file']) == False):
			response = '404'
			print(response)
			c.send(bytes(response, 'UTF-8')) 
			return
		response = readFromFile(message['file'])
		print(response)
		c.send(bytes(response, 'UTF-8'))
		 
	#processing for show command delete		
	elif(message['cmd'] == 'delete'):
		if(validateFile(message['file']) == False):
			response = '404'
			print('File does not exist')
			c.send(bytes(response, 'UTF-8'))
			 
			return
		print('File found\nDeleting file...')
		try:
			#calls os remove function to remove file sent
			os.remove(message['file'])
			confirmation = 'File '+message['file']+' has been removed successfully'
			print(confirmation)
			c.send(bytes(confirmation, 'UTF-8'))
			 
			return
		#catch error on deleting file
		except OSError as e:
			print(e)
			error = bytes(e,'UTF-8')
			c.send(error)
			 
			return
	#end delete
	# wordcount	
	elif(message['cmd'] == 'wordcount'):
	
		if(validateFile(message['file']) == False):
			response = '404'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			 
			return
		print(message['file'])
		content = readFromFile(message['file'])
		words = len(content.split())
		words = str(words)
		print('Wordcount: ', words)
		c.send(bytes(words, 'UTF-8'))
		 
		return
	#end wordcount
	#search

	elif(message['cmd'] == 'search'):
		if(validateFile(message['file']) == False):
			response = 'File does not exists on server'
			print(response)
			c.send(bytes(response, 'UTF-8'))
			 
			return
		response = 'Enter search term: \n'
		c.send(bytes(response, 'UTF-8'))
		print('Awaiting response from client...')
		
	
		search = c.recv(4096)
		search = search.decode()
	
		contents = readFromFile(message['file'])
		index = contents.find(search)
		
		if(index == -1):
			response = search+' is not in '+message['file']
			print(response)
			c.send(bytes(response, 'UTF-8'))
			 
			return
		response = 'Term: '+search+' found in file '+message['file']+' at index '+str(index)
	
		print(response)
		c.send(bytes(response, 'UTF-8'))
		 
		return
		#end search
		#exit
	elif(message['cmd']=='exit'):
	
		response = "I'm sorry Dave I can't let you do that.(2001 space oddessey) Just kidding Shutting down."
		c.send(bytes(response, 'UTF-8'))
		c.close()
		sys.exit(response)
	#end exit
	 
	
		
			
				
	
def MainCode():


	s = socket(AF_INET, SOCK_STREAM)
	host = gethostbyname('127.0.0.1')
	port = 20007
	host_addr = (host, port)
	s.bind(host_addr)
	s.listen(10) ##the listen backlog is a socket setting telling the kernel how to limit the number of outstanding (as yet unaccapted) connections in the listen queue of a listening socket
	live = True
	print('Server Started \nWaiting on connection...')
	c, addr = s.accept()
	print('Received Connection from: ' + str(addr))
	print('Waiting on message ... \n')
	
	# if not message:
	# 	print('No data recieved. Closing outstanding connection!')
	# 	return 
	
	while live == True:
		handleCommand(c)
	
MainCode()
