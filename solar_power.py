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
        
        self.ERG = 5450 # Energy used per charge
        self.max_cap = int(1 / (self.INIT - self.MIN) * self.DAYS * self.PERDAY * self.ERG) # = 10/3 * 7 * 18 * self.ERG = 2 163 000 for self.ERG==5150
        self.min_cap = int(1/self.INIT * 4 * self.ERG) # 1/0.5 * 4 (initial runs in darkness) * self.ERG

        self.price_Li = 500 /1000 /3600 # [$USD/J] From: $500 USD / kWh
        self.price_solar = 21.85 * 3.28**2 # [$USD/m^2] From $21.85 USD / ft^2

        ## Class-wide variables for later use
        
        # Store function of area to battery size
        self.ans = []



    ##### Stored Values #####
    def stored_sim_2020Apr9_5450J(self):
        self.ans = [[0.0, 2289000], [0.001, 2245380], [0.002, 2201760], [0.003, 2158140], [0.004, 2114520], [0.005, 2070900], [0.006, 2027280], [0.007, 1983660], [0.008, 1940040], [0.009, 1896410], [0.01, 1852790], [0.011, 1809170], [0.012, 1765550], [0.013, 1721930], [0.014, 1678310], [0.015, 1634690], [0.016, 1591070], [0.017, 1547440], [0.018, 1503820], [0.019, 1460200], [0.02, 1416580], [0.021, 1372960], [0.022, 1329340], [0.023, 1285720], [0.024, 1242100], [0.025, 1198470], [0.026, 1154850], [0.027, 1111230], [0.028, 1067610], [0.029, 1023990], [0.03, 980370], [0.031, 936750], [0.032, 893130], [0.033, 849510], [0.034, 805880], [0.035, 763290], [0.036, 725410], [0.037, 687520], [0.038, 649640], [0.039, 611760], [0.04, 573880], [0.041, 536000], [0.042, 498110], [0.043, 460230], [0.044, 422350], [0.045, 384470], [0.046, 346580], [0.047, 308700], [0.048, 270820], [0.049, 232940], [0.05, 195050], [0.051, 157170], [0.052, 119330], [0.053, 101440], [0.054, 101300], [0.055, 101160], [0.056, 101020], [0.057, 100870], [0.058, 100730], [0.059, 100590], [0.06, 100450], [0.061, 100300], [0.062, 100160], [0.063, 100020], [0.064, 99880], [0.065, 99730], [0.066, 99590], [0.067, 99450], [0.068, 99300], [0.069, 99160], [0.07, 99020], [0.071, 98880], [0.072, 98730], [0.073, 98590], [0.074, 98450], [0.075, 98310], [0.076, 98160], [0.077, 98020], [0.078, 97880], [0.079, 97740], [0.08, 97590], [0.081, 97450], [0.082, 97310], [0.083, 97170], [0.084, 97020], [0.085, 96880], [0.086, 96740], [0.087, 96590], [0.088, 96450], [0.089, 96310], [0.09, 96170], [0.091, 96020], [0.092, 95880], [0.093, 95740], [0.094, 95600], [0.095, 95450], [0.096, 95310], [0.097, 95170], [0.098, 95030], [0.099, 94880], [0.1, 94740], [0.101, 94600], [0.102, 94450], [0.103, 94310], [0.104, 94170], [0.105, 94030], [0.106, 93880], [0.107, 93740], [0.108, 93600], [0.109, 93460], [0.11, 93310], [0.111, 93170], [0.112, 93030], [0.113, 92890], [0.114, 92740], [0.115, 92600], [0.116, 92460], [0.117, 92310], [0.118, 92170], [0.119, 92030], [0.12, 91890], [0.121, 91740], [0.122, 91600], [0.123, 91460], [0.124, 91320], [0.125, 91170], [0.126, 91030], [0.127, 90890], [0.128, 90750], [0.129, 90600], [0.13, 90460], [0.131, 90320], [0.132, 90300], [0.133, 90300], [0.134, 90300], [0.135, 90290], [0.136, 90290], [0.137, 90280], [0.138, 90280], [0.139, 90280], [0.14, 90270], [0.141, 90270], [0.142, 90260], [0.143, 90260], [0.144, 90260], [0.145, 90250], [0.146, 90250], [0.147, 90240], [0.148, 90240], [0.149, 90230], [0.15, 90230], [0.151, 90230], [0.152, 90220], [0.153, 90220], [0.154, 90210], [0.155, 90210], [0.156, 90210], [0.157, 90200], [0.158, 90200], [0.159, 90190], [0.16, 90190], [0.161, 90190], [0.162, 90180], [0.163, 90180], [0.164, 90170], [0.165, 90170], [0.166, 90170], [0.167, 90160], [0.168, 90160], [0.169, 90150], [0.17, 90150], [0.171, 90150], [0.172, 90140], [0.173, 90140], [0.174, 90130], [0.175, 90130], [0.176, 90130], [0.177, 90120], [0.178, 90120], [0.179, 90110], [0.18, 90110], [0.181, 90110], [0.182, 90100], [0.183, 90100], [0.184, 90090], [0.185, 90090], [0.186, 90090], [0.187, 90080], [0.188, 90080], [0.189, 90070], [0.19, 90070], [0.191, 90060], [0.192, 90060], [0.193, 90060], [0.194, 90050], [0.195, 90050], [0.196, 90040], [0.197, 90040], [0.198, 90040], [0.199, 90030], [0.2, 90030], [0.201, 90020], [0.202, 90020], [0.203, 90020], [0.204, 90010], [0.205, 90010], [0.206, 90000], [0.207, 90000], [0.208, 90000], [0.209, 89990], [0.21, 89990], [0.211, 89980], [0.212, 89980], [0.213, 89980], [0.214, 89970], [0.215, 89970], [0.216, 89960], [0.217, 89960], [0.218, 89960], [0.219, 89950], [0.22, 89950], [0.221, 89940], [0.222, 89940], [0.223, 89940], [0.224, 89930], [0.225, 89930], [0.226, 89920], [0.227, 89920], [0.228, 89910], [0.229, 89910], [0.23, 89910], [0.231, 89900], [0.232, 89900], [0.233, 89890], [0.234, 89890], [0.235, 89890], [0.236, 89880], [0.237, 89880], [0.238, 89870], [0.239, 89870], [0.24, 89870], [0.241, 89860], [0.242, 89860], [0.243, 89850], [0.244, 89850], [0.245, 89850], [0.246, 89840], [0.247, 89840], [0.248, 89830], [0.249, 89830], [0.25, 89830], [0.251, 89820], [0.252, 89820], [0.253, 89810], [0.254, 89810], [0.255, 89810], [0.256, 89800], [0.257, 89800], [0.258, 89790], [0.259, 89790], [0.26, 89790], [0.261, 89780], [0.262, 89780], [0.263, 89770], [0.264, 89770], [0.265, 89770], [0.266, 89760], [0.267, 89760], [0.268, 89750], [0.269, 89750], [0.27, 89740], [0.271, 89740], [0.272, 89740], [0.273, 89730], [0.274, 89730], [0.275, 89720], [0.276, 89720], [0.277, 89720], [0.278, 89710], [0.279, 89710], [0.28, 89700], [0.281, 89700], [0.282, 89700], [0.283, 89690], [0.284, 89690], [0.285, 89680], [0.286, 89680], [0.287, 89680], [0.288, 89670], [0.289, 89670], [0.29, 89660], [0.291, 89660], [0.292, 89660], [0.293, 89650], [0.294, 89650], [0.295, 89640], [0.296, 89640], [0.297, 89640], [0.298, 89630], [0.299, 89630], [0.3, 89620], [0.301, 89620], [0.302, 89620], [0.303, 89610], [0.304, 89610], [0.305, 89600], [0.306, 89600], [0.307, 89590], [0.308, 89590], [0.309, 89590], [0.31, 89580], [0.311, 89580], [0.312, 89570], [0.313, 89570], [0.314, 89570], [0.315, 89560], [0.316, 89560], [0.317, 89550], [0.318, 89550], [0.319, 89550], [0.32, 89540], [0.321, 89540], [0.322, 89530], [0.323, 89530], [0.324, 89530], [0.325, 89520], [0.326, 89520], [0.327, 89510], [0.328, 89510], [0.329, 89510], [0.33, 89500], [0.331, 89500], [0.332, 89490], [0.333, 89490], [0.334, 89490], [0.335, 89480], [0.336, 89480], [0.337, 89470], [0.338, 89470], [0.339, 89470], [0.34, 89460], [0.341, 89460], [0.342, 89450], [0.343, 89450], [0.344, 89450], [0.345, 89440], [0.346, 89440], [0.347, 89430], [0.348, 89430], [0.349, 89420], [0.35, 89420], [0.351, 89420], [0.352, 89410], [0.353, 89410], [0.354, 89400], [0.355, 89400], [0.356, 89400], [0.357, 89390], [0.358, 89390], [0.359, 89380], [0.36, 89380], [0.361, 89380], [0.362, 89370], [0.363, 89370], [0.364, 89360], [0.365, 89360], [0.366, 89360], [0.367, 89350], [0.368, 89350], [0.369, 89340], [0.37, 89340], [0.371, 89340], [0.372, 89330], [0.373, 89330], [0.374, 89320], [0.375, 89320], [0.376, 89320], [0.377, 89310], [0.378, 89310], [0.379, 89300], [0.38, 89300], [0.381, 89300], [0.382, 89290], [0.383, 89290], [0.384, 89280], [0.385, 89280], [0.386, 89280], [0.387, 89270], [0.388, 89270], [0.389, 89260], [0.39, 89260], [0.391, 89250], [0.392, 89250], [0.393, 89250], [0.394, 89240], [0.395, 89240], [0.396, 89230], [0.397, 89230], [0.398, 89230], [0.399, 89220], [0.4, 89220], [0.401, 89210], [0.402, 89210], [0.403, 89210], [0.404, 89200], [0.405, 89200], [0.406, 89190], [0.407, 89190], [0.408, 89190], [0.409, 89180], [0.41, 89180], [0.411, 89170], [0.412, 89170], [0.413, 89170], [0.414, 89160], [0.415, 89160], [0.416, 89150], [0.417, 89150], [0.418, 89150], [0.419, 89140], [0.42, 89140], [0.421, 89130], [0.422, 89130], [0.423, 89130], [0.424, 89120], [0.425, 89120], [0.426, 89110], [0.427, 89110], [0.428, 89100], [0.429, 89100], [0.43, 89100], [0.431, 89090], [0.432, 89090], [0.433, 89080], [0.434, 89080], [0.435, 89080], [0.436, 89070], [0.437, 89070], [0.438, 89060], [0.439, 89060], [0.44, 89060], [0.441, 89050], [0.442, 89050], [0.443, 89040], [0.444, 89040], [0.445, 89040], [0.446, 89030], [0.447, 89030], [0.448, 89020], [0.449, 89020], [0.45, 89020], [0.451, 89010], [0.452, 89010], [0.453, 89000], [0.454, 89000], [0.455, 89000], [0.456, 88990], [0.457, 88990], [0.458, 88980], [0.459, 88980], [0.46, 88980], [0.461, 88970], [0.462, 88970], [0.463, 88960], [0.464, 88960], [0.465, 88960], [0.466, 88950], [0.467, 88950], [0.468, 88940], [0.469, 88940], [0.47, 88930], [0.471, 88930], [0.472, 88930], [0.473, 88920], [0.474, 88920], [0.475, 88910], [0.476, 88910], [0.477, 88910], [0.478, 88900], [0.479, 88900], [0.48, 88890], [0.481, 88890], [0.482, 88890], [0.483, 88880], [0.484, 88880], [0.485, 88870], [0.486, 88870], [0.487, 88870], [0.488, 88860], [0.489, 88860], [0.49, 88850], [0.491, 88850], [0.492, 88850], [0.493, 88840], [0.494, 88840], [0.495, 88830], [0.496, 88830], [0.497, 88830], [0.498, 88820], [0.499, 88820], [0.5, 88810], [0.501, 88810], [0.502, 88810], [0.503, 88800], [0.504, 88800], [0.505, 88790], [0.506, 88790], [0.507, 88780], [0.508, 88780], [0.509, 88780], [0.51, 88770], [0.511, 88770], [0.512, 88760], [0.513, 88760], [0.514, 88760], [0.515, 88750], [0.516, 88750], [0.517, 88740], [0.518, 88740], [0.519, 88740], [0.52, 88730], [0.521, 88730], [0.522, 88720], [0.523, 88720], [0.524, 88720], [0.525, 88710], [0.526, 88710], [0.527, 88700], [0.528, 88700], [0.529, 88700], [0.53, 88690], [0.531, 88690], [0.532, 88680], [0.533, 88680], [0.534, 88680], [0.535, 88670], [0.536, 88670], [0.537, 88660], [0.538, 88660], [0.539, 88660], [0.54, 88650], [0.541, 88650], [0.542, 88640], [0.543, 88640], [0.544, 88640], [0.545, 88630], [0.546, 88630], [0.547, 88620], [0.548, 88620], [0.549, 88610], [0.55, 88610], [0.551, 88610], [0.552, 88600], [0.553, 88600], [0.554, 88590], [0.555, 88590], [0.556, 88590], [0.557, 88580], [0.558, 88580], [0.559, 88570], [0.56, 88570], [0.561, 88570], [0.562, 88560], [0.563, 88560], [0.564, 88550], [0.565, 88550], [0.566, 88550], [0.567, 88540], [0.568, 88540], [0.569, 88530], [0.57, 88530], [0.571, 88530], [0.572, 88520], [0.573, 88520], [0.574, 88510], [0.575, 88510], [0.576, 88510], [0.577, 88500], [0.578, 88500], [0.579, 88490], [0.58, 88490], [0.581, 88490], [0.582, 88480], [0.583, 88480], [0.584, 88470], [0.585, 88470], [0.586, 88470], [0.587, 88460], [0.588, 88460], [0.589, 88450], [0.59, 88450], [0.591, 88440], [0.592, 88440], [0.593, 88440], [0.594, 88430], [0.595, 88430], [0.596, 88420], [0.597, 88420], [0.598, 88420], [0.599, 88410], [0.6, 88410], [0.601, 88400], [0.602, 88400], [0.603, 88400], [0.604, 88390], [0.605, 88390], [0.606, 88380], [0.607, 88380], [0.608, 88380], [0.609, 88370], [0.61, 88370], [0.611, 88360], [0.612, 88360], [0.613, 88360], [0.614, 88350], [0.615, 88350], [0.616, 88340], [0.617, 88340], [0.618, 88340], [0.619, 88330], [0.62, 88330], [0.621, 88320], [0.622, 88320], [0.623, 88320], [0.624, 88310], [0.625, 88310], [0.626, 88300], [0.627, 88300], [0.628, 88290], [0.629, 88290], [0.63, 88290], [0.631, 88280], [0.632, 88280], [0.633, 88270], [0.634, 88270], [0.635, 88270], [0.636, 88260], [0.637, 88260], [0.638, 88250], [0.639, 88250], [0.64, 88250], [0.641, 88240], [0.642, 88240], [0.643, 88230], [0.644, 88230], [0.645, 88230], [0.646, 88220], [0.647, 88220], [0.648, 88210], [0.649, 88210], [0.65, 88210], [0.651, 88200], [0.652, 88200], [0.653, 88190], [0.654, 88190], [0.655, 88190], [0.656, 88180], [0.657, 88180], [0.658, 88170], [0.659, 88170], [0.66, 88170], [0.661, 88160], [0.662, 88160], [0.663, 88150], [0.664, 88150], [0.665, 88150], [0.666, 88140], [0.667, 88140], [0.668, 88130], [0.669, 88130], [0.67, 88120], [0.671, 88120], [0.672, 88120], [0.673, 88110], [0.674, 88110], [0.675, 88100], [0.676, 88100], [0.677, 88100], [0.678, 88090], [0.679, 88090], [0.68, 88080], [0.681, 88080], [0.682, 88080], [0.683, 88070], [0.684, 88070], [0.685, 88060], [0.686, 88060], [0.687, 88060], [0.688, 88050], [0.689, 88050], [0.69, 88040], [0.691, 88040], [0.692, 88040], [0.693, 88030], [0.694, 88030], [0.695, 88020], [0.696, 88020], [0.697, 88020], [0.698, 88010], [0.699, 88010], [0.7, 88000], [0.701, 88000], [0.702, 88000], [0.703, 87990], [0.704, 87990], [0.705, 87980], [0.706, 87980], [0.707, 87970], [0.708, 87970], [0.709, 87970], [0.71, 87960], [0.711, 87960], [0.712, 87950], [0.713, 87950], [0.714, 87950], [0.715, 87940], [0.716, 87940], [0.717, 87930], [0.718, 87930], [0.719, 87930], [0.72, 87920], [0.721, 87920], [0.722, 87910], [0.723, 87910], [0.724, 87910], [0.725, 87900], [0.726, 87900], [0.727, 87890], [0.728, 87890], [0.729, 87890], [0.73, 87880], [0.731, 87880], [0.732, 87870], [0.733, 87870], [0.734, 87870], [0.735, 87860], [0.736, 87860], [0.737, 87850], [0.738, 87850], [0.739, 87850], [0.74, 87840], [0.741, 87840], [0.742, 87830], [0.743, 87830], [0.744, 87830], [0.745, 87820], [0.746, 87820], [0.747, 87810], [0.748, 87810], [0.749, 87800], [0.75, 87800], [0.751, 87800], [0.752, 87790], [0.753, 87790], [0.754, 87780], [0.755, 87780], [0.756, 87780], [0.757, 87770], [0.758, 87770], [0.759, 87760], [0.76, 87760], [0.761, 87760], [0.762, 87750], [0.763, 87750], [0.764, 87740], [0.765, 87740], [0.766, 87740], [0.767, 87730], [0.768, 87730], [0.769, 87720], [0.77, 87720], [0.771, 87720], [0.772, 87710], [0.773, 87710], [0.774, 87700], [0.775, 87700], [0.776, 87700], [0.777, 87690], [0.778, 87690], [0.779, 87680], [0.78, 87680], [0.781, 87680], [0.782, 87670], [0.783, 87670], [0.784, 87660], [0.785, 87660], [0.786, 87660], [0.787, 87650], [0.788, 87650], [0.789, 87640], [0.79, 87640], [0.791, 87630], [0.792, 87630], [0.793, 87630], [0.794, 87620], [0.795, 87620], [0.796, 87610], [0.797, 87610], [0.798, 87610], [0.799, 87600], [0.8, 87600], [0.801, 87590], [0.802, 87590], [0.803, 87590], [0.804, 87580], [0.805, 87580], [0.806, 87570], [0.807, 87570], [0.808, 87570], [0.809, 87560], [0.81, 87560], [0.811, 87550], [0.812, 87550], [0.813, 87550], [0.814, 87540], [0.815, 87540], [0.816, 87530], [0.817, 87530], [0.818, 87530], [0.819, 87520], [0.82, 87520], [0.821, 87510], [0.822, 87510], [0.823, 87510], [0.824, 87500], [0.825, 87500], [0.826, 87490], [0.827, 87490], [0.828, 87480], [0.829, 87480], [0.83, 87480], [0.831, 87470], [0.832, 87470], [0.833, 87460], [0.834, 87460], [0.835, 87460], [0.836, 87450], [0.837, 87450], [0.838, 87440], [0.839, 87440], [0.84, 87440], [0.841, 87430], [0.842, 87430], [0.843, 87420], [0.844, 87420], [0.845, 87420], [0.846, 87410], [0.847, 87410], [0.848, 87400], [0.849, 87400], [0.85, 87400], [0.851, 87390], [0.852, 87390], [0.853, 87380], [0.854, 87380], [0.855, 87380], [0.856, 87370], [0.857, 87370], [0.858, 87360], [0.859, 87360], [0.86, 87360], [0.861, 87350], [0.862, 87350], [0.863, 87340], [0.864, 87340], [0.865, 87340], [0.866, 87330], [0.867, 87330], [0.868, 87320], [0.869, 87320], [0.87, 87310], [0.871, 87310], [0.872, 87310], [0.873, 87300], [0.874, 87300], [0.875, 87290], [0.876, 87290], [0.877, 87290], [0.878, 87280], [0.879, 87280], [0.88, 87270], [0.881, 87270], [0.882, 87270], [0.883, 87260], [0.884, 87260], [0.885, 87250], [0.886, 87250], [0.887, 87250], [0.888, 87240], [0.889, 87240], [0.89, 87230], [0.891, 87230], [0.892, 87230], [0.893, 87220], [0.894, 87220], [0.895, 87210], [0.896, 87210], [0.897, 87210], [0.898, 87200], [0.899, 87200], [0.9, 87190], [0.901, 87190], [0.902, 87190], [0.903, 87180], [0.904, 87180], [0.905, 87170], [0.906, 87170], [0.907, 87160], [0.908, 87160], [0.909, 87160], [0.91, 87150], [0.911, 87150], [0.912, 87140], [0.913, 87140], [0.914, 87140], [0.915, 87130], [0.916, 87130], [0.917, 87120], [0.918, 87120], [0.919, 87120], [0.92, 87110], [0.921, 87110], [0.922, 87100], [0.923, 87100], [0.924, 87100], [0.925, 87090], [0.926, 87090], [0.927, 87080], [0.928, 87080], [0.929, 87080], [0.93, 87070], [0.931, 87070], [0.932, 87060], [0.933, 87060], [0.934, 87060], [0.935, 87050], [0.936, 87050], [0.937, 87040], [0.938, 87040], [0.939, 87040], [0.94, 87030], [0.941, 87030], [0.942, 87020], [0.943, 87020], [0.944, 87020], [0.945, 87010], [0.946, 87010], [0.947, 87000], [0.948, 87000], [0.949, 86990], [0.95, 86990], [0.951, 86990], [0.952, 86980], [0.953, 86980], [0.954, 86970], [0.955, 86970], [0.956, 86970], [0.957, 86960], [0.958, 86960], [0.959, 86950], [0.96, 86950], [0.961, 86950], [0.962, 86940], [0.963, 86940], [0.964, 86930], [0.965, 86930], [0.966, 86930], [0.967, 86920], [0.968, 86920], [0.969, 86910], [0.97, 86910], [0.971, 86910], [0.972, 86900], [0.973, 86900], [0.974, 86890], [0.975, 86890], [0.976, 86890], [0.977, 86880], [0.978, 86880], [0.979, 86870], [0.98, 86870], [0.981, 86870], [0.982, 86860], [0.983, 86860], [0.984, 86850], [0.985, 86850], [0.986, 86850], [0.987, 86840], [0.988, 86840], [0.989, 86830], [0.99, 86830], [0.991, 86820], [0.992, 86820], [0.993, 86820], [0.994, 86810], [0.995, 86810], [0.996, 86800], [0.997, 86800], [0.998, 86800], [0.999, 86790]]
        return True

    def stored_sim_2020Apr9_reduced(self):
        self.ans = []
        return True
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
        elif unitA == 'J':
            if unitB == 'J':
                return value
            elif unitB == 'kJ':
                return value / 1000
            elif unitB == 'Wh':
                return value / 3600
            elif unitB == 'kWh':
                return value / 3600 / 1000
        elif unitA == 'Wh':
            if unitB == 'Wh':
                return value
            elif unitB == 'kWh':
                return value / 1000
            elif unitB == 'J':
                return 3600 * value
            elif unitB == 'kJ':
                return 3600 * value / 1000
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




    ##### PART I & III: Energy Requirements #####

    def daily_use(self,show=False):
        """
        Returns daily energy use in [J/day]
        """
        day_use = self.PERDAY * self.ERG

        if show == True:
            print('Daily use:',day_use,'\t[J]')
        return day_use

    def min_area(self, show=False):
        """
        Calculate the minimum area of solar panelling needed to power the robot, neglecting storage capacity limitaions.
        """
        
        # Calculate mininum area
        min_area = self.daily_use(show=show) / self.daily_sun(show=False)
        
        if show == True:
            print('One m^2 of solar panelling at', self.EFF, 'efficiency can generate enough energy to power', 1/min_area, 'robots!\n\n')
            
            print('The minimum area of the solar panel (neglecting storage capacity limitations) is:')
            print('\t\t =',min_area, '/t/t [m^2]')
            print('\t\t =',min_area*100*100, '/t/t [cm^2]\n\n')

        return min_area



    ##### PART I & II: Cost of the Solar Panel #####

    def cost(self,area,capacity):
        return round(self.price_solar*area + self.price_Li*capacity,2)




    ##### PART IV: Find dimensions #####
    
    def find_min_cap(self,lower=0,upper=0.1,steps=1000,show=False):
        N = steps # Number of steps
        h = lower # Lower bound
        k = upper # Upper bound
        

        self.ans = [] # Reset self.ans


        
        for i in range(0,N,1): # Check areas (0,N)
            area = h + i*k/N

            if i == 0:
                if area == 0 and self.ERG == 5150: 
                    capacity = self.max_cap
                else:
                    capacity = math.floor(1/self.INIT*(4*self.ERG)/10)*10  # Minimum capacity (0.5 -> 0 in one day): floor(2*(4*ERG), -1)
                    
                while self.check_cap(area, capacity) == False:
                    capacity += 10

                    if capacity > self.max_cap: 
                        print('ERROR: Exceeded bounds... somebody\'s math is wrong!')
                        break
            else:
                capacity = ans[1] # Take previous capacity

                while self.check_cap(area, capacity) == True:
                    capacity -= 10

                    if capacity < self.min_cap: 
                        print('ERROR: Something actually went wrong!')
                        break

                capacity += 10 # Add 10 back to capacity, to make it work again   

            ans = [area, capacity]
            if show == True:
                print('Area and Capacity:', ans)
            
            self.ans += [ans]

        if show == True:
            print('Capacity as a function of Area: ',self.ans)
    
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
        
        for i in range(0,len(self.ans),1):
            area += [self.ans[i][0]]
            capacity += [self.convert(self.ans[i][1],'J',erg_unit)]

            max_cap += [1854000] #3.3*(4*self.ERG)
            min_cap += [420 * self.ERG]

        if show == True:
            print('Minimum capacity [J] as a function of Area:', self.ans)
            print('Energy unit:', erg_unit)
            print('Minimum capacity ['+erg_unit+'] as a function of Area:', capacity)

        plt.plot(area,capacity, label='Minimum Battery size for Given Area')
        plt.xlabel('Area [m^2]')
        plt.ylabel('Size of Battery ['+erg_unit+']')
        plt.title('Minimum Battery size for a given Area Curve')
        plt.legend()
        plt.show()
        
        return True




    ##### PART III & IV: Simulate Area and Capacities #####

    def simulate_dimensions(self, area, capacity, num_days=1, erg_unit='J', show=False, plot_upper=True, plot_lower=False):
        sim_battery = []
        sim_collect = []

        # Initiate battery levels
        battery = self.INIT * capacity
        
        collect = [] # Function of how much sun it gets
        for i in self.COLLECT:
            collect += [area * i]

        # Show values it will plot
        if show == True:
            print('Area:', area, '\n')
            print('COLLECT [J/15 min/m^2]:', self.COLLECT, '\nSum of COLLECT:', sum(self.COLLECT), '\n')
            print('collect [J/15 min]:',collect, '\nSum of collect:', sum(collect),'\n')

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
        title = str(num_days) + ' Day Simulation of '+str(area)+ ' m^2 Solar Panel \n and \n '+str(round(self.convert(capacity,'J',erg_unit),2))+' '+erg_unit+' battery'
        for i in range(0,num_days*len(collect),1):
            time += [i*0.25]

        plt.plot(time,sim_battery, 'b', label='Battery Charge')
        plt.plot(time, sim_collect, 'xkcd:orange', label='Solar Energy Collected in 15 minutes')

        if plot_upper == True:
            upper = []
            for i in range(len(time)):
                upper += [capacity]

            plt.plot(time, upper, 'g--', label='Maximum Capacity of Battery')

        if plot_lower == True:
            lower = []
            for i in range(len(time)):
                lower += [0.2 * capacity]

            plt.plot(time, lower, 'r--', label='Minimum Allowable Battery Charge')
        
        plt.xlabel('Time [h]')
        plt.ylabel('Energy ['+erg_unit+']')
        plt.title(title)
        plt.legend(loc='upper left')
        plt.show()

        return True






    ##### PART IV: Optimization for Cost #####
    
    def best_cost(self,show=False):

        price = []
        area = []

        for i in range(0,len(self.ans),1):
            price += [self.cost(self.ans[i][0],self.ans[i][1])]
            area += [self.ans[i][0]]

        min_price = price[0]
        min_index = 0
        
        for i in range(0,len(price),1):
            if price[i] < min_price:
                min_price = price[i]
                min_index = i

        plt.plot(area, price)
        plt.title('Price of the System by Area of Solar Panel')
        plt.xlabel('Area [m^2]')
        plt.ylabel('Price [$ USD]')
        plt.show()
        
        if show == True:
            print('The minimum price is:', price[min_index],'at index',min_index)
            print('The dimensions are: AREA =', self.ans[min_index][0], 'BATTERY =',self.ans[min_index][1])
        return min_index

    def optimal_dimensions(self):
        min_index = self.best_cost(False)
        return self.ans[min_index]
            

        
          

def main():
    x = solar_power()
    #"""
    # Part 2.1
    print('\n\n\t\t>>> PART 2.1 <<<\n\n')
    x.daily_sun(show=True)
    raw_area = x.min_area(show=True)
    ar = round(math.ceil(100*raw_area)/100,2)
    print('\n\nCost of',ar, 'm^2 solar panel is $', x.cost(raw_area,capacity=0), 'USD')
    #"""

    #"""
    # Part 2.2
    print('\n\n\t\t>>> PART 2.2 <<<\n\n')
    cap = 100000
    print('Cost of a 27.78 Wh (100000 J) Li-battery is $', x.cost(area=0,capacity=cap),'USD')
    #"""

    #"""
    # Part 2.3
    print('\n\n\t\t>>> PART 2.3 <<<\n\n')
    x.simulate_dimensions(area=ar,capacity=cap,num_days=1,erg_unit='Wh',show=False,plot_upper=True,plot_lower=False)
    print('Cost of',ar, 'm^2 solar panel and',x.convert(cap,'J','Wh'),'Wh ('+str(cap),'J) Li-battery is $', x.cost(area=raw_area,capacity=cap),'USD')
    #"""

    #"""
    # Part 2.4
    print('\n\n\t\t>>> PART 2.4 <<<\n\n')
    #x.find_min_cap(lower=0,upper=1,steps=1000, show=True) # Computes the values from scratch, but it is slow
    x.stored_sim_2020Apr9_5450J() # This is faster, since I already computed the values

    # Plot minimum battery size as a function of area
    x.plot_min_cap_by_area_curve(show=False,erg_unit='Wh')

    # Find optimal dimensions
    r = x.optimal_dimensions()

    # Simulate optimal dimensions
    x.simulate_dimensions(r[0],r[1],7,'Wh',show=False,plot_upper=True, plot_lower=True)
    target_unit = 'Wh'
    print('Cost of',r[0], 'm^2 of solar panelling and',x.convert(r[1],'J',target_unit),target_unit,'of battery capacity: $',x.cost(r[0],r[1]),'USD')
    #"""

    #"""
    # Discussion
    print('\n\n\t\t>>> DISCUSSION <<<\n\n')
    new_area = 2*r[0]
    new_cap = 1.25*r[1]
    target_unit_2 = 'Wh'
    print('New solar panel area:', new_area, '[m^2]')
    print('New battery capacity:', x.convert(new_cap,'J','Wh') , '['+target_unit_2+']')
    print('\n\nNew cost for 7 % efficient solar panels and only 0.8 of a useable battery: $', x.cost(2*r[0],1.25*r[1]))
    
    #"""

    input('\n\nPRESS ENTER TO ESCAPE')
    
    return True

main()
