from .common_imports import *

class Simulator(object):

    def __init__(self, netlist, sync_obj):
        """Constructor for the Circuit Simulator."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        # Get debug and plot flags
        self.DEBUG, self.PLOT = lib.getDebugPlot("Simulator", self.sync_obj)
        
        self.sync_obj.appendToSimulationPath("Simulator")
        
        if self.DEBUG:
            print('Running Simulator...')
        
        # Timeout to abort simul, after that time is passed.
        self.simul_timeout = None

        # Netlist path of circuit to be simulated.
        self.netlist = netlist
    
        pass

    @sync_track
    def stop(self):
        """Abort simulation, by user command or timeout."""
        
        
        
        # Get abort from timeout or user command, for example
        abort = True
        
        raise ValueError(f"\n\n***Error --> stop not supported yet!\n")
        
        return abort
    
    @sync_track
    def getSimulTimeout(self):
        """Returns value of self.simul_timeout"""
        
        return self.simul_timeout

    @sync_track
    def setSimulTimeout(self, simul_timeout):
        """Set new value for self.simul_timeout"""
        
        self.simul_timeout = simul_timeout

    @sync_track
    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    @sync_track
    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj