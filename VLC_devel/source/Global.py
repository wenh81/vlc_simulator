import numpy as np

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
    "DAC": True,
    "DAC_rounding_or_simul": True,
    "Channel": True,
    "Detector": True,
    "ROIC": False, ## Read-Out Integrated Circuit
    # "ROIC": True, ## Read-Out Integrated Circuit
    "ADC": True,
    "ADC_rounding_or_simul": True
}

# TODO --- FIX ISSUE WITH << "DAC": False >>, where only
# abs of signal is passed through. Needs to apply hermitian symetry in this case!


# TODO --- MUST ADD OPTION TO USE H(0) or h(t)


# list of channel responses for each lamp, when bypassig Channel.
import numpy as np
# Unitary channel
list_of_channel_response = [1*np.array([1])]
list_of_channel_response = [1*np.array([np.random.uniform()+np.random.uniform()*1j, (np.random.uniform()+np.random.uniform()*1j)/2, (np.random.uniform()+np.random.uniform()*1j)/4])]
list_of_channel_response = [1*np.array([1, 0, 0.3+0.3j])]
from scipy import signal
CIR = signal.windows.hann(8)
CIR = signal.unit_impulse(30, 'mid')*3
b, a = signal.butter(4, 0.2)
CIR = signal.lfilter(b, a, CIR)

# list_of_channel_response = [ 1*DELTA(T-T0)]
# list_of_channel_response = [ G0*DELTA(T-T0) + g1*DELTA(T-T1)  ]

# CIR = signal.unit_impulse(10, 'mid')
# CIR = signal.unit_impulse(256, 2)
# import matplotlib.pyplot as plt
# plt.plot(t, y)
# CIR = signal.unit_impulse(10)
# CIR = GAIN*np.array([1])
print(CIR)
list_of_channel_response = [CIR]
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

# # Flag to define if using circuit simulation.
# circuit_simulation = False
# # circuit_simulation = True

# Contains list of dicts with all information needed to configure the ROICs on the receiver.
# Each position has a dict, with the type of ROIC, associated with each corresponding detector.
# Can be used to configure more than one array of ROICs.
# Also, set if will do circuit simulation or not.
# Use the simularion to extract the metrics such as DR, SNR, gain, input referred current noise (current_noise), etc.
# Then, use the metrics instead of the simulation
roic_config = [{
    "circuit_simulation": [False],
    "circuit_type": ["BouncingPixel"],
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
temperature = 273

############### CIRCUIT SIMULATOR ###############

simulator_config = {
    "Tanner": {
        "Windows": {
            "path": r"C:\IR2\bibliotecas\AMSC35_14.3"
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

# supported input_info types
supported_input_info = ["str", "image", "audio"]

# DCO_OFDM_CONFIG = {"DCO-OFDM": [0]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [0.5]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [1.5]}
DCO_OFDM_CONFIG = {"DCO-OFDM": [5]}
# DCO_OFDM_CONFIG = {"DCO-OFDM": [19]}

ACO_OFDM_CONFIG = {"ACO-OFDM": []}

# slack for hermitian imaginary part
hermitian_slack = 1e-6

# Number of FFT points
N_FFT = 32
N_FFT = 64
N_FFT = 128
N_FFT = 256
N_FFT = 512
# N_FFT = 1024

# percentage of pilots, depending on number of FFT carriers 
percentage_of_pilots = 0.3
percentage_of_pilots = 0.125
# percentage_of_pilots = 0.5

# pilot_value
# pilot_value = 15+15j
pilot_value = 7+7j
# pilot_value = -7-7j
# pilot_value = 5-5j
pilot_value = 3+3j
pilot_value = 1-1j

# Type of modulation. OFDM, OOK, etc.
modulation_config = {
                0: {"type": "OFDM",
                    "ofdm_type": DCO_OFDM_CONFIG,
                    "pilot_value": pilot_value,
                    "n_carriers": N_FFT, # number of IFFT stages
                    "n_pilots": int(N_FFT*percentage_of_pilots),
                    "n_cp": N_FFT//4
                    },
                
                1: {"type": "OFDM",
                    "ofdm_type": ACO_OFDM_CONFIG,
                    "pilot_value": pilot_value,
                    "n_carriers": N_FFT, # number of IFFT stages
                    "n_pilots": int(N_FFT*percentage_of_pilots),
                    "n_cp": N_FFT//4
                    },
                
                2: {"type": "OOK"
                    }
}
# Choose modulation type from the above.
modulation_index = 0
modulation_index = 1

# Type of mapping. 4-QAM, 16-QAM, 64-QAM, 256-QAM
mapping_config = {
                0: ["QAM", 4],
                1: ["QAM", 16],
                2: ["QAM", 64],
                3: ["QAM", 256]
}

# Choose mapping type from the above.
mapping_index = 0
# mapping_index = 1
# mapping_index = 2
# mapping_index = 3