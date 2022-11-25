from tkinter import *
from tkinter import messagebox
from socket import *
import threading

server = "192.168.1.54"
port = 12000
connectionSocket = socket(AF_INET, SOCK_STREAM)
connectionSocket.connect((server,port))
        
class GUI:

    def __init__(self):
        self.window = Tk()#istanzia una finestra vuote
        self.window.withdraw()#permette di nascondere una finestra 
        self.login = Toplevel()#istanza una finestra al lvello più in altro delle altre finestre
        self.login.title("Chat")
        self.login.resizable(width = False,  
                             height = False) 
        self.login.configure(width = 400, 
                             height = 300) 
        self.Title = Label(self.login,text = "Join in chat",
                                      justify = CENTER,
                                      font = "Helvetica 14 bold")
        self.subtitle = Label(self.login,text = "Insert the username",
                                         justify = CENTER,
                                         font = "Helvetica 14 bold")
        self.Title.place(relheight = 0.15, 
                           relx = 0.3,  
                           rely = 0.07)
        self.subtitle.place(relheight = 0.2,
                            relx = 0.3,
                            rely = 0.2)
        self.textBox = Entry(self.login,font = "Helvetica 14")
        self.textBox.place(relwidth = 0.4,  
                             relheight = 0.10, 
                             relx = 0.3, 
                             rely = 0.4)
        self.textBox.focus()
        self.go = Button(self.login, 
                         text = "CONTINUE",  
                         font = "Helvetica 14 bold",  
                         command = lambda: self.buttonClick(self.textBox.get())) #evento al click (usando le labda expression)
          
        self.go.place(relx = 0.4, 
                      rely = 0.55) 
        self.window.mainloop()

	
        
    def buttonClick(self,name): #funzione evento dopo il click del bottone 
            self.login.destroy()
            self.layout(name)
            rcv = threading.Thread(target=self.receiveMessage)
            rcv.start()
            
    def layout (self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chatroom")
        self.window.resizable(width = False, 
                              height = False)
        self.window.configure(width = 470, 
                              height = 550, 
                              bg = "#17202A")
        self.labelHead = Label(self.window, 
                             bg = "#17202A",  
                              fg = "#EAECEE", 
                              text = self.name , 
                               font = "Helvetica 13 bold", 
                               pady = 5) 
          
        self.labelHead.place(relwidth = 1) 
        self.line = Label(self.window, 
                          width = 450, 
                          bg = "#ABB2B9") 
          
        self.line.place(relwidth = 1, 
                        rely = 0.07, 
                        relheight = 0.012) 
          
        self.textCons = Text(self.window, 
                             width = 20,  
                             height = 2, 
                             bg = "#17202A", 
                             fg = "#EAECEE", 
                             font = "Helvetica 14",  
                             padx = 5, 
                             pady = 5) 
          
        self.textCons.place(relheight = 0.745, 
                            relwidth = 1,  
                            rely = 0.08) 
          
        self.labelBottom = Label(self.window, 
                                 bg = "#ABB2B9", 
                                 height = 80) 
          
        self.labelBottom.place(relwidth = 1, 
                               rely = 0.825) 
          
        self.entryMsg = Entry(self.labelBottom, 
                              bg = "#2C3E50", 
                              fg = "#EAECEE", 
                              font = "Helvetica 13") 
          
        # place the given widget 
        # into the gui window 
        self.entryMsg.place(relwidth = 0.74, 
                            relheight = 0.06, 
                            rely = 0.008, 
                            relx = 0.011) 
          
        self.entryMsg.focus() 
    
        self.buttonMsg = Button(self.labelBottom, 
                                text = "Send", 
                                font = "Helvetica 10 bold",  
                                width = 20, 
                                bg = "#ABB2B9", 
                                command = lambda : self.sendButton(self.entryMsg.get())) 
          
        self.buttonMsg.place(relx = 0.77, 
                             rely = 0.008, 
                             relheight = 0.06,  
                             relwidth = 0.22)
        
        self.disconnectBtn = Button(self.labelBottom,
                                    text= 'Disconnect',
                                    font = "Helvetica 10 bold",  
                                    width = 20, 
                                    bg = "#ABB2B9",
                                    command = lambda : self.disconnect())
        self.disconnectBtn.place(relx = 0.57, 
                             rely = 0.008, 
                             relheight = 0.06,  
                             relwidth = 0.22)
        
        self.textCons.config(cursor = "arrow") 
          
        # create a scroll bar 
        scrollbar = Scrollbar(self.textCons) 
          
        # place the scroll bar  
        # into the gui window 
        scrollbar.place(relheight = 1, 
                        relx = 0.974) 
          
        scrollbar.config(command = self.textCons.yview) 
          
        self.textCons.config(state = DISABLED) 

    def sendButton(self,messaggio):
        self.textCons.config(state= DISABLED)
        self.entryMsg.delete(0,END)
        self.msgToSend = messaggio
        sndthread = threading.Thread(target=self.sendMessage)
        sndthread.start()

    def sendMessage(self):
        connectionSocket.send(self.msgToSend.encode())

    def receiveMessage(self):
        print("Thread di ricezione partito")
        while True:
            try:
                message = connectionSocket.recv(1024).decode()
                if message == "NAME":
                    connectionSocket.send(self.name.encode())
                elif message == "END":
                    connectionSocket.close()
                    print("Chat left...")
                    self.window.destroy()
                    break
                else:
                    self.textCons.config(state= NORMAL)
                    self.textCons.insert(END,message+"\n\n")
            except:
                print("Connection Error")
                connectionSocket.close()
                break


       
        
    def disconnect(self):
        connectionSocket.send("$exit$".encode())

