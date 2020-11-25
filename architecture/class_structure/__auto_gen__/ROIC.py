class ROIC(object):
    def __init__(self, circuit_type, circuit_simulation, which_simulator, DEBUG=False):
        """Constructor of LightSource. Receives the light_type"""
        
        if DEBUG:
            print('Running ROIC...')
        
        

        # Stores the circuit topology. Ex: APS, Bouncing Pixel, etc.
        self.circuit_type = circuit_type

        # Flag to indicate use of circuit simulation.
        self.circuit_simulation = circuit_simulation

        # Curve that translates how to convert from photocurrent to voltage.
        self.linearity_curve = {"photocurrent": [], "voltage": []}

        # Defines the simulator to be used, if appliable.
        self.which_simulator = simulator

        # Stores the netlist of the circuit.
        self.netlist = None

        # Path to netlist of the circuit.
        self.netlist_path = None
    
        pass

    def convertsToVoltage(self, current):
        """Converts a given photocurrent into associated voltage. If flag to use circuit_simulation is active, then calls the """
        pass
    

    def callSimulator(self):
        """Calls the desired circuit simulator, given the 'circuit_type', and arrat of currents to be simulated."""
        pass
    

    def getCircuitType(self):
        """Returns value of self.circuit_type"""
        
        return self.circuit_type

    def setCircuitType(self, circuit_type):
        """Set new value for self.circuit_type"""
        
        self.circuit_type = circuit_type

    def getCircuitSimulation(self):
        """Returns value of self.circuit_simulation"""
        
        return self.circuit_simulation

    def setCircuitSimulation(self, circuit_simulation):
        """Set new value for self.circuit_simulation"""
        
        self.circuit_simulation = circuit_simulation

    def getLinearityCurve(self):
        """Returns value of self.linearity_curve"""
        
        return self.linearity_curve

    def setLinearityCurve(self, linearity_curve):
        """Set new value for self.linearity_curve"""
        
        self.linearity_curve = linearity_curve

    def getWhichSimulator(self):
        """Returns value of self.which_simulator"""
        
        return self.which_simulator

    def setWhichSimulator(self, which_simulator):
        """Set new value for self.which_simulator"""
        
        self.which_simulator = which_simulator

    def getNetlist(self):
        """Returns value of self.netlist"""
        
        return self.netlist

    def setNetlist(self, netlist):
        """Set new value for self.netlist"""
        
        self.netlist = netlist

    def getNetlistPath(self):
        """Returns value of self.netlist_path"""
        
        return self.netlist_path

    def setNetlistPath(self, netlist_path):
        """Set new value for self.netlist_path"""
        
        self.netlist_path = netlist_path
