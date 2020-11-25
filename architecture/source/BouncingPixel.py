from ROIC import ROIC

import Global

class BouncingPixel(ROIC):
    def __init__(self, sync_obj):
        """Constructor of LightSource. Receives the light_type"""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug()
        
        self.sync_obj.appendToSimulationPath("BouncingPixel")
        
        if self.DEBUG:
            print('Running BouncingPixel...')
        
        # Stores the circuit topology.
        self.circuit_type = "BouncingPixel"
        
        # Stores the list of wave names to be derived
        self.waves_name = None
        
        ROIC.__init__(self, circuit_type = self.circuit_type, waves_name = self.waves_name, sync_obj = sync_obj)
        
        # Flag to indicate use of circuit simulation.
        self.circuit_simulation = Global.circuit_simulation

        # Curve that translates how to convert from photocurrent to voltage.
        self.linearity_curve = {"photocurrent": [], "voltage": []}

        # Defines the simulator to be used, if appliable.
        self.which_simulator = Global.which_simulator

        # Stores the netlist of the circuit.
        self.netlist = None

        # Path to netlist of the circuit.
        self.netlist_path = None
        

    def calculatesReconstructedVoltage(self, all_waves):
        """Depending on circuit simulator, calculates the reconstructed voltage from simulation."""
        self.sync_obj.appendToSimulationPath("calculatesReconstructedVoltage @ BouncingPixel")
        
        # Set previous for debug
        self.sync_obj.setPrevious("BouncingPixel")
        
        # Calculates the reconstructed voltage depending on the simulator.
        if self.which_simulator == "Virtuoso":
            
            raise ValueError(f"\n\n***Error --> Analysis for the waves to get the output voltage from Virtuoso not supported yet!\n")
            
            rx_voltage_list = None
            # return rx_voltage_list = FUNTION(all_waves)
        
        elif self.which_simulator == "Tanner":
            
            raise ValueError(f"\n\n***Error --> Analysis for the waves to get the output voltage from Tanner not supported yet!\n")
            
            # return rx_voltage_list = FUNTION(all_waves)
            rx_voltage_list = None
            
        else:
            raise ValueError(f"\n\n***Error --> Simulator < {self.which_simulator} > at Global.which_simulator is not supported!\n")
        
        return rx_voltage_list
    
    def editNetlist(self):
        """Edit netlist to setup simulationt time, integration time, etc."""
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
