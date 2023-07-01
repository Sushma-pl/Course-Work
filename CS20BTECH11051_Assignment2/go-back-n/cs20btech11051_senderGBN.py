import socket
import time
import sys
import _thread
import os 

senderIP = "10.0.0.1"
senderPort   = 12346
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 900 #Message Buffer Size


mutex = _thread.allocate_lock()
t = int(input("Enter timeout in ms:"))
timeout = t/1000   #100ms
timer_running = 1  #1->running , 0->false

socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

file = open('testFile.jpg' , 'rb')
file_size = os.path.getsize('testFile.jpg')
#print("File Size is :", file_size, "bytes")



base = 0
windowSize = int(input("enter window size: "))
nextSequence = 0
packets = []

flag = 0 #5 ->endof file 


def size_of_window(total_packets):
	return min(windowSize, total_packets-base)

def add_packets():
	global flag
	sequence = 0
	img_data = file.read(bufferSize)
	
	while img_data:
		data = sequence.to_bytes(2,byteorder='big')+ flag.to_bytes(1,byteorder='big') + img_data
		packets.append(data)
		sequence = sequence + 1
		img_data = file.read(bufferSize)
	flag = 5
	data = sequence.to_bytes(2,byteorder='big')+ flag.to_bytes(1,byteorder='big')
	packets.append(data)




def receive_ack(socket_udp):
	global mutex
	global base
	global timer_running
	
	while True:
		msgFromServer = socket_udp.recvfrom(bufferSize)
		ack = int.from_bytes(msgFromServer[0],byteorder='big')
		print(str(ack)+' ack recieved')
		if(ack >= base):
			mutex.acquire()
			base = ack+1 #cumulative ack
			#print('base= '+str(base))
			timer_running = not(timer_running)
			mutex.release()
				

add_packets()
total_packets = len(packets)
windowSize = size_of_window(total_packets)

_thread.start_new_thread(receive_ack, (socket_udp,))
st = time.time()
while base < total_packets:
		windowSize = size_of_window(total_packets)
		mutex.acquire()
		
		start_time = time.time()
		#send packets in windows 
		while nextSequence < base + windowSize:
			socket_udp.sendto(packets[nextSequence], recieverAddressPort)
			print('packet sent = '+str(nextSequence))
			nextSequence = nextSequence + 1

		#start timer
		start_time = time.time()
		timer_running = 1 
		#wait for ack or timeout 
		while (time.time()-start_time) < timeout and timer_running:
			
			mutex.release()
			time.sleep(0.001)
			mutex.acquire()
		

		if (time.time()-start_time) > timeout and timer_running:
			print('Timeout')
			timer_running = 0
			nextSequence = base
		else:
			windowSize = size_of_window(total_packets)
		mutex.release() 	

end_time = time.time()
time_interval = end_time-st
file_size = file_size/1000
print("File Size is :", file_size, "bytes")
throughput = file_size/time_interval

print("Throughput is :", throughput, "kb/s")

t = timeout*1000
print("\ntimeout in ms  = "+str(t))


file.close()
