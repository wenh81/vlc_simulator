from .common_imports import *


# global debug flag
DEBUG = {
    "all": False,
    "None": False,
    "None": True,
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
    "None": False,
    # "None": True,
    "VLC": False,
    # "VLC": True,
    "Message": False,
    "Transmitter": False,
    "Mapping": False,
    "Modulator": False,
    # "Modulator": True,
    "OFDM": False,
    # "OFDM": True,
    "DAC": False,
    "Channel": False,
    # "Channel": True,
    "LightSource": False,
    "Receiver": False,
    # "Receiver": True,
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
    "ROIC": False, ## Read-Out Integrated Circuit ON
    # "ROIC": True, ## NO ROIC
    # "ADC": True,
    "ADC": False,
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
# time_frame = 170e-9
# time_frame = 0.3e-6
# time_frame = 2e-6
# time_frame = 50e-9

# time step in seconds for simulation
time_step = 0.01e-9
time_step = 0.1e-9
time_step = 1e-9
# time_step = 7.246e-9 # so no interpolation is needed...
# time_step = 10e-9
# time_step = 0.5e-9
# time_step = 10e-9

# operating frequency is inverse of time frame (???? at least for OFDM, I guess...)
# calculated on the modulator ???
# sample_frequency = None
# sample_frequency = 1/time_step
simul_frequency = 1/time_step


# Circuit PCB voltage (VDD)
VDD_tx = 3.3
VSS_tx = 0
VDD_rx = 3.3
VSS_rx = 0
tx_voltage_bias_add = 0 ## For IM/DD, it's the bias applied on the LED on TX.
# tx_voltage_bias_add = 2 ## For IM/DD, it's the bias applied on the LED on TX.
# rx_voltage_bias_subtract = 1.5 ## For IM/DD, it's the bias applied on the LED on RX.
# tx_voltage_bias_add = 0 ## For IM/DD, it's the bias applied on the LED on TX.
rx_voltage_bias_subtract = 0 ## For IM/DD, it's the bias applied on the LED on RX.
# rx_voltage_bias_subtract = 0.4 ## For IM/DD, it's the bias applied on the LED on RX.

# Added background radiation power (in W)
background_power = 0
# background_power = 3


# Total voltage bias for DCO-OFDM (ignore tx bias)
# DCO_BIAS = 0.5
DCO_BIAS = 1.5
# DCO_BIAS = 0
# DCO_BIAS = 2
# DCO_BIAS -= tx_voltage_bias_add

# ADC references
adc_configuration = {"vref_plus": VDD_rx, "vref_minus": VSS_rx, "n_bits": 8}
# adc_configuration = {"vref_plus": VDD_rx, "vref_minus": VSS_rx, "n_bits": 12}

# type of interpolation
interpolation_type = 'linear'
interpolation_type = 'cubic'
# interpolation_type = 'nearest'
# interpolation_type = 'next'
interpolation_type = 'previous' ### correct ?
# interpolation_type = 'quadratic'
# interpolation_type = 'slinear'

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
group_delay = 0
group_delay = 10e-9
group_delay = 40e-9
group_delay = 113e-9
group_delay = 200e-9
# group_delay = 400e-9
# group_delay = 500e-9
# group_delay = 520e-9
# group_delay = 0e-9
# group_delay = 0
dist = [1, 1.2, 1.4, 1.9, 2.3, 5, 20]
dist = [1, 1.2, 1.4, 1.9, 2.3]
# dist = [1, 1.2, 1.1]
# dist = [1, 1.1]
# dist = [1, 1.01]
# dist = [2, 2.1]
dist = [1, 2]
dist = [1]
# group_delay = 0
dist = list(np.array(dist))
response = [(attenuation/(d**2), group_delay+d/c_speed) for d in dist]

response = [(attenuation/(d**2), d*group_delay) for d in dist]
# response = [(attenuation/(d**2), group_delay+d/c_speed) for d in dist]
# response = [(1, 200e-9), (1, 500e-9)]
# response = [(0.5, 200e-9), (0.5, 1900e-9), (0.5, 1000e-9)]
# response = [(1, 50e-9)]
# response = [(1, 20e-9)]
# response = [(1, 10e-9)]
# response = [(1, 5e-9)]
# response = [(1, 200e-9)]
# group_delay = 50e-9
# group_delay = 200e-9
# group_delay = 0
# response = [(1, group_delay)]
# variable used for synchronization
# TODO --- if None, returns full signal after convolution, 
# to be used for further correlation, to find group_delay
# TODO --- otherwise, use it to shift signal in time
# group_delay = None
# group_delay = 0
# group_delay = 50e-9

# print(response)
# print(dist)

# test CIRsS
CIR = {
    0: {"impulse": [(1, 1e-9)]},
    1: {"impulse": [(1, 250e-9), (1, 500e-9)]},
    2: {"impulse": [(1, 2e-9), (0.7, 3e-9)]},
    3: {"butter": response},
    4: {"impulse": response},
    9: {"others": []}
}

# test list to be used
list_of_channel_response = [CIR[4]]
list_of_channel_response = [CIR[3]]


# list_of_channel_response = [CIR[0], CIR[1]]
# plotDebug(CIR, symbols='r-o')
# list_of_channel_response = [0.1*np.array([1, 0, 0.3+0.3j])]

# rx_SNR (dB) is ued if not set, if not calculated. Can use <None> to ignore noise
rx_SNR_dB = 50
rx_SNR_dB = 30
# rx_SNR_dB = 25
# rx_SNR_dB = 20
# rx_SNR_dB = 10
rx_SNR_dB = None

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
roic_config = {
    "circuit_simulation": [False], ## ROIC simulation OFF
    # "circuit_simulation": [True], ## ROIC simulation ON
    "circuit_type": ["BouncingPixel"],
    # "roic_setup": [{"vmin": "500m", "vmax": "2.5", "stepTran": "1000"}],
    # "roic_setup": [{"vmin": "500m", "vmax": "2.5", "stepTran": "10000"}],
    # "roic_setup": [{"vmin": "700m", "vmax": "2", "stepTran": "500"}],
    # "roic_setup": [{"vmin": "500m", "vmax": "2.5", "stepTran": "100"}],
    "roic_setup": [{"vmin": "400e-3", "vmax": "2.6", "stepTran": "100"}],
    "gain": [60*1e3],
    # "gain": [1],
    "DR": [130],
    "current_noise": [1e-9],
    "SNR": [144],
    "waves_name": ["vout"]
    }

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
payload_data = {"type": ["str", "str"], "data": ["Primeiro", "Segundo"]}
payload_data = {"type": ["str", "str"], "data": ["Hello, Motto!", "Uma frase beeeem longaaaaaaaaaaa!"]}
# payload_data = {"type": ["text"], "data": [r"../data/test.txt"]}
payload_data = {"type": ["str"], "data": ["mini msg!"]}
# payload_data = {"type": ["str"], "data": ["mensagem media...!"]}
payload_data = {"type": ["str"], "data": ["Uma frase beeeem longaaaaaaaaaaa!"]}
# payload_data = {"type": ["str"], "data": ["A vida eh curta, por isso viva a vida bem vivida!"]}
# payload_data = {"type": ["image"], "data": [r"../data/test.png"], "n_bytes": [3]}
# payload_data = {"type": ["image"]*2, "data": [r"../data/test.png", r"../data/test_larger.png"], "n_bytes": [3]*2}
# payload_data = {"type": ["image", "str"], "data": [r"../data/test.png", "Uma frase beeeem longaaaaaaaaaaa!"], "n_bytes": [3]*2}
# payload_data = {"type": ["image"], "data": [r"../data/test_larger.png"], "n_bytes": [3]}
# payload_data = {"type": ["image"], "data": [r"../data/zebra.png"], "n_bytes": [3]}
# payload_data = {"type": ["image"], "data": [r"../data/zebra_large.png"], "n_bytes": [3]}
# payload_data = {"type": ["bin"], "data": ["10"]}
import random
# payload_data = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 32)])]}
# payload_data = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 2**3)])]}
# payload_data = {"type": ["bin"], "data": ["0110011001100110"]}
# payload_data = {"type": ["bin"], "data": ["0000000000000000000000000000000011111111111111111111111111111111"]}
# payload_data = {"type": ["bin"], "data": ["1111111111111111111111111111111100000000000000000000000000000000"]}
# payload_data = {"type": ["bin"], "data": ["11111111111111111111111111111111"]}
payload_data = {"type": ["bin"], "data": ["0100010100111011000110110011100111110101110100010100001000100011"]}
payload_data = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 256)])]}
# payload_data = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 64)])]}
# payload_data = {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 128)])]}
# 256-bit
# payload_data = {"type": ["bin"], "data": ["0110000011100001011100010000000110101010110000100011110110001001100001110011000001111100110000101100001011110100100011010010000110001110000010000101101100101011101110010011011011111011100101111010000010001110100111010010000010100101110011111111111011010011"]}
# payload_data = {"type": ["bin"], "data": ["00011100001110011000001111100110000101100001011110100100011010010000110001110000010000101101100101011101110010011011011111011100101111010000010001110100111010010000010100101110011111111111011010011"]}

# supported input_info types
supported_input_info = ["str", "image", "audio"]

# printDebug([''.join([str(random.randint(0, 1)) for j in range(0, 15)])])

# # Intensity Modulation / Direct Detection (IM_DD) -- always on for VLC/LiFi [flag kept only for completion]
# IM_DD = True
# IM_DD = False


# DCO_OFDM_CONFIG = {"DCO-OFDM": [0]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [0.5]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [1.5]}
DCO_OFDM_CONFIG = {"DCO-OFDM": [5]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [19]}

ACO_OFDM_CONFIG = {"ACO-OFDM": []}

# slack to consider a value close enough to zero
# Used for hermitian imaginary part (check that imaginary part
#  is [img <= slack]. instead of [img == 0])
# hermitian_slack = 1e-6
zero_slack = 1e-10

# Number of FFT points
# N_FFT = 16
N_FFT = 32
N_FFT = 64
N_FFT = 128
N_FFT = 48
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
                10: {"type": "OFDM",
                    "ofdm_type": DCO_OFDM_CONFIG,
                    "n_fft": N_FFT, # number of IFFT stages
                    # "ofdm_symbol_time": 3e-6, # OFDM symbol time duration (in seconds)
                    # "n_pilots": int(N_FFT*percentage_of_pilots),
                    "IM_DD": True, # Intensity Modulation / Direct Detection (IM_DD) -- always on for VLC/LiFi [false is used for testing on RF OFDM]
                    "n_cp": 4
                    },
                
                11: {"type": "OFDM",
                    "ofdm_type": ACO_OFDM_CONFIG,
                    "n_fft": N_FFT, # number of IFFT stages
                    # "ofdm_symbol_time": 1e-6, # OFDM symbol time duration (in seconds)
                    # "n_pilots": int(N_FFT*percentage_of_pilots),
                    "IM_DD": True,
                    "n_cp": 4
                    },
                
                # 2: {"type": "OFDM",
                #     "ofdm_type": {"ACO-OFDM": []},
                #     "n_fft": 16, # 32-bit data, with 2 bit symbol = 16 data FFT (all are 'pilots')
                #     "pilots": [], ## no pilots here, b/c all will be used for channel estimation
                #     "IM_DD": True,
                #     "n_cp": 4
                #     },

                13: {"type": "OFDM",
                    "ofdm_type": {"ACO-OFDM": []},
                    "n_fft": 52, # number of IFFT stages
                    # "n_pilots": 15,
                    "pilots": [5, 19],
                    "IM_DD": True,
                    "n_cp": 4
                    },
                
                15: {"type": "OFDM",
                    "ofdm_type": {"DCO-OFDM": [5]},
                    "n_fft": 52, # number of IFFT stages
                    # "n_pilots": 15,
                    "pilots": [5, 19],
                    "IM_DD": True,
                    "n_cp": 4
                    },
                
                "ACO-OFDM-FLP": {
                    "type": "OFDM",
                    "ofdm_type": {"ACO-OFDM": []},
                    "n_fft": 16, # 64-bit data, with 1 bit symbol = 4x16 data FFT (all are 'pilots')
                    "pilots": [], ## no pilots here, b/c all will be used for channel estimation
                    "IM_DD": True,
                    "n_cp": 10
                    },
                
                "ACO-OFDM-TDP": {
                    "type": "OFDM",
                    "ofdm_type": {"ACO-OFDM": []},
                    # "n_fft": 16, # 15-bit data with 1 bit symbol -> 15 data FFT  + 1 pilot
                    # "pilots": [1, 5],
                    # "n_fft": 52,
                    # "pilots": [5, 19], 
                    "n_fft": 64,
                    "pilots": [5, 19], #### this values just works for ACO
                    "IM_DD": True,
                    "n_cp": 4
                    },
                
                "ACO-OFDM-ZEROS": {
                    "type": "OFDM",
                    "ofdm_type": {"ACO-OFDM": []},
                    # "n_fft": 52*2, # number of IFFT stages
                    "n_fft": 64*2, # number of IFFT stages #### this values just works for ACO
                    "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": True,
                    "n_cp": 10
                    },
                
                "ACO-OFDM-DATA": {
                    "type": "OFDM",
                    "ofdm_type": {"ACO-OFDM": []},
                    # "n_fft": 52, # number of IFFT stages
                    # "pilots": [5, 19], 
                    # "pilots": [1, 9, 15, 23], 
                    "n_fft": 52*2, # number of IFFT stages
                    "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": True,
                    "n_cp": 10
                    },

                "ACO-OFDM-DATA2": {
                    "type": "OFDM",
                    "ofdm_type": {"ACO-OFDM": []},
                    # "n_fft": 52, # number of IFFT stages
                    # "pilots": [5, 19], 
                    # "pilots": [1, 9, 15, 23], 
                    # "n_fft": 52*2, # number of IFFT stages
                    # "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "n_fft": 128, # number of IFFT stages
                    "pilots": [5, 19, 33, 47, 59], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": True,
                    "n_cp": 10
                    },

                "DCO-OFDM-FLP": {
                    "type": "OFDM",
                    "ofdm_type": {"DCO-OFDM": [DCO_BIAS]},
                    "n_fft": 16, # 64-bit data, with 1 bit symbol = 4x16 data FFT (all are 'pilots')
                    "pilots": [], ## no pilots here, b/c all will be used for channel estimation
                    "IM_DD": True,
                    "n_cp": 10
                    },
                
                "DCO-OFDM-TDP": {
                    "type": "OFDM",
                    "ofdm_type": {"DCO-OFDM": [DCO_BIAS]},
                    # "n_fft": 16, # 15-bit data with 1 bit symbol -> 15 data FFT  + 1 pilot
                    # "pilots": [1, 6],
                    # "n_fft": 52,
                    # "pilots": [5, 19], 
                    "n_fft": 64,
                    "pilots": [5, 15, 19], #### this values just works for DCO
                    "IM_DD": True,
                    "n_cp": 4
                    },
                
                "DCO-OFDM-ZEROS": {
                    "type": "OFDM",
                    "ofdm_type": {"DCO-OFDM": [DCO_BIAS]},
                    # "n_fft": 52*2, # number of IFFT stages
                    # "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    # "n_fft": 64*2, # number of IFFT stages
                    # "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "n_fft": 48, # number of IFFT stages
                    "pilots": [5, 19], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": True,
                    "n_cp": 4
                    },

                "DCO-OFDM-DATA": {
                    "type": "OFDM",
                    "ofdm_type": {"DCO-OFDM": [DCO_BIAS]},
                    # "n_fft": 52, # number of IFFT stages
                    # "pilots": [5, 19], 
                    # "pilots": [1, 9, 15, 23], 
                    "n_fft": 52*2, # number of IFFT stages
                    "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": True,
                    "n_cp": 10
                    },

                "DCO-OFDM-DATA2": {
                    "type": "OFDM",
                    "ofdm_type": {"DCO-OFDM": [DCO_BIAS]},
                    # "n_fft": 52, # number of IFFT stages
                    # "pilots": [5, 19], 
                    # "pilots": [1, 9, 15, 23], 
                    "n_fft": 52*2, # number of IFFT stages
                    "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    # "n_fft": 128, # number of IFFT stages
                    # "pilots": [5, 19, 33, 47, 59], ## equivalent to [-21, -7, +7, +21]
                    # "n_fft": 64, # number of IFFT stages
                    # "pilots": [1, 9, 15, 23], 
                    "IM_DD": True,
                    "n_cp": 10
                    },

                "RF-OFDM-FLP": {
                    "type": "OFDM",
                    "ofdm_type": {"RF-OFDM": ""},
                    "n_fft": 16, # 64-bit data, with 1 bit symbol = 4x16 data FFT (all are 'pilots')
                    "pilots": [], ## no pilots here, b/c all will be used for channel estimation
                    "IM_DD": False,
                    "n_cp": 10
                    },
                
                "RF-OFDM-TDP": {
                    "type": "OFDM",
                    "ofdm_type": {"RF-OFDM": ""},
                    # "n_fft": 32, # 16-bit data with 1 bit symbol -> 15 data FFT  + 1 pilot (twice)
                    "n_fft": 52, # 16-bit data with 1 bit symbol -> 15 data FFT  + 1 pilot (twice)
                    # "pilots": [7, 23], ## [-8, +8]
                    # "pilots": [3, 7, 13, 17, 23, 28], ## [-8, +8]
                    "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": False,
                    "n_cp": 10
                    },
                "RF-OFDM-ZEROS": {
                    "type": "OFDM",
                    "ofdm_type": {"RF-OFDM": ""},
                    "n_fft": 52, # number of IFFT stages
                    "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": False,
                    "n_cp": 10
                    },

                "RF-OFDM-DATA2": {
                    "type": "OFDM",
                    "ofdm_type": {"RF-OFDM": "802.11a OFDM"},
                    # "n_fft": 52, # number of IFFT stages
                    # "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "n_fft": 128, # number of IFFT stages
                    "pilots": [5, 19, 33, 47, 128-47, 128-19, 128-33, 128-5], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": False,
                    "n_cp": 10
                    },
                
                "RF-OFDM-DATA": {
                    "type": "OFDM",
                    "ofdm_type": {"RF-OFDM": "802.11a OFDM"},
                    "n_fft": 52, # number of IFFT stages
                    "pilots": [5, 19, 33, 47], ## equivalent to [-21, -7, +7, +21]
                    "IM_DD": False,
                    "n_cp": 10
                    },
                
                14: {"type": "OOK"
                    }
}
# # Choose modulation type from the above.
# modulation_index = 0
# modulation_index = 1
# modulation_index = 2
# # modulation_index = 3

# Type of mapping. 4-QAM, 16-QAM, 64-QAM, 256-QAM
mapping_config = {
                '4-QAM': ["QAM", 4],
                '16-QAM': ["QAM", 16],
                '64-QAM': ["QAM", 64],
                '256-QAM': ["QAM", 256],
                'BPSK': ["PSK", 2],
                '4-PSK': ["PSK", 4],
                '16-PSK': ["PSK", 16]
}

# # Choose mapping type from the above.
# mapping_index = 0
# mapping_index = 1
# # mapping_index = 2
# # mapping_index = 3

# name for the output log file with results
log_results = "log_results.log"


USED_OFDM_TYPE = "RF"
USED_OFDM_TYPE = "DCO"
USED_OFDM_TYPE = "ACO"

###############
## TODO -- Convert the TX/RX info decode into a 'burst' config, as below
# Setups the burst.
# Sequence tells what are the keys to be executed, and in what order.
# Ex: 'preamble' setups 2 steps, 'short' and 'long', in that order
# each will run a sumbol tx with its own characteristics.
burst_config = {
                'fields': ['SHR', '__PAYLOAD__'],
                # 'fields': ['SHR'] + ['__PAYLOAD__']*4,
                'fields': ['SHR', '_ZEROS_', '__PAYLOAD__', '_ZEROS_'],
                # 'fields': ['SHR'],
                'SHR': { ## Synchronization Header
                    'subfields': ['FLP'],
                    # 'subfields': ['FLP', 'TDP', 'TDP', 'TDP', 'TDP', 'TDP', 'TDP'],
                    # 'subfields': ['FLP', 'TDP'],
                    'subfields': ['FLP', 'TDP', 'TDP'],
                    # 'subfields': ['FLP'] + ['TDP']*2,
                    'FLP': { ## Fast-locking Pattern
                        'sync': True, ## sets this pattern as a sync pattern to get the phase delay. This WON'T be converted into actual data.
                        'duration': 1e-6,
                        # 'sample_frequency_ratio': 10,
                        # 'sample_frequency_ratio': 10,
                        'sample_frequency_ratio': 2,
                        'sample_frequency_ratio': 5,
                        'mapping_index': 'BPSK',
                        'pilots_mapping_index': 'BPSK',
                        # 'modulation_index': "ACO-OFDM-FLP",
                        # 'modulation_index': "DCO-OFDM-FLP",
                        # 'modulation_index': "RF-OFDM-FLP",
                        'modulation_index': f"{USED_OFDM_TYPE}-OFDM-FLP",
                        # 'data': {"type": ["bin"], "data": ["101010101010101010101010101010"]}, # Base pattern, used for sync: 32-bit
                        # 'data': {"type": ["bin"], "data": ["10101010101010101010101010101010"]}, # Base pattern, used for sync: 32-bit
                        # 'data': {"type": ["bin"], "data": ["01010101010101010101010101010101"]}, # Base pattern, used for sync: 32-bit
                        # 'data': {"type": ["bin"], "data": ["10101010101010101010101010101010"]}, # Base pattern, used for sync: 16-bit
                        'data': {"type": ["bin"], "data": [''.join(['10']*32)] }, # Base pattern, used for sync: 64-bit
                        # 'data': {"type": ["bin"], "data": [''.join(['10']*64)] }, # Base pattern, used for sync: 64-bit
                        'method_tx': "FLPEncode@OFDM",
                        'method_rx': "FLPDecode@OFDM",
                        'args_rx': "arg0,arg1"
                    },
                    'TDP': { ## Topology Dependent Pattern
                        'duration': 1e-6,
                        'sample_frequency_ratio': 2,
                        'mapping_index': 'BPSK',
                        'pilots_mapping_index': 'BPSK',
                        # 'pilots_mapping_index': '4-QAM',
                        # 'modulation_index': "ACO-OFDM-TDP", # with 15-bit, use one bit as pilots, and BPSK
                        # 'modulation_index': "DCO-OFDM-TDP", # with 15-bit, use one bit as pilots, and BPSK
                        # 'modulation_index': "RF-OFDM-TDP", # with 15-bit, use one bit as pilots, and BPSK
                        'modulation_index': f"{USED_OFDM_TYPE}-OFDM-TDP",
                        # 'data': {"type": ["bin"], "data": ['101011101111010010100010000101'] }, # 15-bit pattern: identifies the network topology: only visibility, peer-to-peer, star, and broadcast
                        'data': {"type": ["bin"], "data": ['1010111011110100101000100001010'] }, # 16-bit pattern: identifies the network topology: only visibility, peer-to-peer, star, and broadcast
                    }
                },
                '_ZEROS_': {
                    'subfields': ['ZEROS'],
                    'ZEROS': { ## Onle zeros
                        'duration': 1e-6,
                        'sample_frequency_ratio': 2,
                        'mapping_index': 'BPSK',
                        'pilots_mapping_index': 'BPSK',
                        # 'modulation_index': "RF-OFDM-ZEROS",
                        'modulation_index': f"{USED_OFDM_TYPE}-OFDM-ZEROS",
                        'data': {"type": ["bin"], "data": [''.join(['0']*64)] },
                    }
                },
                '__PAYLOAD__': {
                    'subfields': ['__DATA__'],
                    '__DATA__': {
                        'duration': 1e-6,
                        'sample_frequency_ratio': 2,
                        # 'sample_frequency_ratio': 4,
                        'mapping_index': '4-QAM',
                        # 'mapping_index': 'BPSK',
                        'pilots_mapping_index': 'BPSK',
                        # 'pilots_mapping_index': '4-QAM',
                        # 'modulation_index': "ACO-OFDM-DATA",
                        # 'modulation_index': "DCO-OFDM-DATA",
                        # 'modulation_index': "RF-OFDM-DATA",
                        'modulation_index': f"{USED_OFDM_TYPE}-OFDM-DATA",
                        'modulation_index': f"{USED_OFDM_TYPE}-OFDM-DATA2",
                        # 'data': {"type": ["bin"], "data": ['10101110111101001010001000010101'] }
                        # 'data': {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 64)])]}
                        # 'data': {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 256)])]}
                        # 'data': {"type": ["bin"], "data": [''.join([str(random.randint(0, 1)) for j in range(0, 32)])]}
                        
                        'data': {"type": ["bin"], "data": ["0110000011100001011100010000000110101010110000100011110110001001100001110011000001111100110000101100001011110100100011010010000110001110000010000101101100101011101110010011011011111011100101111010000010001110100111010010000010100101110011111111111011010011"]}
                        # 'data': payload_data
                    },
                }
}
