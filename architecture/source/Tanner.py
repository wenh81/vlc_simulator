from Simulator import Simulator

class Tanner(Simulator):
    def __init__(self, netlist, sync_obj):
        """Constructor."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug()
        
        self.sync_obj.appendToSimulationPath("Tanner")
        
        if self.DEBUG:
            print('Running Tanner...')
        
        
        Simulator.__init__(self, netlist = netlist, sync_obj = sync_obj)
        

        # Netlist of circuit to be simulated.
        self.netlist = netlist

        # Output simulation waves. Each key corresponds to a different wave.
        self.waves = None
    
        pass
    
    def setup(self, currents):
        """Setup simulation, like loading netlist."""
        
        self.sync_obj.appendToSimulationPath("setup @ Tanner")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Tanner")
        
        raise ValueError(f"\n\n***Error --> setup not supported yet!\n")
    

    def start(self):
        """Fire simulation, and stops after it finishes (or timeout or abort). Populate 'waves' as the output."""
        
        self.sync_obj.appendToSimulationPath("start @ Tanner")
        
        # Set previous for debug
        self.sync_obj.setPrevious("Tanner")
        
        raise ValueError(f"\n\n***Error --> start not supported yet!\n")
    

    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist

    def getWaves(self):
        """Returns value of self.waves"""
        
        return self.waves

    def setWaves(self, waves):
        """Set new value for self.waves"""
        
        self.waves = waves
