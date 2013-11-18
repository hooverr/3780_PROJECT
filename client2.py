import socket
import sys 
serverAddress = '10.66.110.137'
clientAddress = '10.66.110.137'
serverPort = 2500
clientPort = 2700
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((clientAddress,clientPort))

while 1:
  source = input('Enter identification: ')
  source = source.replace('/','') #strip slashes
  if(len(source) > 30):
    print("Invalid identification (max 30 characters)")
  else:
    break
#2 bytes for sequence number - limits number of messages stored on server to 100
#4 bytes for type
#30 bytes for source name
#30 bytes for destination name
#160 bytes for message - sms standard
#Total is 226, size should be power of 2 so 2^8 = 256 bytes
while(1):
  while 1: 
    frame = "1/READ/"+source+"/SERVER/"
    s.sendto(frame.encode('utf-8'), (serverAddress,serverPort))
    data, address = s.recvfrom(256)
    data = data.decode('utf-8')
    data = data.split('/')
    if(data[4] == ''): #no messages read
      break
    else:
      print(data[2] + " received "+ data[4])
  option = input('Enter option (1 - send, 2 - get, 0 - exit)')
  option = int(option)
  if(option == 1):
    while 1:
      destination = input('Enter name of receiver:')
      destination = destination.replace('/','') #strip slashes
      if(len(destination) > 30):
        print("Invalid destination")
      else:
        break
    while 1:
      message = input('Enter message to send : ')
      message = message.replace('/','')#strip slashes
      if(len(message) > 160):
        print("Message too long (max 160 characters)\n")
      else:
        break
    frame = "1/SEND/" + source + "/" + destination + "/" + message
    s.sendto(frame.encode('utf-8'), (serverAddress,serverPort))
  elif(option == 2):
    frame = "1/GET/"+source+"/SERVER/"
    while 1:
      s.sendto(frame.encode('utf-8'), (serverAddress,serverPort))
      data, address = s.recvfrom(256)
      data = data.decode('utf-8')
      data = data.split('/')
      if(data[4] == ''):
        break
      else:
        print("Message from " + data[2] + "-" + data[4])
        frame = data[0] + "/ACK/"+source+"/"+data[2]+ "/" + data[4]
  else:
    s.close()
    sys.exit(0)
       