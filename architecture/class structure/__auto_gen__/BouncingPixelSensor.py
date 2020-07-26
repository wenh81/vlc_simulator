from Circuit import Circuit

class BouncingPixelSensor(Circuit):
    def __init__(self, netlist, simulator):
        """Constructor"""

        Circuit.__init__(self, netlist = netlist, simulator = simulator)
        

        # Stores the netlist of the circuit.
        self.netlist = netlist

        # Defines the simulator for that netlist
        self.which_simulator = simulator
    
        pass

    def calc_out_voltage(self, input_photocurrent_file):
        """Calculates the output reconstructed voltage."""
        pass
    
