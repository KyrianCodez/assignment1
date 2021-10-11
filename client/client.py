"""
    Name: Egan Hernandez and Kyle 
    Description: Client sends a string array to server
    Language: Python 3.9.7
"""
from socket import *
import os.path
import pickle
import json
#USED TO VALIDATE INPUT FROM USER
def validateInput(uInput):        
    words = uInput.split()
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
        print("Sending request to server...")
        s.send(bytes(cmd, 'UTF-8'))
        data = srecv(1024).decode
        print(data)
    
    


        

        
        
    
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
