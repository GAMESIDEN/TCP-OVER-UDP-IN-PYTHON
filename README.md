This is a Advanced Communication Networks project that creates a connection between server and client by using 3-way handshake, Leaky bucket algorithm for Congestion control 
and Stop and Wait ARQ protocol for Flow control.

Steps to run the Program:
------------------ 3-way Connection ------------------
1. Store all files into a single folder.
2. Open Command Prompt from that located folder.
3. Now, Firstly run the server.py file by using "python server.py" command.
4. Then, run client.py file by using "python client.py" command.
5. Here, It will create a 3-way handshake connection between both ends.

------------------ Leaky bucket Congestion Control -----------------

1. Now, To run Congestion control and send packets to other side,
   In the beginning, Enter the total amount of packets to be send.
2. Then, Enter each packets (ie. 1 2 3 4) and hit enter.
3. At the end, it will show which packets are sent, stored in remaining bucket 
   and which are dropped due to limit of bucket capacity.
4. On the other file, the sent packet size will be printed.

------------------ Stop and Wait ARQ Flow Control ------------------

1. Enter the frame to send from the client side script.
2. On the server side enter the acknowledgement (In this case enter 1).
3. If Any other number will be entered the client side will retrasmit the
   Frame because of the wrong acknowledgment.
4. If the acknowledgment is not being transmited within 10 seconds it
   will be retrasmited.
5. To exit the program just type "exit" and the connection will be terminated.
