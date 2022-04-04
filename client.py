from http import client
from multiprocessing import Value
from common import STATE_MODE
import multiprocessing
import random
import socket
import common
import sys


print('-------------- 3 Way handshake Connection --------------' + '\n')
class Client1:
    global sock_prog
    sock_prog = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddressPort = ("127.0.0.1", 1002)
    
    
    # this is the reserved method in python so this method is called when class object is created 
    def __init__(self):
        self.client_state_3_way = STATE_MODE.CLOSE
        self.handshake_3()

    # this the handshkae method 
    def handshake_3(self):
        if self.client_state_3_way == STATE_MODE.CLOSE: # This is the first handshake send from client to server
            sq_no = random.randint(0, (2 ** 5)-1)
            syn_header = common.Header(sq_no, 0, syn=1, ack=0)
            sock_prog.sendto(syn_header.binaryvalue(), ("127.0.0.1", 1002))
            self.update_state_3_way(STATE_MODE.SYN_SENT)

        if self.client_state_3_way == STATE_MODE.SYN_SENT:
           
            data, addr = sock_prog.recvfrom(1024)  # receive ack and syc from server and client send final ack
            header = common.bits_to_header_int(data)
            body = common.main_data(data)
            if header.syn == 1 and header.ack == 1:
                self.update_state_3_way(STATE_MODE.SYN_ACK_RECEIVED)
                ackno = header.sq_no + 1
                sq_no = header.ackno
                header = common.Header(sq_no, ackno, syn=0, ack=1)
                sock_prog.sendto(header.binaryvalue(), ("127.0.0.1", 1002)) 
                self.update_state_3_way(STATE_MODE.FINAL_ACK)

                # after 3 way call congetion control
                Client3.congestion()

    def update_state_3_way(self, new_state):
        print(self.client_state_3_way, '->', new_state)
        self.client_state_3_way = new_state

class Client2:

    def stop_and_wait():
        ip_port = ("127.0.0.1", 1003)
        sock_prog1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        global ackfromserver
        global address
        print('\n'+'-------------- Flow Control Protocol STOP and WAIT --------------')
        while True:

            data = input('\n'+"--> Enter the frame / Type 'exit' to terminate the transmission : ")   # Enter frame to send
            encodeddata = data.encode("utf-8")
            
            sock_prog1.sendto(encodeddata, ip_port) # Now send the data after encoding to client

            if data == 'exit':
                sys.exit()
        
            while True:
                try:
                    sock_prog1.settimeout(10.0)
                    ackfromserver, address = sock_prog1.recvfrom(5000) # Receive & Decode data
                    decode_ack_from_server = ackfromserver.decode("utf-8")
                    print("Received acknowledgement number :",decode_ack_from_server)

                    while decode_ack_from_server != '1':
                        print("\n"+"Frame " + "'" + data + "'" + "is retrasmitted to server !")
                        encodeddata = data.encode("utf-8")
                        sock_prog1.sendto(encodeddata, address)

                        ackfromserver1, address = sock_prog1.recvfrom(5000) # Receive & Decode data
                        decode_ack_from_server1 = ackfromserver1.decode("utf-8")
                        decode_ack_from_server = decode_ack_from_server1
        
                except socket.timeout: # When timeout, data willbe retransmitted
                    while True:
                        print("After time out, frame" + "'" + data + "'" + "is retrasmitted again !")
                        ackfromserver2, address1 = sock_prog1.recvfrom(5000) # Receive & Decode data
                        decode_ack_from_server = ackfromserver2.decode("utf-8")
                        
                        while decode_ack_from_server != '1':
                            print("Frame " + "'" + data + "'" + "is retrasmitted to server !")
                            encodeddata = data.encode("utf-8")
                            sock_prog1.sendto(encodeddata, address1)

                            ackfromserver3, address = sock_prog1.recvfrom(5000) # Receive & Decode data
                            decode_ack_from_server1 = ackfromserver3.decode("utf-8")
                            decode_ack_from_server = decode_ack_from_server1
                        break
                     
                break

class Client3:
    def congestion():
        print("\n"+"-----------------Congetion Control Leaky Algorithm------------------")
        
        ip_port = ("127.0.0.1", 1004)
        sock_prog2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        rem_bucket = 0
        bucket_cap = 4
        sent_cap = 3
        global send_data_to_server
        converted_data = ""
        print("\nBucket Capacity is: 5")
        print("\nSent Capacity from bucket is: 4")
        i = int(input('\n'+"Enter the total packets : "))
        
        # Read input
        res = list(map(int, input("\nEnter the packet size : ").strip().split()))[:i]

        for x in res:
            if x != 0:
                if rem_bucket + x > bucket_cap: # if for accept calculations
                    accpt = -1
                else:
                    accpt = x
                    rem_bucket = rem_bucket + x
            else:
                accpt = 0
            
            if rem_bucket != 0: # if for sent calaculation 
                if rem_bucket < sent_cap:
                    sent = rem_bucket
                    rem_bucket = 0
                else:
                    sent = sent_cap
                    rem_bucket = rem_bucket - sent_cap
            else:
                sent = 0

            if accpt == -1: # print dropped or calaculated data 
                print( "Packet Size :",x, ", Accept Capacity: dropped", ", Sent Capacity :", sent , ", Remaining in Bucket: " ,rem_bucket)
                send_data_to_server = str(sent)
                converted_data += (' '+send_data_to_server)
            else:
                print( "Packet Size :",x, ", Accept Capacity: ", accpt,", Sent Capacity :", sent , ", Remaining in Bucket: " ,rem_bucket)
                send_data_to_server = str(sent)
                converted_data += (' '+send_data_to_server)
    
        encodeddata1 = converted_data.encode("utf-8")
        sock_prog2.sendto(encodeddata1, ip_port) # Now send the data after encoding to server


        # after 3 way call stop and wait protocol 
        Client2.stop_and_wait()

client1 = Client1() # Class call
client2 = Client2()
client3 = Client3()
