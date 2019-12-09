from socket import *
sock = socket(2, 1)
password = input('Enter password to Terminate Server : ')
sock.connect(('localhost', 45566))
sock.send(bytes(password, 'utf-8'))
sock.close();
