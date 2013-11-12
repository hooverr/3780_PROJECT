import socket
import sys 
serverAddress = '192.168.0.17'
clientAddress = '192.168.0.20'
port = 2500

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((clientAddress,port))
source = input('Enter identification: ')
seqNo = 1 #incremented each message sent, together with client name this is unique
while(1):
  while 1: 
    frame = "1/READ/"+source+"/SERVER/"
    s.sendto(frame.encode('utf-8'), (serverAddress,port))
    data, address = s.recvfrom(256)
    data = data.decode('utf-8')
    data = data.split('/')
    if(data[4] == ''):
      break
    else:
      print(data[2] + " received "+ data[4])
  option = input('Enter option (1 - send, 2 - get, 0 - exit)')
  option = int(option)
  if(option == 1):
    type = "SEND"
    destination = input('Enter name of receiver:')
    while 1:
      message = input('Enter message to send : ')
      message = message.replace('/','')
      if(len(message) > 160):
        print("Message too long (max 160 characters)\n")
      else:
        break
    frame = str(seqNo) + "/" + type + "/" + source + "/" + destination + "/" + message
    s.sendto(frame.encode('utf-8'), (serverAddress,port))
    seqNo += 1
  elif(option == 2):
    frame = "1/GET/"+source+"/SERVER/"
    while 1:
      s.sendto(frame.encode('utf-8'), (serverAddress,port))
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
       