#Robert Hoover 3780 Project
#SERVER
#2013-11-10

import socket
host = '192.168.0.17' 
port = 2500
messageList = []
ackList = []

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))

print ("Server waiting on port:", port)
while 1:
  data, address = s.recvfrom(1024)
  address = address[0]  #IP address of message sender
  data = data.decode('utf-8')
  dataList = data.split("/") #Split frame into its parts
  sequenceNumber = dataList[0]
  type = dataList[1]
  source = dataList[2]
  destination = dataList[3]
  payload = dataList[4]
  if(type == 'SEND'):
    messageList.append((sequenceNumber,source,destination,payload))
  if(type == 'GET'):
    response = ""
    for message in reversed(messageList): #Check for messages
      if (message[2] == source):
        response += "Message from: " + message[1] +" - " + message[3] + "\n"
        ackList.append(("1","SERVER",message[1], message[2] + " received message " + message[3]))
        messageList.remove(message)
    for acknowledgment in reversed(ackList): #Check for acknowledgements
      if (acknowledgment[2] == source):
        response += "Message from: " + acknowledgment[1] +" - " + acknowledgment[3] + "\n"
        ackList.remove(acknowledgment)
    if(response != ""): #send response
      seqNo = "1"
      type = "RESPONSE"
      destination = source
      source = "SERVER"   
      frame = seqNo + "/" + type + "/" + source + "/" + destination + "/" + response
      s.sendto(frame.encode('utf-8'), (address,port))
    else: #if no messages still reply to keep client from waiting
      seqNo = "1"
      type = "RESPONSE"
      destination = source
      source = "SERVER"   
      response = "You have no messages"
      frame = seqNo + "/" + type + "/" + source + "/" + destination + "/" + response
      s.sendto(frame.encode('utf-8'), (address,port))
    
      