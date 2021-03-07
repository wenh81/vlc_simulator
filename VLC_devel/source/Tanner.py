from generalLibrary import timer_dec, sync_track

from Simulator import Simulator

from generalLibrary import printDebug, plotDebug

from subprocess import Popen, PIPE

import os

class Tanner(Simulator):

    def __init__(self, netlist, tspice, sync_obj):
        """Constructor."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Tanner") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Tanner")
        
        if self.DEBUG:
            print('Running Tanner...')
        
        Simulator.__init__(self, netlist = netlist, sync_obj = sync_obj)
        
        # Netlist path of circuit to be simulated.
        self.netlist = netlist
        
        # tspice path
        self.tspice = tspice

        # Output simulation waves. Each key corresponds to a different wave.
        self.waves = None
    
        pass
    
    @sync_track
    def setup(self, currents):
        """Setup simulation, like loading netlist.""" 

        print("MUST SETUP THE INPUT CURRENTS FOR TANNER")
        
        # raise ValueError(f"\n\n***Error --> setup not supported yet!\n")
    

    @sync_track
    def start(self):
        """Fire simulation, and stops after it finishes (or timeout or abort). Populate 'waves' as the output."""
        
        print("\nThe Tanner simulation has started. Please wait....")
        process = Popen([f'{self.tspice}', f'{self.netlist}'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        # WHAT ABOUT IF ANY SIMUL ERROR HAPPENS???
        
        STOP
        
        raise ValueError(f"\n\n***Error --> start not supported yet!\n")
    

    @sync_track
    def getTspice(self):
        """Returns value of self.tspice"""
        
        return self.tspice

    @sync_track
    def setTspice(self, tspice):
        """Set new value for self.tspice"""
        
        self.tspice = tspice
        
    @sync_track
    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    @sync_track
    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist

    @sync_track
    def getWaves(self):
        """Returns value of self.waves"""
        
        return self.waves

    @sync_track
    def setWaves(self, waves):
        """Set new value for self.waves"""
        
        self.waves = waves

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj