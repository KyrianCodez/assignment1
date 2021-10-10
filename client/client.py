"""
    Name: Egan Hernandez and Kyle 
    Description: Client sends a string array to server
    Language: Python 3.9.7
"""
from socket import *
import os.path
#USED TO VALIDATE INPUT FROM USER
def validateInput(uInput):
    
    # if(any(uInput.isdigit()) == True):
    #    return print("Numbers should not be included")
        
    words = uInput.split()
    words[0].casefold()
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
    #checks command entered after validation checks return valid
    
    #put
    if(cmd == 'put'):
        if(validateFile(file) == False):
            return print('File does not exist! Check spelling!')
        
        message = readFromFile(file)
        s.send(bytes(file,'UTF-8'))
        s.send(bytes(message, 'UTF-8'))
        print('Sent Message to server')
        print(input("Type any key to continue..."))
    #end put
    
    #create
    elif(cmd == 'create'):
        # if(validateFile(file) == True):
        #     return print('File already exists')
        message = print(input("Enter file contents: \n"))
        s.send(bytes(file,'UTF-8'))
        s.send(bytes(message, 'UTF-8'))
        print('Awaiting server response....')
        print(input("Type any key to continue..."))
        
    #end create
        
        
        
    
def MainCode():
    cmd = '0'
    s = socket(AF_INET, SOCK_STREAM)
    host = gethostbyname('127.0.0.1')
    port = 20007
    server_addr = (host, port)
    s.connect(server_addr)
    while(cmd != 'exit'):
        printMenu()
        decision(s)
    


MainCode()
