from generalLibrary import timer_dec, sync_track

from Simulator import Simulator

class Virtuoso(Simulator):
    
    def __init__(self, netlist, sync_obj):
        """Constructor."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("Virtuoso") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("Virtuoso")
        
        if self.DEBUG:
            print('Running Virtuoso...')
        
        
        Simulator.__init__(self, netlist = netlist, sync_obj = sync_obj)
        
        # Netlist path of circuit to be simulated.
        self.netlist = netlist
        
        # # Output simulation waves. Each key corresponds to a different wave.
        # self.waves = None
        
        pass
    
    @sync_track
    def setup(self, currents):
        """Setup simulation, like loading netlist."""
        
        
        
        raise ValueError(f"\n\n***Error --> setup not supported yet!\n")
    

    @sync_track
    def start(self):
        """Fire simulation, and stops after it finishes (or timeout or abort). Populate 'waves' as the output."""
        
        
        
        raise ValueError(f"\n\n***Error --> start not supported yet!\n")
    

    @sync_track
    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    @sync_track
    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist

    @sync_track
    def getWave(self, wave):
        """For a given wave name, return its corresponding value."""
        
        
        
        raise ValueError(f"\n\n***Error --> getWave not implemented yet\n")
        
        wave = None
        
        return wave

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj