from generalLibrary import timer_dec, sync_track

import Global

import numpy as np

from Virtuoso import Virtuoso

from Tanner import Tanner

from generalLibrary import printDebug, plotDebug

import generalLibrary as lib

class ROIC(object):
    
    def __init__(self, circuit_type, waves_name, transconductance_gain, circuit_simulation, DR, current_noise, SNR, roic_setup, sync_obj):
        """Constructor of ROIC. Base class of circuit handling"""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("ROIC") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("ROIC")
        
        if self.DEBUG:
            print('Running ROIC...')
        
        # Stores the circuit topology. Ex: APS, Bouncing Pixel, etc.
        self.circuit_type = circuit_type
        
        # Stores the list of wave names to be delivered
        self.waves_name = waves_name

        # Flag to indicate use of circuit simulation.
        self.circuit_simulation = circuit_simulation

        # Curve that translates how to convert from photocurrent to voltage.
        self.linearity_curve = {"photocurrent": [], "voltage": []}

        # Defines the simulator to be used, if appliable.
        self.which_simulator = Global.which_simulator
        
        # Get the all simulator configuration.
        self.simulator_config = Global.simulator_config

        # Stores the netlist of the circuit.
        self.netlist = None

        # Original Path to netlist of the circuit
        self.netlist_path = None
        
        # Path to netlist of the circuit to be simulated
        self.simul_netlist_path = None

        # Default value of transconductance gain (V/A) -- or the sensitivity
        # TODO : Change it to a GAIN curve (vs. current) instead?
        self.transconductance_gain = transconductance_gain
        
        # Dynamic range (in dB)
        self.DR = DR
        
        # input referred current noise (in A)
        self.current_noise = current_noise
        
        # Maximum SNR (in dB) --- TODO : Change it to a SNR curve (vs. current) instead?
        # TODO -- DO WE NEED SNR?? SINCE WE HAVE THE CURRENT NOISE AND GAIN
        self.SNR = SNR

        # Further ROIC setup (when needed)
        self.roic_setup = roic_setup

        # # input referred voltage noise
        # self.voltage_noise = self.current_noise * self.transconductance_gain

        # max_voltage_signal = self.voltage_noise * (10**(self.SNR/20))
        
        # i_sat = 256 / (60*1e3)
        # i_dark = 0
        # i_B = 400e-6

        # DR = 20*np.log10((i_sat - i_dark - i_B)/self.current_noise)
        # # printDebug(i_sat*1e3)
        # printDebug(DR)

        # self.current_noise = (i_sat - i_dark - i_B)/(10**(self.DR/20))
        # printDebug(self.current_noise*1e9)

        # printDebug(max_voltage_signal)
        

    @sync_track
    def convertsToWaves(self, current_wave):
        """Converts a given photocurrent list into associated waves (simulated or not). If flag to use circuit_simulation is active, then calls the Simulator"""
        
        if self.circuit_simulation:
            
            # Calls simulator to get voltage waves from currents
            voltage_wave = self.callSimulator(current_wave)
            
            raise ValueError(f"\n\n***Error --> ROIC simulation is not supported yet, at roic_config['circuit_simulation'] = True\n")
        
        else:
            
            # # If no simulator, converts currents to voltage using modelling
            # voltage = []

                
            # TODO -- Remove this after changing the gain to a curve. It might need to be interpolated...
            self.transconductance_gain = self.transconductance_gain*np.ones(len(current_wave))
            
            # TODO -- Adding non-linearuty to gain (JUST TO SEE THE EFFECT )
            # self.transconductance_gain = np.random.normal(self.transconductance_gain, self.transconductance_gain*0.1)
            # self.transconductance_gain = np.sqrt(self.transconductance_gain)
            # self.transconductance_gain = (np.sqrt(np.arange(0, len(self.transconductance_gain)))*5e-6 + 1)*self.transconductance_gain
            # self.transconductance_gain = (np.power(np.arange(0, len(self.transconductance_gain)), 2)*5e-6 + 1)*self.transconductance_gain
            
            # current_wave = current_wave * 5e-8
            # printDebug(current_wave, plot = True)
            
            if not Global.IM_DD:
                print(f"\n\n***Warning --> ROIC simulation, but using RF OFMD (Global.IM_DD off).\
                    \nApplied gain to each channel real and imaginary instead...")
                
                # Add noise to current_wave. Average = current_wave ; std = self.current_noise
                current_wave_real = np.random.normal(current_wave.real, self.current_noise)
                current_wave_imag = np.random.normal(current_wave.imag, self.current_noise)
                
                # Get from SNR the noise to be applied on the current wave.
                voltage_wave = self.transconductance_gain*current_wave_real + (1j)*self.transconductance_gain*current_wave_imag
                # voltage_wave = 1*current_wave_real + (1j)*1*current_wave_imag

            else:
                # Add noise to current_wave. Average = current_wave ; std = self.current_noise
                current_wave = np.random.normal(current_wave, self.current_noise)
            
                # clip current_wave at zero after noise application
                current_wave = lib.zeroClip(current_wave)
            
                # Get from SNR the noise to be applied on the current wave.
                voltage_wave = self.transconductance_gain*current_wave
                # voltage_wave = 1*current_wave
                
            # plotDebug(voltage_wave)
            # roic_waves.append(voltage_wave)

            # raise ValueError(f"\n\n***Error --> ROIC voltage_wave calculations while not bypassed, and circuit_simulation off, is not supported yet.\n")
                
        return voltage_wave
    
    @sync_track
    def callSimulator(self, current_wave):
        """Calls the desired circuit simulator, given the 'circuit_type', and arrat of currents to be simulated."""
        
        # raise ValueError(f"\n\n***Error --> ROIC simulation is not supported yet, at Global.which_simulator = True\n")
        
        # Needs to use 'self.circuit_type' an 'self.which_simulator'
        # Uses ssh to call simulator
        # self.simulator_config
        
        if self.which_simulator == "Virtuoso":
            
            # self.editNetlist()

            simulator = Virtuoso(
                netlist = "MY_NETLIST",
                sync_obj = self.sync_obj
            )

        elif self.which_simulator == "Tanner":
            
            # Edit netlist with correct setup values, like integration time, etc.
            self.editNetlist()
            
            simulator = Tanner(
                netlist = self.simul_netlist_path,
                tspice = self.simulator_config[self.which_simulator][Global.operating_system]['tspice'],
                sync_obj = self.sync_obj
            )
            
        else:
            raise ValueError(f"\n\n***Error --> Simulator < {self.which_simulator} > at Global.which_simulator is not supported!\n")
        
        # roic_out_list = []
        # for current in current_list:

        # Setup the simulator with desired inputs
        simulator.setup(currents = current_wave)
        
        
        # Start the simulator
        simulator.start()
        
        
        abort = False
        # Keep doing simulation while not aborted
        while not abort:
            
            # abort simulation
            abort = simulator.stop()
        
        
        waves_list = []
        # Get the desired waves, depending on the circuit
        for wave in self.waves_name:
            # append the waves list of interest
            waves_list.append(simulator.getWave(wave = wave))
        
        ### TODO --- GET THE VOLTAGE WAVE FROM WAVES LIST
        voltage_wave = waves_list
        
        return voltage_wave
    
    @sync_track
    def editNetlist(self):
        """Edit netlist to setup simulationt time, integration time, etc."""
        raise ValueError(f"\n\n***Error --> This method should be overriden by its parent, ex: Bouncing Pixel, APS, etc.\n")

    @sync_track
    def getCircuitType(self):
        """Returns value of self.circuit_type"""
        
        return self.circuit_type

    @sync_track
    def setCircuitType(self, circuit_type):
        """Set new value for self.circuit_type"""
        
        self.circuit_type = circuit_type

    @sync_track
    def getCircuitSimulation(self):
        """Returns value of self.circuit_simulation"""
        
        return self.circuit_simulation

    @sync_track
    def setCircuitSimulation(self, circuit_simulation):
        """Set new value for self.circuit_simulation"""
        
        self.circuit_simulation = circuit_simulation

    @sync_track
    def getLinearityCurve(self):
        """Returns value of self.linearity_curve"""
        
        return self.linearity_curve

    @sync_track
    def setLinearityCurve(self, linearity_curve):
        """Set new value for self.linearity_curve"""
        
        self.linearity_curve = linearity_curve

    @sync_track
    def getWhichSimulator(self):
        """Returns value of self.which_simulator"""
        
        return self.which_simulator

    @sync_track
    def setWhichSimulator(self, which_simulator):
        """Set new value for self.which_simulator"""
        
        self.which_simulator = which_simulator

    @sync_track
    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    @sync_track
    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist
    
    @sync_track
    def getTransconductanceGain(self):
        """Returns value of self.transconductance_gain"""
        
        return self.transconductance_gain

    @sync_track
    def setTransconductanceGain(self, transconductance_gain):
        """Set new value for self.transconductance_gain"""
        
        self.transconductance_gain = transconductance_gain
    
    @sync_track
    def getDR(self):
        """Returns value of self.DR"""
        
        return self.DR

    @sync_track
    def setDR(self, DR):
        """Set new value for self.DR"""
        
        self.DR = DR
    
    @sync_track
    def getSNR(self):
        """Returns value of self.SNR"""
        
        return self.SNR

    @sync_track
    def setSNR(self, SNR):
        """Set new value for self.SNR"""
        
        self.SNR = SNR
    
    @sync_track
    def getRoicSetup(self):
        """Returns value of self.roic_setup"""
        
        return self.roic_setup

    @sync_track
    def setRoicSetup(self, roic_setup):
        """Set new value for self.roic_setup"""
        
        self.roic_setup = roic_setup
    
    @sync_track
    def getCurrentNoise(self):
        """Returns value of self.current_noise"""
        
        return self.current_noise

    @sync_track
    def setCurrentNoise(self, current_noise):
        """Set new value for self.current_noise"""
        
        self.current_noise = current_noise

    @sync_track
    def getNetlistPath(self):
        """Returns value of self.netlist_path"""
        
        return self.netlist_path

    @sync_track
    def setNetlistPath(self, netlist_path):
        """Set new value for self.netlist_path"""
        
        self.netlist_path = netlist_path
    
    @sync_track
    def getSimulNetlistPath(self):
        """Returns value of self.simul_netlist_path"""
        
        return self.simul_netlist_path

    @sync_track
    def setSimulNetlistPath(self, simul_netlist_path):
        """Set new value for self.simul_netlist_path"""
        
        self.simul_netlist_path = simul_netlist_path

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj