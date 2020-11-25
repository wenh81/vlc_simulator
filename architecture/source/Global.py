import numpy as np

# Dict with all bypass flags
bypass_dict = {
                "Transmitter": False,
                "LightSource": True,
                "DAC": False,
                "DAC_rounding_or_simul": True,
                "Channel": True,
                "Detector": True,
                "ROIC": False,
                "ADC": False,
                "ADC_rounding_or_simul": True
            }

# list of channel responses for each lamp, when bypassig Channel.
list_of_channel_response = [0.1*np.array([1, 0, 0.3+0.3j])]

# rx_SNR (dB) is ued if not set, if not calculated.
rx_SNR_dB = 25

# Flag to indicate use of raytrace, or not, for the CIR estimation
use_raytrace = False

# TODO --- add timeunits to the program
timeunit = "ns"

# Contains list of dicts with all information needed to configure the lights on the Transmitter. Each position has a dict, with the type of light, the position for each lamp, and angle. Can be used to configure more than one array of lamps.
transmitter_config = [{"light_type": ["LED"], "position": [(0,0,0)], "angle": [(0,0)]}]

# Contains list of dicts with all information needed to configure the detectors on the receiver. Each position has a dict, with the type of detector, the position for each detector, and angle. Can be used to configure more than one array of detectors.
receiver_config = [{"detector_type": ["photodiode"], "position": [(0,0,0)], "angle": [(0,0)]}]

# Contains list of dicts with all information needed to configure the ROICs on the receiver. Each position has a dict, with the type of ROIC, associated with each corresponding detector. Can be used to configure more than one array of ROICs.
roic_config = [{"circuit_type": ["BouncingPixel"], "waves_name": ["vout"]}]

# List of all wavelengths to be considered during simulation, in nm.
wavelenghts = [550]

# Temperature in Kelvin.
temperature = 273

# Defines the simulator to be used, if appliable.
which_simulator = "Virtuoso"

# Flag to define if using circuit simulation.
circuit_simulation = False

# Input info structure
input_info = {"type": "str", "data": ["Primeiro", "Segundo"]}
input_info = {"type": "str", "data": ["Uma frase beeeem longaaaaaaaaaaa!"]}
# input_info = {"type": "image", "data": [r"../images/test.png"]}
# input_info = {"type": "image", "data": [r"../images/test.png", r"../images/test_larger.png"]}
# input_info = {"type": "image", "data": [r"../images/test_large_img.png"]}

# supported input_info types
supported_input_info = ["str", "image", "audio"]

# Type of modulation. OFDM, OOK, etc.
modulation_config = {
                0: {"type": "OFDM",
                    "ofdm_type": "ACO-OFDM",
                    "pilot_value": 3+3j,
                    "n_carriers": 32,
                    "n_pilots": 8,
                    "n_cp": 32//4
                    },
                1: {"type": "OOK"}
                }
# Choose modulation type from the above.
modulation_index = 0

# Type of mapping. 4-QAM, 8-QAM, 16-QAM, etc.
mapping_config = {
                0: ["QAM", 4],
                1: ["QAM", 8],
                2: ["QAM", 16],
                3: ["QAM", 64]
                }
# Choose mapping type from the above.
mapping_index = 0
