import socket

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size


socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )

file = open('recievedImage.jpg','wb')
expectedSequence=0


flag =0

while True:
    recievedMessage,senderAddress = socket_udp.recvfrom(bufferSize)
    seq = int.from_bytes(recievedMessage[0:2],byteorder='big')
    flag = recievedMessage[2]
    if flag == 5:
    	print('ack', seq)
    	message = seq.to_bytes(2,byteorder='big')
    	socket_udp.sendto(message, senderAddress)
    	break
    print(str(seq)+' packet recieved')
    
    if seq == expectedSequence:
    	print('ack', expectedSequence)
    	message = expectedSequence.to_bytes(2,byteorder='big')
    	socket_udp.sendto(message, senderAddress)
    	expectedSequence = expectedSequence + 1
    	msg = recievedMessage[3:903]
    	file.write(msg)	
    else:
    	print('ack', expectedSequence - 1)
    	x = expectedSequence - 1
    	message = x.to_bytes(2,byteorder='big')
    	socket_udp.sendto(message, senderAddress)
            
file.close()
