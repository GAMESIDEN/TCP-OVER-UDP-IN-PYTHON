from enum import Enum

DEBUG = True

class STATE_MODE(Enum):
	CLOSE, LISTEN , SYN_RECEIVED, SYN_SENT , SYN_ACK_SENT, SYN_ACK_RECEIVED, FINAL_ACK = range(1, 8)

class Header:
	def __init__(self, sq_no, ackno, syn, ack):
		self.sq_no = sq_no
		self.ackno = ackno
		self.syn = syn
		self.ack = ack

# convert integer to bits for all values
	def binaryvalue(self):

		binaryvalue = '{0:032b}'.format(self.sq_no)
		binaryvalue += '{0:032b}'.format(self.ackno) + '{0:01b}'.format(self.syn) +'{0:01b}'.format(self.ack) + '{0:032b}'.format(0)
		sq_no = binaryvalue[:32]
		ackno = binaryvalue[32:64]
		sq_ack = binaryvalue[64:]
		output =  "seq_num = {0}".format(int(sq_no,2)) + ', ' +  "ackno = {0}".format(int(ackno,2)) + ', ' + "syn = {0}, ack = {1}".format(sq_ack[0], sq_ack[1])
		print(output)
		return binaryvalue.encode()
		 
# convert binary to integer and pass header to client and server
def bits_to_header_int(binaryvalue):

	binaryvalue = binaryvalue.decode()
	sq_no, ackno, syn, ack = int(binaryvalue[:32], 2), int(binaryvalue[32:64], 2), int(binaryvalue[64], 2), int(binaryvalue[65], 2)
	return Header(sq_no, ackno, syn, ack)

def main_data(data):
	data = data.decode()
	return data[96:]
