#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
##import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")

##            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(msg):  # event is passed by binders.
    """Handles sending of messages."""
    msg += "xxx"
    msg = msg.encode("utf8")
    client_socket.send(msg)
    print(msg)

#----Now comes the sockets part----
HOST = '192.168.0.101'
PORT = 12346

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

send("en")


##import socket, time, threading, os
##
##
##def timeout():
##    global inTime
##    time.sleep(5)
##    inTime = False
##
##
##try:
##    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##    host = '192.168.0.101'
##    port = 12346
##    sock.connect((host, port))
##    sock.send(b'A')
##    print('Connection is stable')
##except:
##    print('Connection is unstable.')
##    print('Please check the server.')
##    os._exit(0)
##
##while True:
##    time.sleep(1)
##    sock.send('hallo')
##    rMessage = sock.recv(2).decode()
##    print(rMessage)
##
##    print('Connection is unstable')
##
##
##
##
##sock.close()
##