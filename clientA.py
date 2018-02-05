import socket, time, threading, os
from alarmcodes import *


def timeout():
    global inTime
    time.sleep(5)
    inTime = False


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '145.89.86.57'
    port = 12345
    sock.connect((host, port))
    sock.send(b'A')
    print('Connection is stable')
except:
    print('Connection is unstable.')
    print('Please check the server.')
    os._exit(0)

while True:

    time.sleep(1)
    sock.send('01'.encode())
    rMessage = sock.recv(2).decode()
    print(rMessage)

    print('Connection is unstable')




sock.close()
