import numpy as np

from generalLibrary import printDebug, plotDebug

# global debug flag
DEBUG = {
    "all": False,
    "VLC": True,
    "Message": False,
    "Transmitter": False,
    "Mapping": False,
    "Modulator": False,
    "OFDM": False,
    "DAC": False,
    "Channel": False,
    "LightSource": False,
    "Receiver": False,
    "Detector": False,
    "ADC": False,
    "ROIC": False,
    "BouncingPixel": False,
    "Simulator": False,
    "Virtuoso": False,
    "Tanner": False,
    "MeritFunctions": True,
    "SimulationSync": True
}

# global plot flag
PLOT = {
    "all": False,
    "VLC": False,
    "Message": False,
    "Transmitter": False,
    "Mapping": False,
    "Modulator": False,
    "OFDM": True,
    "DAC": False,
    "Channel": False,
    # "Channel": True,
    "LightSource": False,
    "Receiver": False,
    "Detector": False,
    "ADC": False,
    "ROIC": False,
    "BouncingPixel": False,
    "Simulator": False,
    "Virtuoso": False,
    "Tanner": False,
    "MeritFunctions": False,
    "SimulationSync": False
}


# Dict with all bypass flags
bypass_dict = {
    "Modulator": False,
    "LightSource": True,
    # "DAC": True,
    "DAC": False,
    "DAC_rounding_or_simul": True,
    "Channel": True,
    "Detector": True,
    # "ROIC": False, ## Read-Out Integrated Circuit ON
    "ROIC": True, ## NO ROIC
    "ADC": True,
    "ADC_rounding_or_simul": True
}

# Random SEED for all random simulation (does not work yet... 
# try with very low SNR and reproduce BER)
rand_seed = 10

# TODO --- FIX ISSUE WITH << "DAC": False >>, where only
# abs of signal is passed through. Needs to apply hermitian symetry in this case!


# TODO --- MUST ADD OPTION TO USE H(0) or h(t)


# simulation time frame [1/(operating frequency)] for each transaction
time_frame = 50e-6
time_frame = 5e-6
time_frame = 1e-6
# time_frame = 0.3e-6
# time_frame = 2e-6
# time_frame = 50e-9

# time step in seconds for simulation
time_step = 1e-11
time_step = 1e-9
# time_step = 2e-9
# time_step = 0.5e-9
# time_step = 10e-9

# operating frequency is inverse of time frame (???? at least for OFDM, I guess...)
# calculated on the modulator ???
# sample_frequency = None
# sample_frequency = 1/time_step
simul_frequency = 1/time_step


# Circuit PCB voltage (VDD)
VDD = 3.3
VSS = 0


# Total number of points in simulation.
# This is to define a fixed number of points
# If you have less, data will be interpolated
number_of_points = int(time_frame/time_step)

# base time vector
base_time_vector = np.arange(0, number_of_points)*time_step

# number of points in the simulation
# printDebug(time_frame/time_step)
# N_POINTS = 12
# N_POINTS = int(time_frame/time_step)
# full_time_vector = np.arange(0,N_POINTS)*time_step

# # To be calculated through the simulation.
# # It's equal base_time_vector if only one frame.
# # And increments each step with base_time_vector + time_frame
# full_time_vector = None

# list of channel responses for each lamp, when bypassig Channel.

# Unitary channel
# list_of_channel_response = [1*np.array([1])]
# list_of_channel_response = [1*np.array([np.random.uniform()+np.random.uniform()*1j, (np.random.uniform()+np.random.uniform()*1j)/2, (np.random.uniform()+np.random.uniform()*1j)/4])]
# list_of_channel_response = [1*np.array([1, 0, 0.3+0.3j])]
# from scipy import signal
# CIR = signal.windows.hann(8)

# G*delta(t-d/c)
# N_POINTS = 120
# CIR = 2*signal.unit_impulse(N_POINTS, 5) + 0.5*signal.unit_impulse(N_POINTS, 8)

# Channel response types
# impulse = (gain, delay); delay --> t - d/c

# light speed (m/s)
c_speed = 3e8
# test (distance in m)
# gain (inverse of distance) --> resp = dist/kappa
attenuation = 1
# attenuation = 0.3
group_delay = 100e-9
group_delay = 200e-9
# group_delay = 900e-9
# group_delay = 0e-9
# group_delay = 0
dist = [1, 1.2, 1.4, 1.9, 2.3, 5, 20]
# dist = [1, 2.3]
# dist = [1]
dist = list(np.array(dist))
response = [(attenuation/(d**2), group_delay+d/c_speed) for d in dist]
# response = [(1, 200e-9), (1, 500e-9)]
# response = [(0.5, 200e-9), (0.5, 1900e-9), (0.5, 1000e-9)]
# response = [(1, 50e-9)]
# response = [(1, 20e-9)]
# response = [(1, 10e-9)]
# response = [(1, 5e-9)]
# response = [(1, 200e-9)]
# group_delay = 50e-9
# group_delay = 200e-9
response = [(1, 0)]
group_delay = 0
# variable used for synchronization
# TODO --- if None, returns full signal after convolution, 
# to be used for further correlation, to find group_delay
# TODO --- otherwise, use it to shift signal in time
# group_delay = None
# group_delay = 0
# group_delay = 50e-9
print(response)
print(dist)
# sad
CIR = {
    0: {"impulse": [(1, 1e-9)]},
    1: {"impulse": [(1, 250e-9), (1, 500e-9)]},
    2: {"impulse": [(1, 2e-9), (0.7, 3e-9)]},
    3: {"butter": response},
    4: {"impulse": response},
    9: {"others": []}
}


# b, a = signal.butter(1, 0.2)
# CIR = signal.lfilter(b, a, CIR)

# list_of_channel_response = [ 1*DELTA(T-T0)]
# list_of_channel_response = [ G0*DELTA(T-T0) + g1*DELTA(T-T1)  ]

# CIR = signal.unit_impulse(10, 'mid')
# CIR = signal.unit_impulse(256, 2)
# import matplotlib.pyplot as plt
# plt.plot(t, y)
# CIR = signal.unit_impulse(10)
# CIR = GAIN*np.array([1])

list_of_channel_response = [CIR[3]]
list_of_channel_response = [CIR[4]]

# list_of_channel_response = [CIR[0], CIR[1]]
# plotDebug(CIR, symbols='r-o')
# list_of_channel_response = [0.1*np.array([1, 0, 0.3+0.3j])]

# rx_SNR (dB) is ued if not set, if not calculated. Can use <None> to ignore noise
rx_SNR_dB = None
# rx_SNR_dB = 50
# rx_SNR_dB = 30
# rx_SNR_dB = 25
# rx_SNR_dB = 20
# rx_SNR_dB = 10

# TODO --- add timeunits to the program
timeunit = "ns"

# Contains list of dicts with all information needed to configure the lights on the Transmitter. Each position has a dict, with the type of light, the position for each lamp, and angle. Can be used to configure more than one array of lamps.
transmitter_config = [{"light_type": ["LED"], "position": [(0,0,0)], "angle": [(0,0)], "database": ["path_to_database"]}]

# Contains list of dicts with all information needed to configure the detectors on the receiver. Each position has a dict, with the type of detector, the position for each detector, and angle. Can be used to configure more than one array of detectors.
receiver_config = [{"detector_type": ["photodiode"], "position": [(0,0,0)], "angle": [(0,0)], "database": ["path_to_database"]}]


# Contains list of dicts with all information needed to configure the ROICs on the receiver.
# Each position has a dict, with the type of ROIC, associated with each corresponding detector.
# Can be used to configure more than one array of ROICs.
# Also, set if will do circuit simulation or not.
# Use the simularion to extract the metrics such as DR, SNR, gain, input referred current noise (current_noise), etc.
# Then, use the metrics instead of the simulation
roic_config = [{
    "circuit_simulation": [False], ## ROIC simulation OFF
    # "circuit_simulation": [True], ## ROIC simulation ON
    "circuit_type": ["BouncingPixel"],
    # "roic_setup": [{"vmin": "500m", "vmax": "2.5", "stepTran": "1000"}],
    # "roic_setup": [{"vmin": "500m", "vmax": "2.5", "stepTran": "10000"}],
    # "roic_setup": [{"vmin": "700m", "vmax": "2", "stepTran": "500"}],
    "roic_setup": [{"vmin": "500m", "vmax": "2.5", "stepTran": "100"}],
    "gain": [60*1e3],
    "DR": [130],
    "current_noise": [1e-9],
    "SNR": [144],
    "waves_name": ["vout"]
    }]

############### PHYSICAL VARIABLES ###############
# List of all wavelengths to be considered during simulation, in nm.
wavelenghts = [550]

# Temperature in Kelvin.
temperature = 300

############### CIRCUIT SIMULATOR ###############

simulator_config = {
    "Tanner": {
        "Windows": {
            "library": r"C:\IR2\bibliotecas\AMSC35_14.3\SPICE_MODELS",
            "tspice": r"C:\Program Files\Tanner EDA\Tanner Tools v15.0\tspcmd.exe",
            "netlist": r"C:\IR2\VLC\source_netlists\BouncingPixel.sv",
            "data_folder": r"C:\IR2\VLC",
            "simul_corner": "tm"
            },
        "Linux": {
            "path": r"...."
            }
        },
    "Virtuoso": {
        "Windows": {
            "path": r"...."
            },
        "Linux": {
            "path": r"...."
            }
        },
    "None": {
        "NO_OS": {
            "path": None
            }
        }
}

##### Defines the simulator to be used, if appliable.
# which_simulator = "Virtuoso"
which_simulator = "Tanner"
# which_simulator = "None"

operating_system = "Windows"
# operating_system = "Linux"


# Intensity Modulation / Direct Detection (IM_DD) -- always on for VLC/LiFi [flag kept only for completion]
IM_DD = True
# IM_DD = False

################################### < FLAGS > ###################################
# Flag to remove padded zeros before analysis (must be setup for images... fix later)
remove_padded_zeros = False
remove_padded_zeros = True

# Flag to indicate use of raytrace, or not, for the CIR estimation
use_raytrace = False
# use_raytrace = True (NOT SUPPORTED YET)

# Flag to use pyfft (wrapper for FFTW, that is faster), istead of numpy fft
use_pyfft = True
# use_pyfft = False

# Enable multi_theading or not pos [0] and number of threads pos [1]
multi_theading = [True, 4]
multi_theading = [True, 40]
multi_theading = [False, None]

################################### > FLAGS < ###################################

# Input info structure
input_info = {"type": ["str", "str"], "data": ["Primeiro", "Segundo"]}
input_info = {"type": ["str", "str"], "data": ["Hello, Motto!", "Uma frase beeeem longaaaaaaaaaaa!"]}
# input_info = {"type": ["text"], "data": [r"../data/test.txt"]}
input_info = {"type": ["str"], "data": ["mini msg!"]}
# input_info = {"type": ["str"], "data": ["mensagem media...!"]}
input_info = {"type": ["str"], "data": ["Uma frase beeeem longaaaaaaaaaaa!"]}
# input_info = {"type": ["str"], "data": ["A vida eh curta, por isso viva a vida bem vivida!"]}
# input_info = {"type": ["image"], "data": [r"../data/test.png"], "n_bytes": [3]}
# input_info = {"type": ["image"]*2, "data": [r"../data/test.png", r"../data/test_larger.png"], "n_bytes": [3]*2}
# input_info = {"type": ["image", "str"], "data": [r"../data/test.png", "Uma frase beeeem longaaaaaaaaaaa!"], "n_bytes": [3]*2}
# input_info = {"type": ["image"], "data": [r"../data/test_larger.png"], "n_bytes": [3]}
# input_info = {"type": ["image"], "data": [r"../data/zebra.png"], "n_bytes": [3]}
# input_info = {"type": ["image"], "data": [r"../data/zebra_large.png"], "n_bytes": [3]}
# input_info = {"type": ["bin"], "data": ["10"]}
import random
# input_info = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 32)])]}
input_info = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 64)])]}
# input_info = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 2**3)])]}
# input_info = {"type": ["bin"], "data": ["0110011001100110"]}
# input_info = {"type": ["bin"], "data": ["0000000000000000000000000000000011111111111111111111111111111111"]}
# input_info = {"type": ["bin"], "data": ["1111111111111111111111111111111100000000000000000000000000000000"]}
# input_info = {"type": ["bin"], "data": ["11111111111111111111111111111111"]}

# supported input_info types
supported_input_info = ["str", "image", "audio"]

# DCO_OFDM_CONFIG = {"DCO-OFDM": [0]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [0.5]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [1.5]}
DCO_OFDM_CONFIG = {"DCO-OFDM": [5]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [19]}

ACO_OFDM_CONFIG = {"ACO-OFDM": []}

# slack for hermitian imaginary part (check that imaginary part
#  is [img <= slack]. instead of [img == 0])
hermitian_slack = 1e-6

# Number of FFT points
# N_FFT = 16
N_FFT = 32
N_FFT = 64
N_FFT = 128
# N_FFT = 256
# N_FFT = 512
# N_FFT = 1024

# percentage of pilots, depending on number of FFT carriers 
percentage_of_pilots = 0.4
percentage_of_pilots = 0.3
# percentage_of_pilots = 0.125
# percentage_of_pilots = 0.2

# pilot_value
# pilot_value = 15+15j
pilot_value = 7+7j
# pilot_value = -7-7j
# pilot_value = 5-5j
pilot_value = 3+3j
# pilot_value = 1-1j

# Type of modulation. OFDM, OOK, etc.
modulation_config = {
                0: {"type": "OFDM",
                    "ofdm_type": DCO_OFDM_CONFIG,
                    "pilot_value": pilot_value,
                    "n_carriers": N_FFT, # number of IFFT stages
                    # "ofdm_symbol_time": 3e-6, # OFDM symbol time duration (in seconds)
                    "n_pilots": int(N_FFT*percentage_of_pilots),
                    "n_cp": N_FFT//4
                    },
                
                1: {"type": "OFDM",
                    "ofdm_type": ACO_OFDM_CONFIG,
                    "pilot_value": pilot_value,
                    "n_carriers": N_FFT, # number of IFFT stages
                    # "ofdm_symbol_time": 1e-6, # OFDM symbol time duration (in seconds)
                    "n_pilots": int(N_FFT*percentage_of_pilots),
                    "n_cp": N_FFT//4
                    },
                
                2: {"type": "OOK"
                    }
}
# Choose modulation type from the above.
modulation_index = 0
# modulation_index = 1
# modulation_index = 2

# Type of mapping. 4-QAM, 16-QAM, 64-QAM, 256-QAM
mapping_config = {
                0: ["QAM", 4],
                1: ["QAM", 16],
                2: ["QAM", 64],
                3: ["QAM", 256]
}

# Choose mapping type from the above.
mapping_index = 0
mapping_index = 1
# mapping_index = 2
# mapping_index = 3