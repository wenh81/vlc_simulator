from generalLibrary import timer_dec, sync_track

import Global

import numpy as np

from Virtuoso import Virtuoso

from Tanner import Tanner

from generalLibrary import printDebug, plotDebug

import generalLibrary as lib

class ROIC(object):
    
    def __init__(self, circuit_type, waves_name, transconductance_gain, circuit_simulation, sync_obj):
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

        # Stores the netlist of the circuit.
        self.netlist = None

        # Path to netlist of the circuit.
        self.netlist_path = None

        # Default value of transconductance gain (V/A) -- or the sensitivity
        # TODO : Change it to a GAIN curve (vs. current) instead?
        self.transconductance_gain = transconductance_gain
        
        # Dynamic range (in dB)
        self.DR = 130
        
        # input referred current noise (in A)
        self.current_noise = 1e-9
        
        # Maximum SNR (in dB) --- TODO : Change it to a SNR curve (vs. current) instead?
        # TODO -- DO WE NEED SNR?? SINCE WE HAVE THE CURRENT NOISE AND GAIN
        self.SNR = 144

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
    def convertsToWaves(self, current_list):
        """Converts a given photocurrent list into associated waves (simulated or not). If flag to use circuit_simulation is active, then calls the Simulator"""
        
        if self.circuit_simulation:
            
            # Calls simulator to get voltage waves from currents
            roic_waves_list = self.callSimulator(current_list)
            
            raise ValueError(f"\n\n***Error --> ROIC simulation is not supported yet, at Global.which_simulator = True\n")
        
        else:
            
            # If no simulator, converts currents to voltage using modelling
            roic_waves_list = []
            for current_wave in current_list:
                
                # TODO -- Remove this after changing the gain to a curve. It might need to be interpolated...
                self.transconductance_gain = self.transconductance_gain*np.ones(len(current_wave))
                
                # TODO -- Adding non-linearuty to gain (JUST TO SEE THE EFFECT )
                # self.transconductance_gain = np.random.normal(self.transconductance_gain, self.transconductance_gain*0.1)
                # self.transconductance_gain = np.sqrt(self.transconductance_gain)
                # self.transconductance_gain = (np.sqrt(np.arange(0, len(self.transconductance_gain)))*1e-5 + 1)*self.transconductance_gain
                self.transconductance_gain = (np.power(np.arange(0, len(self.transconductance_gain)), 2)*1e-5 + 1)*self.transconductance_gain
                
                # current_wave = current_wave * 5e-8
                # printDebug(current_wave, plot = True)
                
                # Add noise to current_wave. Average = current_wave ; std = self.current_noise
                current_wave = np.random.normal(current_wave, self.current_noise)
                
                # clip current_wave at zero after noise application
                current_wave = lib.zeroClip(current_wave)
                # plotDebug(current_wave)
                
                # Get from SNR the noise to be applied on the current wave.
                voltage = self.transconductance_gain*current_wave
                # voltage = 1*current_wave
                
                # printDebug(voltage, plot = True)
                
                roic_waves_list.append(voltage)
            
            # raise ValueError(f"\n\n***Error --> ROIC voltage calculations while not bypassed, and circuit_simulation off, is not supported yet.\n")
                
        return roic_waves_list
        
        
    @sync_track
    def callSimulator(self, current_list):
        """Calls the desired circuit simulator, given the 'circuit_type', and arrat of currents to be simulated."""
        
        raise ValueError(f"\n\n***Error --> ROIC simulation is not supported yet, at Global.which_simulator = True\n")
        
        # Needs to use 'self.circuit_type' an 'self.which_simulator'
        # Uses ssh to call simulator
        
        if self.which_simulator == "Virtuoso":
            
            simulator = Virtuoso(
                netlist = "MY_NETLIST",
                sync_obj = self.sync_obj
            )

        elif self.which_simulator == "Tanner":
            
            simulator = Tanner(
                netlist = "MY_NETLIST",
                sync_obj = self.sync_obj
            )
            
        else:
            raise ValueError(f"\n\n***Error --> Simulator < {self.which_simulator} > at Global.which_simulator is not supported!\n")
        
        roic_out_list = []
        for current in current_list:
            
            
            # Setup the simulator
            simulator.setup(currents = current)
            
            
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
            
            # Append list of waves to the roic list output
            roic_out_list.append(waves_list)
        
        return roic_out_list
        
        
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
    def getNetlistPath(self):
        """Returns value of self.netlist_path"""
        
        return self.netlist_path

    @sync_track
    def setNetlistPath(self, netlist_path):
        """Set new value for self.netlist_path"""
        
        self.netlist_path = netlist_path

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj