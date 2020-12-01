class Simulator(object):
    def __init__(self, netlist, DEBUG=False):
        """Constructor."""
        
        if DEBUG:
            print('Running Simulator...')
        
        

        # Timeout to abort simul, after that time is passed.
        self.simul_timeout = None

        # Netlist of circuit to be simulated.
        self.netlist = netlist
    
        pass

    def stopSimulation(self):
        """Abort simulation, by user command or timeout."""
        pass
    

    def getSimulTimeout(self):
        """Returns value of self.simul_timeout"""
        
        return self.simul_timeout

    def setSimulTimeout(self, simul_timeout):
        """Set new value for self.simul_timeout"""
        
        self.simul_timeout = simul_timeout

    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist
