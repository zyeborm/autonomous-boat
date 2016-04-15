import socket
import logging

class Network_Manager(object):
    def __init__(self):
      logging.info('Init Network port 0.0.0.0 5005')
      self.Address = "0.0.0.0"
      self.Port = 5005
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet , UDP
      self.sock.bind((self.Address, self.Port))
      self.sock.setblocking(0) #so we can poll it
    
    def Poll_Network(self):
        Got_Data = True
        Processed_Packets = 0 #if there are too many packets the executive will stop
        while (Got_Data): #need to loop to process all the packets we have recieved
        
            try: #if we look and there is no data we get an error
                data, addr = self.sock.recvfrom(1400) # buffer size is 1400 bytes
                print "received message:", data
            except:
                Got_Data = False

            if (Processed_Packets > 10):
                Got_Data = False
                logging.warning("Rxed too many packets")  #FIXME should empty the socket at this point

            Processed_Packets += 1  

if __name__ == "__main__":
    import time
    net = Network_Manager()
    while True:    
        #print "wind : %3.2f   sail %3.2f" % (rotary.Read_Wind_Angle_Sensor(), rotary.Read_Sail_1_Angle_Sensor())
        net.Poll_Network()
        time.sleep(.1)    
