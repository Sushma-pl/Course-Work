import socket

dict = {}

def handle_request(recvmsg):
	messages = recvmsg.split(' ')
	if(messages[0] == 'GET'):
		key_pair = messages[1].split('?')
		value = key_pair[1].split('=')
		if(dict.has_key(value[1])):
			response = 'HTTP/1.1'  +  ' 200 OK \n' + dict[value[1]]
		else:
			response = 'HTTP/1.1 404 NOT FOUND'		
	elif(messages[0] == 'PUT'):
		key_pair = messages[1].split('/')
		if(dict.has_key(key_pair[2])):
			response = 'HTTP/1.1 200 Ok'
			dict[key_pair[2]] = key_pair[3]
		else:
			response = 'HTTP/1.1 201 Created'
			dict[key_pair[2]] = key_pair[3]			
	elif(messages[0] == 'DELETE'):
		key_pair = messages[1].split('/')
		dict.pop(key_pair[2])
		response = 'HTTP/1.1 200 OK \n record deleted successfully'
	
	return response



dst_ip = "10.0.1.2"

s = socket.socket()
print ("Socket successfully created")

dport = 12346

s.bind((dst_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")

while True:
  c, addr = s.accept()
  print ('Got connection from', addr )
  recvmsg = c.recv(1024).decode()
  print('Server received: '+recvmsg)
  c.send('Hello client'.encode())
  recvmsg = c.recv(1024).decode()
  print('Server received: '+recvmsg)
  response = handle_request(recvmsg)
  response = response + '\r\n\r\n\r\n\r\n' 
  c.sendall(response.encode())
  


  c.close()

