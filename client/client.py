"""
	Name: Egan Hernandez (816028176) and Kyle Macintosh (816023362)
	Description: Client sends a string array to server
	Language: Python 3.9.7

"""
#used for socket connection
from socket import *
#used for referencing os paths
import os
#used for encoding and decoding dictionaries
import json
#used for shutting down of application
import sys
#splits input and changes command to lowercase
def validateInput(uInput):  	
	words = uInput.split()    
	words[0] = words[0].casefold()
	return words
#Returns false if file does not exist
def validateFile(file):
	return os.path.isfile(file)
#calls validate file
def checkFile(file):
	if(validateFile(file) == False):
		print('File does not exist! Check spelling!')
		print(input("Press enter to continue..."))
		return 404
	
#Reads data from file into a string variable
def readFromFile(file):
	inFile = open(file, 'rb')
	message = inFile.read()
	message = str(message, 'UTF-8')
	inFile.close()
	return message
#prints menu to console
def printMenu():
	options = '\n1. To send datafile to server location type PUT and name of datafile to send\n2. To create a new datafile type CREATE and the name of datafile.\n3. To see all files at server location, type LIST\n4. To see contents of a file at server location type SHOW and the name of the datafile.\n5. To remove a textfile from server location, type DELETE and the name of the textfile.\n6. To count the number of words in a file at server location type, WORDCOUNT and the name of the file.\n7. To see if a word exists in a file type, SEARCH and the word being queried\n8. To close connection, type EXIT'

	return print(options)
#handles entered options
def handleInput():
	  #Accepts user input as string
	uInput = input()
	#checks if any input was entered. returns an error code if empty.
	if not uInput:
		return 401
	print("\n"+uInput)
	#calls validate input function
	valWords = validateInput(uInput)
	return valWords
#error handling for not entering a file name where needed
def handleEmptyFile(file): 
	if not file:
		print("Error: No file specified!")
		print(input("Press enter to continue..."))
		return 401
#processes options
def decision(s):
	valWords = handleInput()
	#handles case if no input was entered.
	if(valWords == 401):
		print('No command entered. Please choose an option from the list.')
		print(input("Press enter to continue..."))
		return
	#declared file variable as empty string
	file = ''
	#checks if user entered one or two words. if 2 file is populated, else only cmd is populated.
	if(len(valWords) == 2):
		file = valWords[1] 
	cmd = valWords[0]
   
	#declaring json (dict) object. holds information for sending to server
	message = { 
			"cmd": '',
			"file": '',
			"text": '',
		}

	#put
	if(cmd == 'put'):
		if(handleEmptyFile(file) == 401):
			return	
		if (checkFile(file) == 404):
			return
		text = readFromFile(file)
		#assigning values to dictionary for sending and processing
		message['cmd'] = cmd
		message['file'] = file
		message['text'] = text
		#json.dumps is called to encode the object for transmission
		message = bytes(json.dumps(message), 'UTF-8')
		#object is sent to server
		s.send(message)
		print('Awaiting response...')
		#recieved server response
		response = s.recv(4096)
		#decode is called to decode byte form to string
		print("Response from server: ", response.decode())
		print(input("Press enter to continue..."))
	#end put
	
	#create
	elif(cmd == 'create'):
		if(handleEmptyFile(file) == 401):
			return
		#for case where its possible to send a filename without an extention
		path = file.split(".")
		
		if (len(path) == 1):
		
			print('No extension attached')
			print(input("Press enter to continue..."))
			return 	
		#populate text
		print("Enter file contents: \n")
		text = input()

		message['cmd'] = cmd
		message['file'] = file
		message['text'] = text
		message = bytes(json.dumps(message), 'UTF-8')
		s.send(message)
		print('Awaiting server response....')
		response = s.recv(4096)
		print("Response from server: " , response.decode() +'\n')
		print(input("Press enter to continue..."))    
	#end create
	#list
	elif(cmd == 'list'):
		message['cmd'] = cmd
		print('Sending request to server...\n')
		s.send(bytes(json.dumps(message), 'UTF-8'))
		print('Awaiting server response...]n')
		response = s.recv(4096).decode()
		print('List of files in directory: \n'+ response)
		print(input("Press enter to continue...")) 
	#endlist

	#show
	elif(cmd == 'show'):
    	#checks if file is empty
		if(handleEmptyFile(file) == 401):
			return
		message['cmd'] = cmd
		message['file'] = file 
		print('Sending request to server...\n')
		s.send(bytes(json.dumps(message), 'UTF-8'))
		response = s.recv(4096).decode()
		if(response == '404'):
			print('Response from server:','File not found.')
			print(input("Press enter to continue...")) 
			return
		print('File found.')
		print('Response from server:',response)
		print(input("Press enter to continue...")) 
	#delete
	elif(cmd == 'delete'):
    	
		if(handleEmptyFile(file) == 401):
			return	
		message['cmd'] = cmd
		message['file'] = file
		print('Sending server request...')
		message = bytes(json.dumps(message), 'UTF-8')
		s.send(message)
		response = s.recv(4096).decode()
		if(response == '404'):
			print('File not found.')
			print(input("Press enter to continue...")) 
			return
		print(response)
		print(input("Press enter to continue...")) 
		return
	#wordcount
	elif(cmd == 'wordcount'):
		if(handleEmptyFile(file) == 401):
			return	
		message['cmd'] = cmd
		message['file'] = file
		print('Sending server request...')
		message = bytes(json.dumps(message), 'UTF-8')
		s.send(message)
		response = s.recv(4096).decode()
		if(response == '404'):
			print('File does not exist on server')
			print(input("Press enter to continue...")) 
			return
		print('Response from server: ',file , 'contains', response, 'words')
		print(input("Press enter to continue...")) 
		return
	#end wordcount

	#search
	elif(cmd == 'search'):
		if(handleEmptyFile(file) == 401):
			return	
		message['cmd'] = cmd
		message['file'] = file
		message = bytes(json.dumps(message), 'UTF-8')
		s.send(message)
		print('Message sent to server...\n')
		print('Awaiting server response....\n')
		response = s.recv(4096)
		print("Response from server: " , response.decode())
		search = input()
		s.send(bytes(search, 'UTF-8'))
		print('Awaiting server response....')
		response = s.recv(4096)
		print("Response from server:" , response.decode() +'\n')
		response = s.recv(4096)
	#end search

	#exit
	elif(cmd == 'exit'):
		message['cmd'] = cmd
		message = bytes(json.dumps(message), 'UTF-8')
		s.send(message)
		print('Closing connection...\n')
		response = s.recv(4096).decode()
		print('Response from server: ', response)
		print(input("Press enter to close.")) 
		#shuts down program
		sys.exit()
	#end exit

	#catch cases that fall outside of listed commands
	else:
		print('Incorrect option. Please only choose an option that is listed')

		

		
		
	
def MainCode():
    
	loop = True
	# begin TCP socket connection 
	s = socket(AF_INET, SOCK_STREAM)
	#get host name
	host = gethostbyname('127.0.0.1')
	#get  port
	port = 20007
	#assign address
	server_addr = (host, port)
	#establish connection 
	s.connect(server_addr)
	#begin loop for taking instructions
	while(loop == True):
		printMenu()
		decision(s)
	


MainCode()
