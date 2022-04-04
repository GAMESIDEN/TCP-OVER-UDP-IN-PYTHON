import socket
import common
from common import STATE_MODE
import sys
from threading import *
import random
import multiprocessing

# global sock_prog
# global server_state_3_way
server_state_3_way = STATE_MODE.CLOSE


def update_server_state_3_way(new_state):
    global server_state_3_way
    print(server_state_3_way, '->', new_state)
    server_state_3_way = new_state

print('-------------- 3 Way handshake Connection --------------' + '\n')
def ThreeWayHandshake():
    sock_prog = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_prog.bind(("127.0.0.1", 1002))  # Bind the connection
    while True:
        if server_state_3_way == STATE_MODE.CLOSE:
            update_server_state_3_way(STATE_MODE.LISTEN)   # Server in Listen mode

        if server_state_3_way == STATE_MODE.LISTEN: # Server receive the ack from client and then send sck 1 and syn 1
            data, addr = sock_prog.recvfrom(1024)
            header = common.bits_to_header_int(data)
            body = common.main_data(data)

            if header.syn == 1:
                # it generate the rendom number
                seq_number = random.randint(0, (2 ** 5)-1)
                ack_number = header.sq_no + 1
                syn_header = common.Header(seq_number, ack_number, syn=1, ack=1)

                update_server_state_3_way(STATE_MODE.SYN_RECEIVED)
                sock_prog.sendto(syn_header.binaryvalue(), addr)
                print("Header sent Successfully!")
                update_server_state_3_way(STATE_MODE.SYN_ACK_SENT)

            if server_state_3_way == STATE_MODE.SYN_ACK_SENT: # Server receive the final ack from client and establish connection 
                data, addr = sock_prog.recvfrom(1024)
                header = common.bits_to_header_int(data)
                body = common.main_data(data)
                if header.syn == 0 and header.ack == 1:
                    update_server_state_3_way(STATE_MODE.FINAL_ACK)
                     
                    if server_state_3_way == STATE_MODE.FINAL_ACK:   
                        Thread(target=congetion).start()
                    sys.exit()
     


def stop_and_wait():
    
    print('\n'+'-------------- Flow Control Protocol STOP and WAIT --------------')

    ip_port = ("127.0.0.1", 1003)
    sock_prog1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_prog1.bind(("127.0.0.1", 1003))  # bind the connection
    
    while True:
        messageFromClient, address = sock_prog1.recvfrom(1024) # receive the data and decode it 
        dataFromClient = messageFromClient.decode("utf-8")
        print('\n'+"--> Frame receievd from client : ",dataFromClient)

        if dataFromClient == 'exit':
            sys.exit()

        if len(dataFromClient) > 0:
            ack = input("Enter acknowledgement number (Use no=1 to confirm ack) : ")
            encodeddatatoclient = ack.encode("utf-8")
            sock_prog1.sendto(encodeddatatoclient,address)

def congetion():
    print('\n' + '-------------- Congetion Control Leaky Algorithm --------------')

    ip_port = ("127.0.0.1", 1004)
    sock_prog2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_prog2.bind(("127.0.0.1", 1004))  # bind the connection

    while True:
        sentDataFromClient, address = sock_prog2.recvfrom(1024) # receive the data and decode it 
        dataFromClient1 = sentDataFromClient.decode("utf-8")
        array = dataFromClient1.split()
        for y in array:
            print('\n'+"--> Packet Size Received in server : ",int(y))

     # after 3 way call stop and wait protocol 
        Thread(target=stop_and_wait).start()


if __name__ == '__main__':
    Thread(target=ThreeWayHandshake).start()