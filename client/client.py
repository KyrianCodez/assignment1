"""
    Name: Egan Hernandez and Kyle 
    Description: Client sends a string array to server
    Language: Python 3.9.7
"""
from socket import *
import os.path
import json
#USED TO VALIDATE INPUT FROM USER
def validateInput(uInput):  
        
    words = uInput.split()
    if(len(words) == 1):
        print('uinput ',len(words))
        return uInput  
    
    words[0] = words[0].casefold()
    return words
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
#prints menu to console
def printMenu():
    options = '\n1. To send datafile to server location type PUT and name of datafile to send\n2. To create a new datafile type CREATE and the name of datafile.\n3. To see all files at server locatio, type LIST\n4. To see contents of a file at server location type SHOW and the name of the datafile.\n5. To remove a textfile from server location, type DELETE and the name of the textfile.\n6. To count the number of words in a file at server location type, WORDCOUNT and the name of the file.\n7. To see if a word exists in a file type, SEARCH and the word being queried\n8. To close connection, type EXIT'

    return print(options)
#handles entered options
def decision(s):
    #Accepts user input as string
    uInput = input()
    print("\n"+uInput)
    #calls validate input function
    valWords = validateInput(uInput)
    cmd = valWords[0]
    file = valWords[1]
    #declaring json object
    message = { 
            "cmd": '',
            "file": '',
            "text": '',
        }
    #put
    if(cmd == 'put'):
        if(validateFile(file) == False):
            return print('File does not exist! Check spelling!')
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
        print(input("Type any key to continue..."))
    #end put
    
    #create
    elif(cmd == 'create'):
        print("Enter file contents: \n")
        text = input()
        message['cmd'] = cmd
        message['file'] = file
        message['text'] = text
        message = bytes(json.dumps(message), 'UTF-8')
        s.send(message)
        print('Awaiting server response....')
        response = s.recv(4096)
        print("Response from server: " , response.decode())
        print(input("Type enter to continue..."))    
    #end create
        

    #list
    elif(cmd == 'list'):
        message['cmd'] = cmd
        message['file'] = file
        print('Sending request to server...')
        s.send(bytes(json.dumps(message), 'UTF-8'))
        print('Awaiting server response')
        response = s.recv(4096).decode()
        print('List of files in directory: \n'+ response)
    #endlist
    #show
    elif(cmd == 'show'):
        message['cmd'] == cmd
        message['file'] == file 
        print('Sending request to server...')
        s.send(bytes(json.dumps(message), 'UTF-8'))
        response = s.recv(4096).decode()
        if(response == 'File does not exist on server'):
            print('File not found.')
        print('File found.')
        content = s.recv(4096).decode()
        print('File contents: ')
        print(content)
    #delete
    elif(cmd == 'delete'):
        message['cmd'] == cmd
        message['file'] == file
        print('Sending server request...')
        #s.send(bytes(json.dumps(message), 'UTF-8'))
        message = bytes(json.dumps(message), 'UTF-8')
        s.send(message)
        response = s.recv(4096).decode()
        if(response == 'File does not exist on server'):
            print(response)
        elif(response == 'File found'):
            confirm = s.recv(4096).decode()
            print(confirm)
        elif(response == 'File type incorrect'):
            print(response)
    #wordcount
    elif(cmd == 'wordcount'):
        message['cmd'] = cmd
        message['file'] == file
        print('Sending server request...')
        message = bytes(json.dumps(message), 'UTF-8')
        s.send(message)
        response = s.recv(4096).decode()
        if(response == 'File does not exist on server'):
            print(response)
        elif():
            print('File: '+file)
            print('Wordcount: '+response)

    elif(cmd == 'search'):
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
