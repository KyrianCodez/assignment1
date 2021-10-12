"""
	Name: Egan Hernandez and Kyle 
	Description: Client sends a string array to server
	Language: Python 3.9.7
"""
from socket import *
import os.path
import json
import sys
#USED TO VALIDATE INPUT FROM USER
def validateInput(uInput):  
		
	words = uInput.split()    
	words[0] = words[0].casefold()
	return words
#Returns false if file does not exist
def validateFile(file):
	return os.path.isfile(file)
def checkFile(file):
	if(validateFile(file) == False):
		print('File does not exist! Check spelling!')
		print(input("Press enter to continue..."))
	return 
#Reads data from file into a string variable
def readFromFile(file):
	inFile = open(file, 'rb')
	message = inFile.read()
	message = str(message, 'UTF-8')
	inFile.close()
	return message
#prints menu to console
def printMenu():
	options = '\n1. To send datafile to server location type PUT and name of datafile to send\n2. To create a new datafile type CREATE and the name of datafile.\n3. To see all files at server locatio, type LIST\n4. To see contents of a file at server location type SHOW and the name of the datafile.\n5. To remove a textfile from server location, type DELETE and the name of the textfile.\n6. To count the number of words in a file at server location type, WORDCOUNT and the name of the file.\n7. To see if a word exists in a file type, SEARCH and the word being queried\n8. To close connection, type EXIT'

	return print(options)
#handles entered options
def handleInput():
	  #Accepts user input as string
	uInput = input()
	if not uInput:
		return 401
	print("\n"+uInput)
	#calls validate input function
	valWords = validateInput(uInput)
	return valWords
def handleEmptyFile(file): 
	if not file:
		print("Error: No file specified!")
		print(input("Press enter to continue..."))
		return
  
def decision(s):
	valWords = handleInput()
	if(valWords == 401):
		print('No command entered. Please choose an option from the list.')
		print(input("Press enter to continue..."))
		return
	file = ''
	if(len(valWords) == 2):
		file = valWords[1] 
	cmd = valWords[0]
   
	#declaring json object
	message = { 
			"cmd": '',
			"file": '',
			"text": '',
		}

	#put
	if(cmd == 'put'):
		handleEmptyFile(file)
		checkFile(file)
		text = readFromFile(file)
		 #using json to simplify data for sending and processing
		message['cmd'] = cmd
		message['file'] = file
		message['text'] = text
		message = bytes(json.dumps(message), 'UTF-8')
		s.send(message)
		print('Awaiting response...')
		response = s.recv(4096)
		print("Response from server: ", response.decode())
		print(input("Press enter to continue..."))
	#end put
	
	#create
	elif(cmd == 'create'):
		handleEmptyFile(file)
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
		handleEmptyFile(file)
		print('cmd is:', cmd)
		message['cmd'] = cmd
		message['file'] = file 
		print('Sending request to server...\n')
		s.send(bytes(json.dumps(message), 'UTF-8'))
		response = s.recv(4096).decode()
		if(response == '404'):
			print('Response from server: ','File not found.')
			print(input("Press enter to continue...")) 
			return
		print('File found.')
		print('Response from server: ',response)
		print(input("Press enter to continue...")) 
	#delete
	elif(cmd == 'delete'):
		handleEmptyFile(file)
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
		handleEmptyFile(file)
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
	elif(cmd == 'search'):
		handleEmptyFile(file)
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
	elif(cmd == 'exit'):
		message['cmd'] = cmd
		message = bytes(json.dumps(message), 'UTF-8')
		s.send(message)
		print('Closing connection...\n')
		response = s.recv(4096).decode()
		print('Response from server: ', response)
		print(input("Press enter to close.")) 
		sys.exit()
	else:
		print('Incorrect option. Please only choose an option that is listed')

		

		
		
	
def MainCode():
	cmd = '0'
	while(cmd != 'exit'): 
		s = socket(AF_INET, SOCK_STREAM)
		host = gethostbyname('127.0.0.1')
		port = 20007
		server_addr = (host, port)
		s.connect(server_addr)
		printMenu()
		decision(s)
	


MainCode()
