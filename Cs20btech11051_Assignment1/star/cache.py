import socket

cache_dict = {}

cache_dst_ip = "10.0.1.2"
server_ip = "10.0.1.3"

s = socket.socket()
print("cache successfully created socket ")

cport = 12346
sport = 12347

def handle_request(recvmsg):
	recv_response = 'key-pair doen not present in cache'
	messages = recvmsg.split(' ')
	if(messages[0] == 'GET'):
		key_pair = messages[1].split('?')
        	key = key_pair[1].split('=')
		if(cache_dict.has_key(key[1])):
			recv_response ='HTTP/1.1 200 OK'+'\n'+cache_dict[key[1]]
		else:
			print(recv_response)
			print('Accesing from server')
			s2 = socket.socket()
	        	s2.connect((server_ip,sport))
        		s2.send('Hello Server'.encode())
			print('Cache received: '+s2.recv(1024).decode())
			recvmsg = recvmsg + '\r\n\r\n'
			s2.send(recvmsg.encode())
        		received_response = s2.recv(1024).decode()
			recv_response =  received_response
			x = received_response.split(' ')
			if(x[1] == '200'):
				y = x[2].split('\n')
        			cache_dict[key[1]] = y[1]
	if(messages[0] == 'PUT'):
		key_pair = messages[1].split('/')
		cache_dict[key_pair[2]] = key_pair[3]
		s2 = socket.socket()
                s2.connect((server_ip,sport))
		s2.send('Hello Server'.encode())
                print('Cache received: '+s2.recv(1024).decode())
		recvmsg = recvmsg + '\r\n\r\n'
                s2.send(recvmsg.encode())
                received_response = s2.recv(1024).decode()
                recv_response =  received_response
               
	return recv_response 



s.bind((cache_dst_ip,cport))
print("socket binded to %s" %(cport))

s.listen(5)

print("socket is listening")


while True:
	con , addr = s.accept()
	print('Got connection from ',addr )
	recvmsg = con.recv(1024).decode()
	print('Cache received: '+recvmsg)
	con.send('Hello client'.encode())
	recvmsg = con.recv(1024).decode()
	print('Cache Received :'+recvmsg)
	response = handle_request(recvmsg)
	response = response + '\r\n\r\n\r\n'
	con.sendall(response.encode())
	con.close()

