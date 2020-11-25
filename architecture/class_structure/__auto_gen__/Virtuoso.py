from Simulator import Simulator

class Virtuoso(Simulator):
    def __init__(self, netlist, wave_names, DEBUG=False):
        """Constructor."""
        
        if DEBUG:
            print('Running Virtuoso...')
        
        

        Simulator.__init__(self, netlist = netlist)
        

        # Netlist of circuit to be simulated.
        self.netlist = netlist

        # Output simulation waves. Each key corresponds to a different wave.
        self.waves = None
    
        pass

    def setupVirtuoso(self):
        """Setup simulation, like loading netlist."""
        pass
    

    def startVirtuoso(self):
        """Fire simulation, and stops after it finishes (or timeout or abort). Populate 'waves' as the output."""
        pass
    

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
