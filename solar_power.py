# Solar power rover

import math
import numpy as np
import matplotlib.pyplot as plt

class solar_power():
    def __init__(self):

        ## Define constants as specified in assignment
        
        self.SUN = [   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, \
              0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, \
              0,   0,   0,   9,  24,  53, 103, 128, 163, 170, 193, 252, \
            302, 286, 355, 426, 444, 523, 528, 534, 541, 486, 518, 538, \
            461, 464, 499, 431, 454, 539, 455, 518, 502, 453, 433, 351, \
            384, 317, 276, 263, 122, 116,  77,  70,  43,  38,   6,   0, \
              0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, \
              0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0] # Solar energy flux as a function of time [W/m^2]

        self.TIME = 15*60 # Time interval for the sun
        self.EFF = 0.15 # Efficiency of the solar panels
        self.INIT = 0.5 # Ratio of how full the battery starts...

        self.MIN = 0.2 # Minimum acceptable charge
        self.DAYS = 7 # Number of days in simulation
        self.PERDAY = 18 # Charge cycles per day

        self.COLLECT = [] # Energy flux collected as a function of time [J/m^2]
        for i in self.SUN:
            self.COLLECT += [i * self.EFF * self.TIME]


        ## Constants that I have previously calculated
        
        self.ERG = 5150 # Energy used per charge


        ## Class-wide variables for later use
        
        # Store function of area to battery size
        self.ans = []




    ##### Energy Generated ######

    def convert(self, value,unitA='J/day/m^2', unitB='J/day/m^2'):
        """
        Convert units of ENERGY FLUX.
        """
        # This would be better to use split at '/'
        
        if unitA == 'J/day/m^2':
            if unitB == 'J/day/m^2':
                return value
            elif unitB == 'kJ/day/m^2':
                return value / 1000
            elif unitB == 'W/m^2':
                return value / 86400
            elif unitB == 'kW/m^2':
                return value / 86400 / 1000
            elif unitB == 'Wh/day/m^2':
                return value / 3600
            elif unitB == 'kWh/day/m^2':
                return value / 3600 / 1000
            else:
                print('ERROR: unsupoorted target unit in solar_power.convert(). Value returned as None.')
                return None
        else:
            print('ERROR: unsupported input unit in solar_power.convert(). Value returned as None.')
            return None

    def daily_sun(self,show=False):
        """
        Calculate and display the TOTAL SOLAR ENERGY FLUX and the COLLECTED SOLAR ENERGY FLUX.

        Returns COLLECTED SOLAR FLUX in [J/day/m^2]
        """

        # Calculate SOLAR FLUX
        flux  = self.TIME * sum(self.SUN)

        # Calculate COLLECTED SOLAR FLUX
        col  = self.EFF * flux
        
        if show == True:
            # TOTAL SOLAR ENERGY FLUX
            fluxK = self.convert(flux,unitB='kJ/day/m^2')
            fluxA = self.convert(flux,unitB='W/m^2')
            fluxB = self.convert(flux,unitB='kW/m^2')
            fluxC = self.convert(flux,unitB='Wh/day/m^2')
            fluxD = self.convert(flux,unitB='kWh/day/m^2')
            
            print('The total solar energy flux:')
            print('\t\t =', flux,  '\t\t [J/day/m^2]')
            print('\t\t =', fluxK,  '\t\t [kJ/day/m^2]')
            print('\t\t =', fluxA, '\t\t [W/m^2]')
            print('\t\t =', fluxB, '\t\t [kW/m^2]')
            print('\t\t =', fluxC, '\t\t [Wh/day/m^2]')
            print('\t\t =', fluxD, '\t\t [kWh/day/m^2]\n\n')

            # COLLECTED SOLAR ENERGY FLUX
            
            colK = self.EFF * fluxK
            colA = self.EFF * fluxA
            colB = self.EFF * fluxB
            colC = self.EFF * fluxC
            colD = self.EFF * fluxD
            print('The total collected solar energy flux:')
            print('\t\t =', col,  '\t\t [J/day/m^2]')
            print('\t\t =', colK,  '\t\t [kJ/day/m^2]')
            print('\t\t =', colA, '\t\t [W/m^2]')
            print('\t\t =', colB, '\t\t [kW/m^2]')
            print('\t\t =', colC, '\t\t [Wh/day/m^2]')
            print('\t\t =', colD, '\t\t [kWh/day/m^2]\n\n')
        
        return col




    ##### Energy Requirements #####

    def daily_use(self):
        """
        Returns daily energy use in [J/day]
        """
        return self.PERDAY * self.ERG

    def min_area(self, show=False):
        """
        Calculate the minimum area of solar panelling needed to power the robot, neglecting storage capacity limitaions.
        """
        
        # Calculate mininum area
        min_area = self.daily_use() / self.daily_sun(show=False)
        
        if show == True:
            print('One m^2 of solar panelling at', self.EFF, 'efficiency can generate enough energy to power', 1/min_area, 'robots!\n\n')
            
            print('The minimum area of the solar panel (neglecting storage capacity limitations) is:')
            print('\t\t =',min_area, '/t/t [m^2]')
            print('\t\t =',min_area*100*100, '/t/t [cm^2]\n\n')

        return min_area




    ##### Find dimensions #####

    def find_min_cap(self,show=False):
        N = 1000 # Number of steps
        k = 0.1 # Upper interval

        self.ans = [] # Reset self.ans

        max_theory_capacity = 1 / (self.INIT - self.MIN) * self.DAYS * self.PERDAY * self.ERG # = 10/3 * 7 * 18 * self.ERG = 2 163 000 for self.ERG==5150
        print('Max is', max_theory_capacity)
        for i in range(0,N,1): # Check areas (0,N)
            area = i*k/N

            if i == 0:
                if area == 0 and self.ERG == 5150: 
                    capacity = max_theory_capacity
                else:
                    capacity = math.floor(1/self.INIT*(4*self.ERG)/10)*10  # Minimum capacity (0.5 -> 0 in one day): floor(2*(4*ERG), -1)
                    
                while self.check_cap(area, capacity) == False:
                    capacity += 10

                    if capacity > max_theory_capacity: 
                        print('ERROR: Exceeded bounds... somebody\'s math is wrong!')
                        break
            else:
                capacity = ans[1] # Take previous capacity

                while self.check_cap(area, capacity) == True:
                    capacity -= 10

                    if capacity < 1/self.INIT * 4 * self.ERG: # 1/0.5 * 4 (initial runs in darkness) * self.ERG
                        print('ERROR: Something actually went wrong!')
                        break

                capacity += 10 # Add 10 back to capacity, to make it work again   

            ans = [area, capacity]
            if show == True:
                print('Area and Capacity:', ans)
            
            self.ans += [ans]
    
        return True

    def check_cap(self, area, capacity, min_charge=0.2):

        battery = self.INIT * capacity

        collect = [] # Function of how much sun it gets (in J)
        for i in self.COLLECT:
            collect += [area * i]

        for day in range(0,self.DAYS,1):
            for t in range(0,len(collect),1):
                if t % 8 == 0 or (t%4==0 and t>23 and t<75):
                    battery -= self.ERG # Use battery

                    if battery < min_charge * capacity: # Check if battery is out of charge
                        return False
                    
                battery += collect[t]
                if battery > capacity:
                    battery = capacity

        # If it passes the filter, return True
        return True
        
    def plot_min_cap_by_area_curve(self,show=False,erg_unit='Wh'):
        

        area = []
        capacity = []
        max_cap = []
        min_cap = []
        flux_unit = erg_unit+'/day/m^2'
        
        for i in range(0,len(self.ans),1):
            area += [self.ans[i][0]]
            capacity += [self.convert(self.ans[i][1], unitB=flux_unit)]

            max_cap += [1854000] #3.3*(4*self.ERG)
            min_cap += [420 * self.ERG]

        if show == True:
            print('Minimum capacity [J] as a function of Area:', self.ans)
            print('Flux unit:', flux_unit)
            print('Minimum capacity ['+flux_unit+'] as a function of Area:', capacity)

        plt.plot(area,capacity, label='Minimum Battery size for Given Area')
        plt.xlabel('Area [m^2]')
        plt.ylabel('Size of Battery ['+erg_unit+']')
        plt.title('Optimal Battery-size-to-Area Curve')
        plt.legend()
        plt.show()
        
        return True



    def simulate_dimensions(self, area, capacity, num_days=1, show=False, plot_upper=False, plot_lower=False):
        sim_battery = []
        sim_collect = []

        # Initiate battery levels
        battery = self.INIT * capacity
        
        collect = [] # Function of how much sun it gets
        for i in self.COLLECT:
            collect += [area * i]
        print('Collected solar energy [J/15 min]:', collect)

        # Show values it will plot
        if show == True:
            print('Area:', area, '\n')
            print('COLLECT:', self.COLLECT, '\nSum of COLLECT:', sum(self.COLLECT), '\n')
            print('collect:',collect, '\nSum of collect:', sum(collect),'\n')

        for day in range(0, num_days, 1):
            
            for t in range(0,len(collect),1):

                sim_battery += [battery]
                sim_collect += [collect[t]] # WAS: [self.TIME * area * collect[t]]. Incorrect?

                
                if t % 8 == 0 or (t%4==0 and t>23 and t<75):
                    battery -= self.ERG # Use battery

                    if show == True:
                        if battery < 0.2 * capacity and battery > 0: # Check if battery is out of charge
                            print('WARNING: BATTERY LOW')
                        elif battery <= 0:
                            print('ERROR: BATTERY DEAD')
                    
                battery += collect[t]
                if battery > capacity:
                    battery = capacity

        # Plotting it out
        time = []
        title = str(num_days) + ' Day Simulation of '+str(area)+ ' m^2 Solar Panel \n and \n '+str(round(capacity/3600,2))+' W-h battery'
        for i in range(0,num_days*len(collect),1):
            time += [i*0.25]

        plt.plot(time,sim_battery, 'b', label='Battery Charge')
        plt.plot(time, sim_collect, 'xkcd:orange', label='Sunlight collected')

        if plot_upper == True:
            upper = []
            for i in range(len(time)):
                upper += [capacity]

            plt.plot(time, upper, 'g--', label='Capacity of Battery')

        if plot_lower == True:
            lower = []
            for i in range(len(time)):
                lower += [0.2 * capacity]

            plt.plot(time, lower, 'r--', label='Minimum Battery Charge')
        
        plt.xlabel('Time [h]')
        plt.ylabel('Energy [J]')
        plt.title(title)
        plt.legend(loc='upper left')
        plt.show()

        return True

    def sim_stored_2020_04_08(self):
        """
        Store value from simulation on April 5th.
        """
        L =[[0.0, 1854000], [0.0001, 1850270], [0.0002, 1846530], [0.00030000000000000003, 1842790], [0.0004, 1839050], [0.0005, 1835310], [0.0006000000000000001, 1831570], [0.0007000000000000001, 1827830], [0.0008, 1824090], [0.0009, 1820350], [0.001, 1816620], [0.0011, 1812880], [0.0012000000000000001, 1809140], [0.0013, 1805400], [0.0014000000000000002, 1801660], [0.0015, 1797920], [0.0016, 1794180], [0.0017000000000000001, 1790440], [0.0018, 1786700], [0.0019000000000000002, 1782960], [0.002, 1779230], [0.0021000000000000003, 1775490], [0.0022, 1771750], [0.0023000000000000004, 1768010], [0.0024000000000000002, 1764270], [0.0025, 1760530], [0.0026, 1756790], [0.0027, 1753050], [0.0028000000000000004, 1749310], [0.0029000000000000002, 1745580], [0.003, 1741840], [0.0031, 1738100], [0.0032, 1734360], [0.0033000000000000004, 1730620], [0.0034000000000000002, 1726880], [0.0035, 1723140], [0.0036, 1719400], [0.0037, 1715660], [0.0038000000000000004, 1711920], [0.0039000000000000003, 1708190], [0.004, 1704450], [0.0041, 1700710], [0.004200000000000001, 1696970], [0.0043, 1693230], [0.0044, 1689490], [0.0045, 1685750], [0.004600000000000001, 1682010], [0.0047, 1678270], [0.0048000000000000004, 1674530], [0.004900000000000001, 1670800], [0.005, 1667060], [0.0051, 1663320], [0.0052, 1659580], [0.005300000000000001, 1655840], [0.0054, 1652100], [0.0055, 1648360], [0.005600000000000001, 1644620], [0.0057, 1640880], [0.0058000000000000005, 1637150], [0.005900000000000001, 1633410], [0.006, 1629670], [0.0061, 1625930], [0.0062, 1622190], [0.006300000000000001, 1618450], [0.0064, 1614710], [0.0065, 1610970], [0.006600000000000001, 1607230], [0.0067, 1603490], [0.0068000000000000005, 1599760], [0.006900000000000001, 1596020], [0.007, 1592280], [0.0071, 1588540], [0.0072, 1584800], [0.007300000000000001, 1581060], [0.0074, 1577320], [0.0075, 1573580], [0.007600000000000001, 1569840], [0.0077, 1566110], [0.0078000000000000005, 1562370], [0.0079, 1558630], [0.008, 1554890], [0.0081, 1551150], [0.0082, 1547410], [0.0083, 1543670], [0.008400000000000001, 1539930], [0.0085, 1536190], [0.0086, 1532450], [0.008700000000000001, 1528720], [0.0088, 1524980], [0.0089, 1521240], [0.009, 1517500], [0.0091, 1513760], [0.009200000000000002, 1510020], [0.009300000000000001, 1506280], [0.0094, 1502540], [0.0095, 1498800], [0.009600000000000001, 1495060], [0.0097, 1491330], [0.009800000000000001, 1487590], [0.0099, 1483850], [0.01, 1480110], [0.010100000000000001, 1476370], [0.0102, 1472630], [0.0103, 1468890], [0.0104, 1465150], [0.0105, 1461410], [0.010600000000000002, 1457680], [0.010700000000000001, 1453940], [0.0108, 1450200], [0.0109, 1446460], [0.011, 1442720], [0.011100000000000002, 1438980], [0.011200000000000002, 1435240], [0.011300000000000001, 1431500], [0.0114, 1427760], [0.0115, 1424020], [0.011600000000000001, 1420290], [0.0117, 1416550], [0.011800000000000001, 1412810], [0.0119, 1409070], [0.012, 1405330], [0.012100000000000001, 1401590], [0.0122, 1397850], [0.0123, 1394110], [0.0124, 1390370], [0.0125, 1386630], [0.012600000000000002, 1382900], [0.012700000000000001, 1379160], [0.0128, 1375420], [0.0129, 1371680], [0.013, 1367940], [0.013100000000000002, 1364200], [0.013200000000000002, 1360460], [0.013300000000000001, 1356720], [0.0134, 1352980], [0.0135, 1349250], [0.013600000000000001, 1345510], [0.0137, 1341770], [0.013800000000000002, 1338030], [0.013900000000000001, 1334290], [0.014, 1330550], [0.014100000000000001, 1326810], [0.0142, 1323070], [0.0143, 1319330], [0.0144, 1315590], [0.0145, 1311860], [0.014600000000000002, 1308120], [0.014700000000000001, 1304380], [0.0148, 1300640], [0.0149, 1296900], [0.015, 1293160], [0.0151, 1289420], [0.015200000000000002, 1285680], [0.015300000000000001, 1281940], [0.0154, 1278210], [0.0155, 1274470], [0.015600000000000001, 1270730], [0.015700000000000002, 1266990], [0.0158, 1263250], [0.0159, 1259510], [0.016, 1255770], [0.0161, 1252030], [0.0162, 1248290], [0.016300000000000002, 1244550], [0.0164, 1240820], [0.0165, 1237080], [0.0166, 1233340], [0.0167, 1229600], [0.016800000000000002, 1225860], [0.016900000000000002, 1222120], [0.017, 1218380], [0.0171, 1214640], [0.0172, 1210900], [0.0173, 1207160], [0.017400000000000002, 1203430], [0.0175, 1199690], [0.0176, 1195950], [0.0177, 1192210], [0.0178, 1188470], [0.017900000000000003, 1184730], [0.018, 1180990], [0.0181, 1177250], [0.0182, 1173510], [0.0183, 1169780], [0.018400000000000003, 1166040], [0.0185, 1162300], [0.018600000000000002, 1158560], [0.018699999999999998, 1154820], [0.0188, 1151080], [0.018900000000000004, 1147340], [0.019, 1143600], [0.019100000000000002, 1139860], [0.019200000000000002, 1136120], [0.0193, 1132390], [0.0194, 1128650], [0.0195, 1124910], [0.019600000000000003, 1121170], [0.019700000000000002, 1117430], [0.0198, 1113690], [0.0199, 1109950], [0.02, 1106210], [0.0201, 1102470], [0.020200000000000003, 1098740], [0.020300000000000002, 1095000], [0.0204, 1091260], [0.0205, 1087520], [0.0206, 1083780], [0.020700000000000003, 1080040], [0.0208, 1076300], [0.020900000000000002, 1072560], [0.021, 1068820], [0.0211, 1065080], [0.021200000000000004, 1061350], [0.0213, 1057610], [0.021400000000000002, 1053870], [0.0215, 1050130], [0.0216, 1046390], [0.021700000000000004, 1042650], [0.0218, 1038910], [0.021900000000000003, 1035170], [0.022, 1031430], [0.0221, 1027690], [0.022200000000000004, 1023960], [0.0223, 1020220], [0.022400000000000003, 1016480], [0.0225, 1012740], [0.022600000000000002, 1009000], [0.0227, 1005260], [0.0228, 1001520], [0.022900000000000004, 997780], [0.023, 994040], [0.023100000000000002, 990310], [0.023200000000000002, 986570], [0.0233, 982830], [0.0234, 979090], [0.0235, 975350], [0.023600000000000003, 971610], [0.023700000000000002, 967870], [0.0238, 964130], [0.0239, 960390], [0.024, 956650], [0.0241, 952920], [0.024200000000000003, 949180], [0.024300000000000002, 945440], [0.0244, 941700], [0.0245, 937960], [0.0246, 934220], [0.024700000000000003, 930480], [0.0248, 926740], [0.024900000000000002, 923000], [0.025, 919260], [0.0251, 915530], [0.025200000000000004, 911790], [0.0253, 908050], [0.025400000000000002, 904310], [0.0255, 900570], [0.0256, 896830], [0.025700000000000004, 893090], [0.0258, 889350], [0.025900000000000003, 885610], [0.026, 881880], [0.0261, 878140], [0.026200000000000005, 874400], [0.0263, 870660], [0.026400000000000003, 866920], [0.0265, 863180], [0.026600000000000002, 859440], [0.0267, 855700], [0.0268, 851960], [0.026900000000000004, 848220], [0.027, 844490], [0.027100000000000003, 840750], [0.027200000000000002, 837010], [0.0273, 833270], [0.0274, 829530], [0.0275, 825790], [0.027600000000000003, 822050], [0.027700000000000002, 818310], [0.027800000000000002, 814570], [0.0279, 810840], [0.028, 807100], [0.0281, 803360], [0.028200000000000003, 799620], [0.028300000000000002, 795880], [0.0284, 792140], [0.0285, 788400], [0.0286, 784660], [0.028700000000000003, 780920], [0.0288, 777180], [0.028900000000000002, 773450], [0.029, 769710], [0.0291, 765970], [0.029200000000000004, 762230], [0.0293, 758490], [0.029400000000000003, 754750], [0.0295, 751010], [0.0296, 747270], [0.029700000000000004, 743530], [0.0298, 739790], [0.029900000000000003, 736060], [0.03, 732320], [0.030100000000000002, 728580], [0.0302, 724840], [0.0303, 721100], [0.030400000000000003, 717360], [0.0305, 713620], [0.030600000000000002, 709880], [0.0307, 706140], [0.0308, 702410], [0.030900000000000004, 698670], [0.031, 694930], [0.031100000000000003, 691190], [0.031200000000000002, 687450], [0.0313, 683710], [0.031400000000000004, 679970], [0.0315, 676230], [0.0316, 672490], [0.031700000000000006, 668750], [0.0318, 665020], [0.031900000000000005, 661280], [0.032, 657540], [0.032100000000000004, 653800], [0.0322, 650060], [0.0323, 646320], [0.0324, 642580], [0.0325, 638840], [0.032600000000000004, 635100], [0.0327, 631370], [0.0328, 627630], [0.0329, 623890], [0.033, 620700], [0.033100000000000004, 617530], [0.0332, 614370], [0.0333, 611200], [0.0334, 608040], [0.0335, 604870], [0.033600000000000005, 601710], [0.0337, 598540], [0.033800000000000004, 595380], [0.0339, 592210], [0.034, 589050], [0.0341, 585880], [0.0342, 582720], [0.034300000000000004, 579550], [0.0344, 576390], [0.0345, 573220], [0.0346, 570060], [0.0347, 566890], [0.034800000000000005, 563730], [0.0349, 560560], [0.035, 557400], [0.0351, 554230], [0.0352, 551070], [0.035300000000000005, 547900], [0.0354, 544740], [0.0355, 541570], [0.0356, 538400], [0.0357, 535240], [0.035800000000000005, 532070], [0.0359, 528910], [0.036, 525740], [0.0361, 522580], [0.0362, 519410], [0.036300000000000006, 516250], [0.0364, 513080], [0.0365, 509920], [0.0366, 506750], [0.0367, 503590], [0.036800000000000006, 500420], [0.036899999999999995, 497260], [0.037, 494090], [0.0371, 490930], [0.037200000000000004, 487760], [0.03730000000000001, 484600], [0.037399999999999996, 481430], [0.0375, 478270], [0.0376, 475100], [0.037700000000000004, 471940], [0.03780000000000001, 468770], [0.037899999999999996, 465610], [0.038, 462440], [0.0381, 459280], [0.038200000000000005, 456110], [0.03830000000000001, 452950], [0.038400000000000004, 449780], [0.0385, 446620], [0.0386, 443450], [0.038700000000000005, 440290], [0.0388, 437120], [0.038900000000000004, 433960], [0.039, 430790], [0.0391, 427630], [0.039200000000000006, 424460], [0.0393, 421300], [0.039400000000000004, 418130], [0.0395, 414970], [0.0396, 411800], [0.039700000000000006, 408640], [0.0398, 405470], [0.039900000000000005, 402310], [0.04, 399140], [0.040100000000000004, 395980], [0.0402, 392810], [0.0403, 389650], [0.040400000000000005, 386480], [0.0405, 383320], [0.040600000000000004, 380150], [0.0407, 376990], [0.0408, 373820], [0.040900000000000006, 370660], [0.041, 367490], [0.041100000000000005, 364330], [0.0412, 361160], [0.0413, 358000], [0.041400000000000006, 354830], [0.0415, 351670], [0.0416, 348500], [0.0417, 345340], [0.041800000000000004, 342170], [0.04190000000000001, 339010], [0.042, 335840], [0.0421, 332680], [0.0422, 329510], [0.042300000000000004, 326340], [0.04240000000000001, 323180], [0.0425, 320010], [0.0426, 316850], [0.0427, 313680], [0.042800000000000005, 310520], [0.04290000000000001, 307350], [0.043, 304190], [0.0431, 301020], [0.0432, 297860], [0.043300000000000005, 294690], [0.04340000000000001, 291530], [0.0435, 288360], [0.0436, 285200], [0.0437, 282030], [0.043800000000000006, 278870], [0.04390000000000001, 275700], [0.044, 272540], [0.0441, 269370], [0.0442, 266210], [0.044300000000000006, 263040], [0.04440000000000001, 259880], [0.0445, 256710], [0.0446, 253550], [0.044700000000000004, 250380], [0.044800000000000006, 247220], [0.0449, 244050], [0.045, 240890], [0.0451, 237720], [0.045200000000000004, 234560], [0.04530000000000001, 231390], [0.0454, 228230], [0.0455, 225060], [0.0456, 221900], [0.045700000000000005, 218730], [0.04580000000000001, 215570], [0.0459, 212400], [0.046, 209240], [0.0461, 206070], [0.046200000000000005, 202910], [0.0463, 199740], [0.046400000000000004, 196580], [0.0465, 193410], [0.0466, 190250], [0.046700000000000005, 187080], [0.0468, 183920], [0.046900000000000004, 180750], [0.047, 177590], [0.0471, 174420], [0.047200000000000006, 171260], [0.0473, 168090], [0.047400000000000005, 164930], [0.0475, 161760], [0.0476, 158600], [0.047700000000000006, 155430], [0.0478, 152270], [0.047900000000000005, 149100], [0.048, 145940], [0.048100000000000004, 142770], [0.0482, 139610], [0.0483, 136440], [0.048400000000000006, 133280], [0.0485, 130110], [0.048600000000000004, 126950], [0.0487, 123780], [0.0488, 120620], [0.048900000000000006, 117450], [0.049, 114280], [0.049100000000000005, 111140], [0.0492, 108010], [0.049300000000000004, 104880], [0.049400000000000006, 101750], [0.0495, 98620], [0.0496, 95930], [0.0497, 95920], [0.049800000000000004, 95900], [0.04990000000000001, 95890], [0.05, 95870], [0.0501, 95860], [0.0502, 95840], [0.050300000000000004, 95830], [0.05040000000000001, 95820], [0.0505, 95800], [0.0506, 95790], [0.0507, 95770], [0.050800000000000005, 95760], [0.05090000000000001, 95740], [0.051, 95730], [0.0511, 95720], [0.0512, 95700], [0.051300000000000005, 95690], [0.05140000000000001, 95670], [0.0515, 95660], [0.0516, 95640], [0.0517, 95630], [0.051800000000000006, 95620], [0.05190000000000001, 95600], [0.052, 95590], [0.0521, 95570], [0.0522, 95560], [0.052300000000000006, 95540], [0.05240000000000001, 95530], [0.0525, 95520], [0.0526, 95500], [0.052700000000000004, 95490], [0.05280000000000001, 95470], [0.0529, 95460], [0.053, 95440], [0.0531, 95430], [0.053200000000000004, 95420], [0.05330000000000001, 95400], [0.0534, 95390], [0.0535, 95370], [0.0536, 95360], [0.053700000000000005, 95340], [0.05380000000000001, 95330], [0.0539, 95320], [0.054, 95300], [0.0541, 95290], [0.054200000000000005, 95270], [0.0543, 95260], [0.054400000000000004, 95240], [0.0545, 95230], [0.0546, 95220], [0.054700000000000006, 95200], [0.0548, 95190], [0.054900000000000004, 95170], [0.055, 95160], [0.0551, 95140], [0.055200000000000006, 95130], [0.0553, 95120], [0.055400000000000005, 95100], [0.0555, 95090], [0.055600000000000004, 95070], [0.0557, 95060], [0.0558, 95050], [0.055900000000000005, 95030], [0.056, 95020], [0.056100000000000004, 95000], [0.0562, 94990], [0.0563, 94970], [0.056400000000000006, 94960], [0.0565, 94950], [0.056600000000000004, 94930], [0.0567, 94920], [0.0568, 94900], [0.056900000000000006, 94890], [0.057, 94870], [0.0571, 94860], [0.0572, 94850], [0.057300000000000004, 94830], [0.05740000000000001, 94820], [0.0575, 94800], [0.0576, 94790], [0.0577, 94770], [0.057800000000000004, 94760], [0.05790000000000001, 94750], [0.058, 94730], [0.0581, 94720], [0.0582, 94700], [0.058300000000000005, 94690], [0.05840000000000001, 94670], [0.0585, 94660], [0.0586, 94650], [0.0587, 94630], [0.058800000000000005, 94620], [0.05890000000000001, 94600], [0.059, 94590], [0.0591, 94570], [0.0592, 94560], [0.059300000000000005, 94550], [0.05940000000000001, 94530], [0.0595, 94520], [0.0596, 94500], [0.0597, 94490], [0.059800000000000006, 94470], [0.05990000000000001, 94460], [0.06, 94450], [0.0601, 94430], [0.060200000000000004, 94420], [0.060300000000000006, 94400], [0.0604, 94390], [0.0605, 94370], [0.0606, 94360], [0.060700000000000004, 94350], [0.06080000000000001, 94330], [0.0609, 94320], [0.061, 94300], [0.0611, 94290], [0.061200000000000004, 94270], [0.06130000000000001, 94260], [0.0614, 94250], [0.0615, 94230], [0.0616, 94220], [0.061700000000000005, 94200], [0.06180000000000001, 94190], [0.061900000000000004, 94170], [0.062, 94160], [0.0621, 94150], [0.062200000000000005, 94130], [0.0623, 94120], [0.062400000000000004, 94100], [0.0625, 94090], [0.0626, 94080], [0.0627, 94060], [0.06280000000000001, 94050], [0.06290000000000001, 94030], [0.063, 94020], [0.0631, 94000], [0.0632, 93990], [0.06330000000000001, 93980], [0.06340000000000001, 93960], [0.0635, 93950], [0.0636, 93930], [0.0637, 93920], [0.06380000000000001, 93900], [0.06390000000000001, 93890], [0.064, 93880], [0.0641, 93860], [0.06420000000000001, 93850], [0.0643, 93830], [0.0644, 93820], [0.0645, 93800], [0.0646, 93790], [0.06470000000000001, 93780], [0.0648, 93760], [0.0649, 93750], [0.065, 93730], [0.0651, 93720], [0.06520000000000001, 93700], [0.0653, 93690], [0.0654, 93680], [0.0655, 93660], [0.0656, 93650], [0.06570000000000001, 93630], [0.0658, 93620], [0.0659, 93600], [0.066, 93590], [0.0661, 93580], [0.06620000000000001, 93560], [0.0663, 93550], [0.0664, 93530], [0.0665, 93520], [0.0666, 93500], [0.06670000000000001, 93490], [0.0668, 93480], [0.0669, 93460], [0.067, 93450], [0.0671, 93430], [0.06720000000000001, 93420], [0.0673, 93400], [0.0674, 93390], [0.0675, 93380], [0.06760000000000001, 93360], [0.0677, 93350], [0.0678, 93330], [0.0679, 93320], [0.068, 93300], [0.06810000000000001, 93290], [0.0682, 93280], [0.0683, 93260], [0.0684, 93250], [0.0685, 93230], [0.06860000000000001, 93220], [0.0687, 93200], [0.0688, 93190], [0.0689, 93180], [0.069, 93160], [0.06910000000000001, 93150], [0.0692, 93130], [0.0693, 93120], [0.0694, 93110], [0.0695, 93090], [0.06960000000000001, 93080], [0.0697, 93060], [0.0698, 93050], [0.0699, 93030], [0.07, 93020], [0.07010000000000001, 93010], [0.0702, 92990], [0.0703, 92980], [0.0704, 92960], [0.0705, 92950], [0.07060000000000001, 92930], [0.0707, 92920], [0.0708, 92910], [0.0709, 92890], [0.071, 92880], [0.07110000000000001, 92860], [0.0712, 92850], [0.0713, 92830], [0.0714, 92820], [0.0715, 92810], [0.07160000000000001, 92790], [0.0717, 92780], [0.0718, 92760], [0.0719, 92750], [0.072, 92730], [0.07210000000000001, 92720], [0.0722, 92710], [0.0723, 92690], [0.0724, 92680], [0.0725, 92660], [0.07260000000000001, 92650], [0.0727, 92630], [0.0728, 92620], [0.0729, 92610], [0.073, 92590], [0.07310000000000001, 92580], [0.0732, 92560], [0.0733, 92550], [0.0734, 92530], [0.0735, 92520], [0.07360000000000001, 92510], [0.0737, 92490], [0.07379999999999999, 92480], [0.07390000000000001, 92460], [0.074, 92450], [0.07410000000000001, 92430], [0.0742, 92420], [0.07429999999999999, 92410], [0.07440000000000001, 92390], [0.0745, 92380], [0.07460000000000001, 92360], [0.0747, 92350], [0.07479999999999999, 92330], [0.07490000000000001, 92320], [0.075, 92310], [0.07510000000000001, 92290], [0.0752, 92280], [0.07529999999999999, 92260], [0.07540000000000001, 92250], [0.0755, 92230], [0.07560000000000001, 92220], [0.0757, 92210], [0.07579999999999999, 92190], [0.07590000000000001, 92180], [0.076, 92160], [0.07610000000000001, 92150], [0.0762, 92140], [0.07629999999999999, 92120], [0.07640000000000001, 92110], [0.0765, 92090], [0.07660000000000002, 92080], [0.0767, 92060], [0.07680000000000001, 92050], [0.07690000000000001, 92040], [0.077, 92020], [0.0771, 92010], [0.0772, 91990], [0.07730000000000001, 91980], [0.07740000000000001, 91960], [0.0775, 91950], [0.0776, 91940], [0.0777, 91920], [0.07780000000000001, 91910], [0.07790000000000001, 91890], [0.078, 91880], [0.0781, 91860], [0.0782, 91850], [0.07830000000000001, 91840], [0.07840000000000001, 91820], [0.0785, 91810], [0.0786, 91790], [0.0787, 91780], [0.07880000000000001, 91760], [0.07890000000000001, 91750], [0.079, 91740], [0.0791, 91720], [0.0792, 91710], [0.07930000000000001, 91690], [0.07940000000000001, 91680], [0.0795, 91660], [0.0796, 91650], [0.07970000000000001, 91640], [0.07980000000000001, 91620], [0.0799, 91610], [0.08, 91590], [0.0801, 91580], [0.08020000000000001, 91560], [0.08030000000000001, 91550], [0.0804, 91540], [0.0805, 91520], [0.0806, 91510], [0.08070000000000001, 91490], [0.08080000000000001, 91480], [0.0809, 91460], [0.081, 91450], [0.0811, 91440], [0.08120000000000001, 91420], [0.08130000000000001, 91410], [0.0814, 91390], [0.0815, 91380], [0.0816, 91360], [0.08170000000000001, 91350], [0.08180000000000001, 91340], [0.0819, 91320], [0.082, 91310], [0.0821, 91290], [0.08220000000000001, 91280], [0.08230000000000001, 91260], [0.0824, 91250], [0.0825, 91240], [0.0826, 91220], [0.08270000000000001, 91210], [0.08280000000000001, 91190], [0.0829, 91180], [0.083, 91170], [0.08310000000000001, 91150], [0.0832, 91140], [0.08330000000000001, 91120], [0.0834, 91110], [0.0835, 91090], [0.08360000000000001, 91080], [0.0837, 91070], [0.08380000000000001, 91050], [0.0839, 91040], [0.084, 91020], [0.08410000000000001, 91010], [0.0842, 90990], [0.08430000000000001, 90980], [0.0844, 90970], [0.0845, 90950], [0.08460000000000001, 90940], [0.0847, 90920], [0.08480000000000001, 90910], [0.0849, 90890], [0.085, 90880], [0.08510000000000001, 90870], [0.0852, 90850], [0.08530000000000001, 90840], [0.0854, 90820], [0.0855, 90810], [0.08560000000000001, 90790], [0.0857, 90780], [0.08580000000000002, 90770], [0.0859, 90750], [0.086, 90740], [0.08610000000000001, 90720], [0.0862, 90710], [0.08630000000000002, 90690], [0.0864, 90680], [0.0865, 90670], [0.08660000000000001, 90650], [0.0867, 90640], [0.08680000000000002, 90620], [0.0869, 90610], [0.087, 90590], [0.08710000000000001, 90580], [0.0872, 90570], [0.08730000000000002, 90550], [0.0874, 90540], [0.0875, 90520], [0.08760000000000001, 90510], [0.0877, 90490], [0.08780000000000002, 90480], [0.0879, 90470], [0.088, 90450], [0.08810000000000001, 90440], [0.0882, 90420], [0.08830000000000002, 90410], [0.0884, 90390], [0.0885, 90380], [0.08860000000000001, 90370], [0.0887, 90350], [0.08880000000000002, 90340], [0.0889, 90320], [0.089, 90310], [0.08910000000000001, 90290], [0.0892, 90280], [0.08930000000000002, 90270], [0.08940000000000001, 90250], [0.0895, 90240], [0.08960000000000001, 90220], [0.0897, 90210], [0.0898, 90200], [0.08990000000000001, 90180], [0.09, 90170], [0.09010000000000001, 90150], [0.0902, 90140], [0.0903, 90120], [0.09040000000000001, 90110], [0.0905, 90100], [0.09060000000000001, 90080], [0.0907, 90070], [0.0908, 90050], [0.09090000000000001, 90040], [0.091, 90020], [0.09110000000000001, 90010], [0.0912, 90000], [0.0913, 89980], [0.09140000000000001, 89970], [0.0915, 89950], [0.09160000000000001, 89940], [0.0917, 89920], [0.0918, 89910], [0.09190000000000001, 89900], [0.092, 89880], [0.09210000000000002, 89870], [0.0922, 89850], [0.09230000000000001, 89840], [0.09240000000000001, 89820], [0.0925, 89810], [0.0926, 89800], [0.0927, 89780], [0.09280000000000001, 89770], [0.09290000000000001, 89750], [0.093, 89740], [0.0931, 89720], [0.0932, 89710], [0.09330000000000001, 89700], [0.09340000000000001, 89680], [0.0935, 89670], [0.0936, 89650], [0.0937, 89640], [0.09380000000000001, 89620], [0.09390000000000001, 89610], [0.094, 89600], [0.0941, 89580], [0.0942, 89570], [0.09430000000000001, 89550], [0.09440000000000001, 89540], [0.0945, 89520], [0.0946, 89510], [0.0947, 89500], [0.09480000000000001, 89480], [0.09490000000000001, 89470], [0.095, 89450], [0.0951, 89440], [0.0952, 89420], [0.09530000000000001, 89410], [0.09540000000000001, 89400], [0.0955, 89380], [0.0956, 89370], [0.09570000000000001, 89350], [0.09580000000000001, 89340], [0.0959, 89320], [0.096, 89310], [0.0961, 89300], [0.09620000000000001, 89280], [0.09630000000000001, 89270], [0.0964, 89250], [0.0965, 89240], [0.0966, 89230], [0.09670000000000001, 89210], [0.09680000000000001, 89200], [0.0969, 89180], [0.097, 89170], [0.0971, 89150], [0.09720000000000001, 89140], [0.09730000000000001, 89130], [0.0974, 89110], [0.0975, 89100], [0.0976, 89080], [0.09770000000000001, 89070], [0.09780000000000001, 89050], [0.0979, 89040], [0.098, 89030], [0.0981, 89010], [0.09820000000000001, 89000], [0.09830000000000001, 88980], [0.0984, 88970], [0.0985, 88950], [0.09860000000000001, 88940], [0.0987, 88930], [0.09880000000000001, 88910], [0.0989, 88900], [0.099, 88880], [0.09910000000000001, 88870], [0.0992, 88850], [0.09930000000000001, 88840], [0.0994, 88830], [0.0995, 88810], [0.09960000000000001, 88800], [0.0997, 88780], [0.09980000000000001, 88770], [0.0999, 88750]]
        self.ans = L

        return True

def main():
    x = solar_power()

    #r = x.check_cap(0, 1854010)
    #print(r)

    #x.daily_sun(show=True)
    #x.min_area()

    #x.sim_stored_2020_04_08()

    x.find_min_cap(show=True)
    #x.plot_min_cap_by_area_curve(show=False,erg_unit='J')
    
    
    #x.simulate_dimensions(area=0.05, capacity=100000, num_days=7, show=False, plot_upper=True, plot_lower=True)

main()
