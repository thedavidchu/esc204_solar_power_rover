# Solar power rover

import numpy as np
import matplotlib.pyplot as plt

class solar_power():
    def __init__(self):
        self.SUN = [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, \
              0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, \
              0,   0,   0,   9,  24,  53, 103, 128, 163, 170, 193, 252, \
            302, 286, 355, 426, 444, 523, 528, 534, 541, 486, 518, 538, \
            461, 464, 499, 431, 454, 539, 455, 518, 502, 453, 433, 351, \
            384, 317, 276, 263, 122, 116,  77,  70,  43,  38,   6,   0, \
              0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, \
              0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
        self.TIME = 15*60 # Time interval for the sun
        self.EFF = 0.15 # Efficiency of the solar panels
        self.ERG = 4130 # Energy used per charge
        self.INIT = 0.5 # Ratio of how full the battery starts...

        self.COLLECT = []
        for i in self.SUN:
            self.COLLECT += [i * self.EFF]

        self.ans = []

    def total_daily_sun(self):
        total_daily_sun = self.TIME * sum(self.SUN)
        print("The total energy the sun emits per day [J/m^2/day] =", total_daily_sun)

        erg_area = self.EFF * total_daily_sun
        print("The total energy collected per day[J/m^2/day] =", erg_area)

        return True

    def find_dimensions(self):
        factor = 0.001
        for area in range(0,1000,1): # Check areas (0,1000)
            capacity = 4*(4*4130) # Minimum capacity

            while self.check_dimensions(area*factor, capacity) == False:
                capacity += 10

                if capacity > 2*520380:
                    print("ERROR!")
                    break

            ans = [area*factor, capacity]
            print('Area and Capacity:', ans)
            
            self.ans += [ans]
            
        return True

    def check_dimensions(self, area, capacity):
        battery = self.INIT * capacity
        collect = [] # Function of how much sun it gets
        for i in self.COLLECT:
            collect += [area * i]

        for day in range(0,6,1):
            for t in range(0,len(collect),1):
                if t % 8 == 0 or (t%4==0 and t>23 and t<75):
                    battery -= self.ERG # Use battery

                    if battery < 0.2 * capacity: # Check if battery is out of charge
                        return False
                    
                battery += self.TIME*collect[t]
                if battery > capacity:
                    battery = capacity
        return True
        

    def results(self):
        print("Answer:", self.ans)

        x = []
        y = []
        for i in range(0,len(self.ans),1):
            x += [self.ans[i][0]]
            y += [self.ans[i][1]]

        plt.plot(x,y, label='Battery Size to Area')
        plt.xlabel('Area [m^2]')
        plt.ylabel('Size of Battery [J]')
        plt.title('Plot Showing Size of Battery to Area')
        plt.legend()
        plt.show()
        
        return True

    def simulate_dimensions(self, area, capacity, num_days=1):
        sim_battery = []
        sim_collect = []
        
        battery = self.INIT * capacity
        collect = [] # Function of how much sun it gets
        for i in self.COLLECT:
            collect += [area * i]

        for day in range(0, num_days, 1):
            

            for t in range(0,len(collect),1):

                sim_battery += [battery]
                sim_collect += [self.TIME * collect[t]]

                
                if t % 8 == 0 or (t%4==0 and t>23 and t<75):
                    battery -= self.ERG # Use battery

                    if battery < 0: # OR 0.2 * capacity: # Check if battery is out of charge
                        return False
                    
                battery += self.TIME*collect[t]
                if battery > capacity:
                    battery = capacity

        # Plotting it out
        time = []
        for i in range(0,num_days*len(collect),1):
            time += [i*0.25]

        plt.plot(time,sim_battery, label='Battery Charge')
        plt.plot(time, sim_collect, label='Sunlight collected')
        plt.xlabel('Time [h]')
        plt.ylabel('Energy [J]')
        plt.title('Simulation of 0.600 m^2 Solar Panel \n and \n 11.07 W-h battery')
        plt.legend()
        plt.show()

        return True
                

def main():
    x = solar_power()
    #x.total_daily_sun()
    
    #x.find_dimensions()
    #x.results()
    x.simulate_dimensions(0.04,76900,7)

main()
