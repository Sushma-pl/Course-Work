import socket
import time

serverIP = "10.0.1.2"


dst_ip = "10.0.1.2"
s = socket.socket()

print(dst_ip)

port = 12346

s.connect((dst_ip, port))


s.send('Hello server'.encode())
print ('Client received: '+s.recv(1024).decode())

print("Enter the request:")
req1 = raw_input()
req1 = req1 +'\r\n\r\n'

start_time = time.time()
s.send(req1.encode())
response = s.recv(1024).decode()
end_time = time.time()

print('Client received '+ response)

print('time taken to serve request:')
print("{:.5f}".format(end_time-start_time))
s.close()
