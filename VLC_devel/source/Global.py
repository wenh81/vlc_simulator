import numpy as np

# global debug flag
DEBUG = {
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
    "MeritFunctions": True,
    "SimulationSync": True
}

# global plot flag
PLOT = {
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
    "ROIC": True,
    "ADC": True,
    "ADC_rounding_or_simul": True
}

# TODO --- FIX ISSUE WITH << "DAC": False >>, where only
# abs of signal is passed through. Needs to apply hermitian symetry in this case!

# list of channel responses for each lamp, when bypassig Channel.
list_of_channel_response = [1*np.array([1, 0, 0.3+0.3j])]
# list_of_channel_response = [0.1*np.array([1, 0, 0.3+0.3j])]

# rx_SNR (dB) is ued if not set, if not calculated.
rx_SNR_dB = 30
# rx_SNR_dB = 25
# rx_SNR_dB = 10

# TODO --- add timeunits to the program
timeunit = "ns"

# Contains list of dicts with all information needed to configure the lights on the Transmitter. Each position has a dict, with the type of light, the position for each lamp, and angle. Can be used to configure more than one array of lamps.
transmitter_config = [{"light_type": ["LED"], "position": [(0,0,0)], "angle": [(0,0)], "database": ["path_to_database"]}]

# Contains list of dicts with all information needed to configure the detectors on the receiver. Each position has a dict, with the type of detector, the position for each detector, and angle. Can be used to configure more than one array of detectors.
receiver_config = [{"detector_type": ["photodiode"], "position": [(0,0,0)], "angle": [(0,0)], "database": ["path_to_database"]}]

# Contains list of dicts with all information needed to configure the ROICs on the receiver. Each position has a dict, with the type of ROIC, associated with each corresponding detector. Can be used to configure more than one array of ROICs.
roic_config = [{"circuit_type": ["BouncingPixel"], "waves_name": ["vout"]}]

# List of all wavelengths to be considered during simulation, in nm.
wavelenghts = [550]

# Temperature in Kelvin.
temperature = 273

# Defines the simulator to be used, if appliable.
which_simulator = "Virtuoso"


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

# Flag to define if using circuit simulation.
circuit_simulation = False

# Enable multi_theading or not pos [0] and number of threads pos [1]
multi_theading = [True, 4]
multi_theading = [True, 40]
multi_theading = [False, None]

################################### > FLAGS < ###################################

# Input info structure
input_info = {"type": "str", "data": ["Primeiro", "Segundo"]}
input_info = {"type": "str", "data": ["mini msg!"]}
input_info = {"type": "str", "data": ["mensagem media...!"]}
input_info = {"type": "str", "data": ["Uma frase beeeem longaaaaaaaaaaa!"]}
input_info = {"type": "str", "data": ["A vida eh curta, por isso viva a vida bem vivida!"]}
# input_info = {"type": "image", "data": [r"../images/test.png"], "n_bytes": [3]}
input_info = {"type": "image", "data": [r"../images/test_larger.png"], "n_bytes": [3]}
# input_info = {"type": "image", "data": [r"../images/zebra.png"], "n_bytes": [3]}
# input_info = {"type": "image", "data": [r"../images/zebra_large.png"], "n_bytes": [3]}

# supported input_info types
supported_input_info = ["str", "image", "audio"]

# Type of modulation. OFDM, OOK, etc.
modulation_config = {
                0: {"type": "OFDM",
                    "ofdm_type": "ACO-OFDM",
                    "pilot_value": 3+3j,
                    "n_carriers": 512,
                    "n_pilots": int(512*0.125),
                    "n_cp": 512//4
                    },
                
                1: {"type": "OOK"
                    }
}
# Choose modulation type from the above.
modulation_index = 0

# Type of mapping. 4-QAM, 8-QAM, 16-QAM, etc.
mapping_config = {
                0: ["QAM", 4],
                1: ["QAM", 8],
                2: ["QAM", 16],
                3: ["QAM", 64],
                4: ["QAM", 128],
                5: ["QAM", 256]
}

# Choose mapping type from the above.
mapping_index = 3