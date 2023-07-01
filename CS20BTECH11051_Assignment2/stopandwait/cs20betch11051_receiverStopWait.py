import socket

recieverIP = "10.0.0.2"
recieverPort   = 12347
bufferSize  = 1024 #Message Buffer Size


socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )


file = open('receivedImage.jpg','wb')
recievedMessage , senderAddress =  socket_udp.recvfrom(bufferSize)
ack=0

while recievedMessage:  
    seq_rec = recievedMessage[0:2]
    flag = recievedMessage[2]
    
    if flag == 5:
    	message = seq_rec  
    	socket_udp.sendto(message,senderAddress)
    	break;
    sequence = int.from_bytes(seq_rec,byteorder='big')
    print(str(sequence)+' recieved')
    while sequence != ack:
    	print(str(sequence)+' sent')
    	socket_udp.sendto(sequence.to_bytes(2,byteorder='big'),senderAddress)
    	recievedMessage , senderAddress =  socket_udp.recvfrom(bufferSize)
    	seq_rec = recievedMessage[0:2]
    	sequence = int.from_bytes(seq_rec,byteorder='big')


    msg = recievedMessage[3:903]
    file.write(msg)	
    
    reply = ack.to_bytes(2,byteorder='big')
    print(str(ack)+' sent')
    socket_udp.sendto(reply,senderAddress)
    ack = not(ack)
    recievedMessage , senderAddress = socket_udp.recvfrom(bufferSize)

file.close()
print("image received!!")
file.close()
