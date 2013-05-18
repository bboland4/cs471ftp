#!/usr/bin/env python

import sys
import socket

# The length of the length string for sending files
LEN_LEN = 100

# The length of a command string
CMD_LEN = 100

#######               Command String Info            ###################
# [0-4 port number]:[6-8 command]:[10-99 cmd arg (filename)] 
# port number will be padded with 0's infront of it if len < 5
# ls command will be padded with a space after it 
# cmd arg will be padded with $'s after the text
########################################################################



########################################################################
# Sends all data 
# @param sock - the socket to send the data over
# @param data - the actual data to send
########################################################################
def sendData(sock, data):	
	# The total number of bytes sent in one shot
	numSent = 0	
	# The cumulative number of bytes sent
	totalNumSent = 0	
	# Send all the data
	while totalNumSent < len(data):		
		# Send as much as you can
		numSent = sock.send(data[totalNumSent:])		
		# Update how many bytes were sent thus far
		totalNumSent += numSent
	
	return totalNumSent
	
########################################################################
# Sends the size 
# @param sock - the socket to send it over
# @param size - the size to send
########################################################################
def sendSize(sock, size):	
	# Convert the size into string
	strSize = str(size) 	
	# Padd the size with leading 0's
	while len(strSize) < LEN_LEN:
		strSize = "0" + strSize	
	# Send the size
	sendData(sock, strSize)

########################################################################
# getFileInfo - gets information about a file
# @param filepath - the relative path to the file
# #return - Tuple - (file pointer, file size, file name)	
#         - None if invalid file path
########################################################################
def getFileInfo(filepath):
    try:
        fp = open(path, 'rb')
        size = os.path.getsize(path)
        p, filename = os.path.split(path)
        return (fp, size, filename)
    except:
        return None
    
    

########################################################################
# Receive data
# Receives the specified amount of data
# @param sock - the socket to receive the data from
# @param size - how much to receive
# @return - the received data
########################################################################
def recvData(sock, size):
	
	# The buffer to store the data
	data = ""
	
	# Keep receiving until all is received
	while size > len(data):
		
		# Receive as much as you can
		data += sock.recv(size - len(data))
	
	# Return the received data
	return data

########################################################################
# Recieves the size
# @param sock - the socket over which to receive the size
# @return - the received size
########################################################################
def recvSize(sock):

	# Get the string size
	strSize = recvData(sock, LEN_LEN)
		
	# Conver the size to an integer and return 
	return int(strSize)

########################################################################
# Recieves the command from the client
# @param sock - the socket over which to receive the size
# @return - dict - with fields 'port', 'cmd', 'filename'
########################################################################
def recvCmd(sock):
    try:
        strcmd = recvData(sock, CMD_LEN)
        lstcmd = strcmd.split(":")
        if cmd.length != 2:
            print "Error incorrect command format recieved"
            exit(0)
        cmd = {}
        cmd['port'] = int(lstcmd[0])
        cmd['cmd'] = lstcmd[1]
        cmd['filename'] = lstcmd[2]
        return cmd
    except:
        return None


########################################################################
#                               Main                                   # 
########################################################################
def main(port):  
    #number of parallel connections
    backlog = 10
    #bind the socket and listen for new connections
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind(('',port))
    listenSocket.listen(backlog)

    #listen forever
    while True:
        client, address = listenSocket.accept()
        #ERROR HERE: need to figure out how to wait for the command to come in
        # before we call this function...
        cmdinfo = recvCmd(listenSocket)
        #connect the datasocket to the client
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.connect(address, cmdinfo['port'])
        
        if cmdinfo['cmd'] == "ls ":
            print "ls command"
        elif cmdinfo['cmd'] == "put":
            print "put command"
        elif cmdinfo['cmd'] == "get":
            print "get command"
        else:
            print "Error, unknown command"
        
        dataSocket.close()
        
    return
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: ", sys.argv[0], " <Server Port>"
        exit(0)
    main(int(sys.argv[1]))
