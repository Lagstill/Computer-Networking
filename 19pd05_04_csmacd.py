"""
PSG COLLEGE OF TECHNOLOGY
       AMCS
    CN PACKAGE
    
    
19PD04 - AKSHAYA L
19PD05 - ALAGU PRAKALYA P
    
"""

import numpy
import random
import math
import collections
import time


Max_time = 50
#total_num = 0
#global trasmission_delay

#The functions creates connection between the stations + avg_arr_rate
def create_station(N, A, D): 
    stations = []
    for i in range(0, N):
        stations.append(Station(i*D, A))
    return stations

#In order to make the packet transmission if the channel is idle
#while continously sensing the medium, the packet is moved along
#exponential rate in the channel
def move_pkt_exp_rv(arr_time):
    rand_val = 1 - random.uniform(0, 1)
    res = (-math.log(1 - rand_val) / float(arr_time))
    return res


#Funtion to implement 1-P,p-P, N-P
def MAC_CSMA_CD(N, A, R, L, D, S, persistent_type):
    
    time_current = 0
    transmitted_packets = 0                #pkts transmitted
    actual_pkt_recieved = 0                #pkts which are successfully transmitted
    stations = create_station(N, A, D)     #Creates the LAN

    while True:

        # Some random temporary station is chosen initailly and is checked alongside
        
        shortest_timed_station = Station(None, A)  
        shortest_timed_station.track_station = [float("infinity")]
        for station in stations:
            if len(station.track_station) > 0:
                #checking min time taking station with other stations
                shortest_timed_station = shortest_timed_station if shortest_timed_station.track_station[0] < station.track_station[0] else station
        
        # If no more pkts are left, we break
        if shortest_timed_station.distance is None:  
            break

        time_current = shortest_timed_station.track_station[0]
        #Transimission begins
        transmitted_packets += 1

       # Checking further collisions
        had_collided= False
        for station in stations:
            if station.distance != shortest_timed_station.distance and len(station.track_station) > 0:
                stat_dist = abs(shortest_timed_station.distance - station.distance)
                
                propagation_delay = stat_dist / float(S)  #D/S
                trasmission_delay = L/float(R)            #L/R

                if station.track_station[0] <= (time_current + propagation_delay): 
                    collision_possible= True 
                else:
                    collision_possible=False

                # Sense the channel if it is idle or busy
                if (time_current + propagation_delay) < station.track_station[0] < (time_current + propagation_delay + trasmission_delay):
                    #based on collision occerence the pkts are sent with prob 1
                    if persistent_type == 0:
                        for i in range(len(station.track_station)):
                            if (time_current + propagation_delay) < station.track_station[i] < (time_current + propagation_delay + trasmission_delay):
                                station.track_station[i] = (time_current + propagation_delay + trasmission_delay)
                            else:
                                break
                    #P-persistent implementation
                    
                    if persistent_type == 2:  
                        #assuming station transmits or waits again with probabilities p=0.4
                        p=0.4  
                        # Get random value between 0 (exclusive) and 1 (inclusive)
                        rand_ = random.uniform(0, 1)
                        print("\n------------------------------\n")
                        print("Acquired random number :",rand_)
                        print("\n------------------------------\n")
                        if(rand_<=p):
                            for i in range(len(station.track_station)):
                                if (time_current + propagation_delay) < station.track_station[i] < (time_current + propagation_delay + trasmission_delay):
                                    station.track_station[i] = (time_current + propagation_delay + trasmission_delay)
                                else:
                                    break
                        else:
                            print("Waiting Randomly")
                            time.sleep(2.2)
                            if (time_current + propagation_delay) < station.track_station[0] < (time_current + propagation_delay + trasmission_delay):
                                MAC_CSMA_CD(N, A, R, L, D, S, 0)
                    
                    #Non-persistent implementation        
                    if persistent_type == 1:
                        station.NP_chn_busy(R)

                if collision_possible:
                    had_collided= True
                    transmitted_packets += 1
                    station.check_collision(R)

        #Trying for collision recovery
        # Update all stations latest packet arrival times 
        
        # If no collision happened
        if had_collided is not True:  
            actual_pkt_recieved += 1
            shortest_timed_station.rmv_pkt()
        # If a collision occurred
        else:   
            print("\n%%% Collision Occurred %%%\n")
            shortest_timed_station.check_collision(R)

    print("\n*******************************************\n")
    print("Success ratio (pkt trans_): ", (actual_pkt_recieved/float(transmitted_packets))*100)
    c=transmitted_packets-actual_pkt_recieved
    print("Acquired effeciency : ", (L/R)/((c*2*(D/S))+(D/S)+(L/R)))

    print("Acquired throughput", (L * actual_pkt_recieved) / float(time_current + (L/R)) * pow(10, -6), "Mbps")
    print("")
    print("\n*******************************************\n")
    

#defining the node connected the LAN network
class Station:
    def __init__(self, distance, A):
        
        self.track_station = collections.deque(self.station_track_station(A))
        self.distance = distance  
        self.collisions = 0
        self.random_collision_wait = 0
        self.Collision_limit = 5
        
    def successful_transmission(self):
        self.collisions = 0
        self.random_collision_wait = 0

    def station_track_station(self, A):
        packets = []
        arrival_time_sum = 0
        
        #giving the maximum simulation time checker
        while arrival_time_sum <= Max_time:
            arrival_time_sum += move_pkt_exp_rv(A)
            packets.append(arrival_time_sum)
        return sorted(packets)

    def exp_backoff(self, R, general_collisions):
        rand_num = random.random() * (pow(2, general_collisions) - 1)
        return rand_num * 512/float(R) 

    def check_collision(self, R):
        self.collisions += 1
        if self.collisions > self.Collision_limit:
            
            # Since max collision occured, return pkts (drop_)
            return self.rmv_pkt()

        # Add the exponential backoff time to waiting time
        backoff = self.track_station[0] + self.exp_backoff(R, self.collisions)
        for i in range(len(self.track_station)):
            if backoff >= self.track_station[i]:
                self.track_station[i] = backoff
            else:
                break

    def rmv_pkt(self):
        self.track_station.popleft()
        self.collisions = 0
        self.random_collision_wait = 0

    def NP_chn_busy(self, R):
        self.random_collision_wait += 1
        if self.random_collision_wait > self.Collision_limit:
           return self.rmv_pkt()
        
        # Add the exponential backoff time to waiting time
        backoff = self.track_station[0] + self.exp_backoff(R, self.random_collision_wait)
        print("NP-BACKK OFF:",backoff)
        for i in range(len(self.track_station)):
            if backoff >= self.track_station[i]:
                self.track_station[i] = backoff
            else:
                break

# N = Number of stations connected to the LAN
# A = Packet arrival rate 
# R = Channel speed
# L = Packet size
# D = Distance between stations
# S = Propagation speed 



#main function

S = (2/float(3)) * 3 * pow(10, 8)

print("IMPLEMENTATION OF CSMA/CD WITH THE FOLLOWING METHODS :   ")
print("\n1. 1-PERSISTENT \n2. p-PERSISTENT \n3. NON-PERSISTENT   ")
print("Enter the value of the following parameters :   \n")
D = int(input("Enter the distance between adjacent stations on the channel (m): "))
L = int(input("Enter the size of the packet (bits): "))

print("\nPacket arrival rate :   ",[12, 5, 7],"\n")
print("Number of stations connected to the LAN :   ",(1, 21, 10))
R = float(input("Channel speed :  " ))
#print("Channel speed :   ",2 * pow(10, 6),"\n")
R = R * pow(10, 6)

dec = int(input("Enter the mode of carrier sense (0- [1p], 1-[np], 2-[pp]): "))

# (CSMA/CD Persistent)
if(dec==0):
    for N in range(1, 21, 10):
        for A in [12, 5, 7]:
            print("Persistent: ", " Station No. : ", N, "  Packet rcvd : ", A)
            MAC_CSMA_CD(N, A, R, L, D, S, 0)

#(CSMA/CD Non-persistent)
if(dec==1):
    for N in range(1,21,10):
        for A in [12,5,7]:
            print("Non persistent", " Station No.: ", N, "  Packet rcvd : ", A)
            MAC_CSMA_CD(N, A, R, L, D, S, 1)
     
# (CSMA/CD p-persistent)
if(dec==2):
    for N in range(1, 21, 10):
        for A in [12, 5, 7]:
            print("p(0.4)-Persistent: ", "  Stations: ", N, "  Packet rcvd : ", A)
            MAC_CSMA_CD(N, A, R, L, D, S, 2)