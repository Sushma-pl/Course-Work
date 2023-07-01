import socket 

dict = {'key1':'val1','key2':'val2','key3':'val3','key4':'val4','key5':'val5','key6':'val6'}

def handle_request(recvmsg):
	response = 'HTTP/1.1 404 Not Found'
	messages = recvmsg.split(' ')
	if(messages[0] == 'GET'):
		key_pair = messages[1].split('?')
        	keys = key_pair[1].split('=')
		if(dict.has_key(keys[1])):
			response = 'HTTP/1.1 200 OK' + '\n' + dict[keys[1]]
	if(messages[0] == 'PUT'):
		key_pair = messages[1].split('/')
		if(dict.has_key(key_pair[2])):
			response = 'HTTP/1.1 200 OK'
			dict[key_pair[2]] = key_pair[3]
		else:
			dict[key_pair[2]] = key_pair[3]
			response = 'HTTP/1.1 201 Created'
	return response

server_ip = "10.0.1.3"

ser_s = socket.socket()
print("server: socket created successfully")

sport = 12347

ser_s.bind((server_ip , sport))
print("server:socket successfully binded to %s" %(sport))

ser_s.listen(5)
print("server: socket is listening")

while True:
	connection , addr = ser_s.accept()
	print('Got connection from ', addr )
	recvmsg = connection.recv(1024).decode()
	print('Server received: '+recvmsg)
	connection.send('Hello cache'.encode())
	recvmsg = connection.recv(1024).decode()
	print('server received: '+recvmsg)
	response = handle_request(recvmsg)
	response = response + ' \r\n\r\n\r\n\r\n'
	connection.sendall(response.encode())
	connection.close() 


	
