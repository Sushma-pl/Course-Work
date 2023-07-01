import socket
import time
import  sys 
import select
import os 

senderIP = "10.0.0.1"
senderPort   = 12346
recieverAddressPort = ("10.0.0.2", 12347)
bufferSize  = 900 							

socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

n = int(input("Enter the timeout in ms : "))
timeout = n/1000 #0.01   #10ms
socket_udp.settimeout(timeout)


file = open('testFile.jpg' , 'rb')
file_size = os.path.getsize('testFile.jpg')


sequence=0
flag=0 # 1 indicate end of file
retransmit = 0
next_packet = 0
packets = []

def add_packets():
	global flag
	seq = 0
	img_data = file.read(bufferSize)
	
	while img_data:
		data = seq.to_bytes(2,byteorder='big')+ flag.to_bytes(1,byteorder='big') + img_data
		packets.append(data)
		seq = not(seq) 
		img_data = file.read(bufferSize)
	flag = 5	#last packet to indicate end of file
	data = seq.to_bytes(2,byteorder='big')+ flag.to_bytes(1,byteorder='big')
	packets.append(data)


add_packets()
total_packets = len(packets)
start_time = time.time()
while next_packet < total_packets:
	message = packets[next_packet] 
	sequence = int.from_bytes(message[0:2],byteorder='big')
	print("packet "+str(sequence)+" is sent "+str(next_packet))
	socket_udp.sendto(message, recieverAddressPort)
	
	#waiting for ack
	try:
		while True:
			msgFromServer = socket_udp.recvfrom(bufferSize)
			ack = int.from_bytes(msgFromServer[0],byteorder='big')
			print(str(ack)+' ack recieved')
			if ack == sequence:
				break
		next_packet = next_packet+1
	except socket.timeout:
		print("timeout")
		retransmit = retransmit+1



end_time = time.time()
time_interval = end_time-start_time
file_size = file_size/1000
print("File Size is :", file_size, "bytes")
throughput = file_size/time_interval
print("Throughput is :", throughput, "kb/s")

t = timeout*1000
print("\ntimeout in ms  = "+str(t))
print("\npacket retransmit = "+str(retransmit))
file.close()
