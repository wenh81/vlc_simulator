import numpy as np
from matplotlib import pyplot as plt
from timeit import default_timer as timer
from scipy import interpolate
from scipy import signal
from scipy import fftpack
from collections import defaultdict
from bitstring  import BitArray
import re
from PIL import Image
from numba import njit, jit, vectorize
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
from tabulate import tabulate
import json
import random
import inspect
from beeprint import pp
import pyfftw
import reikna
import os
from commpy.modulation import QAMModem, PSKModem, ofdm_tx
from subprocess import Popen, PIPE

# from scipy.signal import correlate
# import pycuda.autoinit
# import pycuda.gpuarray as gpuarray
# ONLY FOR LINUX
# import skcuda.fft as cu_fft


# from . import Global as Global
from . import Global
# from .generalLibrary import *
from . import generalLibrary as lib
from .generalLibrary import timer_dec, sync_track
from .generalLibrary import printDebug, plotDebug


from .Message import Message
from .Mapping import Mapping
from .OFDM import OFDM
# # # from .OOK import OOK
from .Modulator import Modulator
from .DAC import DAC
from .ADC import ADC
from .Transmitter import Transmitter
from .Channel import Channel

from .Simulator import Simulator
from .Tanner import Tanner
from .Virtuoso import Virtuoso

from .Detector import Detector
from .ROIC import ROIC
from .BouncingPixel import BouncingPixel
# from .APS import APS

from .Receiver import Receiver
from .MeritFunctions import MeritFunctions


from .SimulationSync import SimulationSync

random.seed(Global.rand_seed)