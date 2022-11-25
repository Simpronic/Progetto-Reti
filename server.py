from socket import *
import matplotlib.pyplot as plt
import threading
import numpy as np
import datetime
from Model import  *
from  enum import Enum

class Prediction(Enum):
    books = 0
    film = 1
    music = 2

class Person_data:
    def __init__(self,name):
        self.id = name
        self.music = 0
        self.books = 0
        self.film = 0
    def increaseMusic(self,n):
        self.music += n
    def increaseBook(self,n):
        self.books += n
    def increaseFilm(self,n):
        self.film += n
    def changeId(self,name):
        self.id = name
        
class PhraseBuffer:
    mess_id = ""
    message = ""
    hasSpace = 1
    hasMessage = 0
    cv_to_wait = threading.Condition()

buffer = PhraseBuffer()
Connection_threads = []
Utility_Thread = []
clients = []
people = []

def searchByName(name):
    trovato = False
    i = 0
    person_array = [] #Nel caso ci siano omonimi
    while (i<len(people)):
        if(people[i].id == name):
            person = people[i]
            trovato = True
            person_array.append(person)
        i +=1
    if not trovato:
        return None
    else:
        return person_array
    
def createStatisticGraph():
    print("Sintassi comando: makeHisto id")
    person = Person_data("NONAME")
    while 1: 
        command = input()
        splitted_command = command.split()
        if(len(splitted_command) != 2):
            if(splitted_command[0] == "help" or splitted_command[0] == "HELP"):
                print("[HELP]: Sintassi comando: makeHisto id")
            else: 
                print("Invalid command")
        else:
            name = splitted_command[1]
            command = splitted_command[0]
            if(command == "makeHisto"):
                person = searchByName(name)
                if(person is None or len(person) == 0):
                    print("This person doesn't exist")
                else:
                    for p in person:
                        createStatistics(p)
                    
def createStatistics(person):
    objects = ['Music','Film','Books']
    x = [person.music,person.film,person.books]
    y = np.arange(len(objects))
    plt.bar(y,x,align='center', alpha=0.5)
    plt.xticks(y,objects)
    plt.title("Statistics of {}".format(person.id))
    plt.show()

def makePrediction(name,message):
        result = elaborazione(message)
        person = searchByName(name)
        print(Prediction.books.value)
        if result == Prediction.books.value:
            person[0].increaseBook(1)
        elif result == Prediction.film.value:
            person[0].increaseFilm(1)
        elif result == Prediction.music.value:
             person[0].increaseMusic(1)
        else:
            print('Errore nelle occorrenze!')
        print('Numero di occorrenze musica: ' + str(person[0].music))
        print('Numero di occorrenze film: ' + str(person[0].film))
        print('Numero di occorrenze libri: ' + str(person[0].books))
        #saveOnFile(person)


def PredictionHandler():
    while 1:
        buffer.cv_to_wait.acquire()
        if(not(buffer.hasMessage)):
          buffer.cv_to_wait.wait()
        makePrediction(buffer.message_id,buffer.message)
        buffer.hasMessage = 0
        buffer.hasSpace = 1
        buffer.cv_to_wait.notify()
        buffer.cv_to_wait.release()
        
def saveOnFile(Person_data):
    person = Person_data
    text_tw = '\n' + str(datetime.datetime.now()) + '\n' + 'name: ' + str(person.id) + '\n' + 'music occurences: ' + str(person.music) + '\n' + 'film occurences: ' + str(person.film) + '\n' +'books occurences:' + str(person.books)
    open('history.txt', 'a').write(text_tw)  
                    
def broadcast(message):
    print(message)
    for client in clients:
        client.send(message.encode())
        
def connectionHandler(threadName,connectionSocket,addr):
    try:
        connectionSocket.send("NAME".encode())
        name = connectionSocket.recv(1024).decode()
        person = Person_data(name)
        people.append(person)
        broadcast("{} has joined".format(name))
        connected = True
        while(connected):
            message = connectionSocket.recv(1024).decode()
            if message == "$exit$":
                connectionSocket.send("END".encode())
                broadcast("{} has left the chat".format(name))
                connected = False
            else:
                broadcast("{}: ".format(name)+message)
                buffer.cv_to_wait.acquire()
                if not(buffer.hasSpace):
                    buffer.cv_to_wait.wait()
                buffer.message = message
                buffer.message_id = name
                buffer.hasMessage = 1
                buffer.hasSpace = 0
                print("Notifico che ho finito")
                buffer.cv_to_wait.notify()
                buffer.cv_to_wait.release()
    except IOError:
        connectionSocket.close()


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #costruisco una socket TCP
serverSocket.bind(('',serverPort))
serverSocket.listen()
print("Ready to serve \n")
threadPrediction = threading.Thread(target=PredictionHandler)
threadGraphs = threading.Thread(target=createStatisticGraph)
threadGraphs.start()
threadPrediction.start()
while 1:
    connectionSocket, addr = serverSocket.accept()
    print("Connection established, creating new thread.....")
    newThread = threading.Thread(target=connectionHandler,args=(1,connectionSocket,addr))
    newThread.start()
    clients.append(connectionSocket)
    Connection_threads.append(newThread)
serverSocket.close()
sys.exit()





