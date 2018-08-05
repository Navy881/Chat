import socket
import threading
import sys
from tkinter import *

sock = socket.socket()
sock.connect(('localhost', 9080))

def insertText():
    while True:
        data = sock.recv(1024).decode()

        text.insert(END, data)


def WriteMSG(event=NONE):
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    sock.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        sock.close()
        chat.quit()

#ТЕКСТОВОЕ ОКНО

chat = Tk()
chat.title("Chat Antoshka")#титульный лист(название чата)

POLE=Frame(chat,height=340, width=600)
panelFrame=Frame(chat,height=60, bg='gray')
name=StringVar()
name.set("Ваше имя")
my_msg= StringVar()
my_msg.set(" ")
text = Listbox(POLE,height=30,width=106, bg="white", fg='green')#создал окно с текстом, тут указаны его размеры и цвета
scroll = Scrollbar(POLE,command=text.yview)#Scrollbar. Объект-скроллер связывает с виджетом, которому он требуется, прокрутка экрана привязана к текстовому окну
scroll.pack(side=RIGHT, fill=Y)#прокрутка по оси Y, находится с права
text.config(yscrollcommand=scroll.set)

#1
POLE.pack(side='top',  expand=1)
text.pack(side='top',  expand=1)
panelFrame.pack(side='bottom', fill='x')

button_send_msg = Button(panelFrame, text="Отправка", command=WriteMSG)
button_send_msg.place(x = 560, y = 1, height = 60,width = 100)
entry_msg = Entry (panelFrame, textvariable=my_msg)
entry_msg.bind("<Return>", WriteMSG)
entry_msg.place(x = 0, y = 30, height = 30,width = 540)
entry_nick_name=Entry(panelFrame,textvariable=name)
entry_nick_name.place(x = 0, y = 0, height = 30,width = 120)


t3= threading.Thread(target=insertText)
t3.start()
chat.mainloop()
