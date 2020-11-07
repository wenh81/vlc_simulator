class Circuit(object):
    def __init__(self, netlist, simulator):
        """Constructor"""

        # Stores the netlist of the circuit.
        self.netlist = netlist

        # Defines the simulator for that netlist
        self.which_simulator = simulator
    
        pass

    def calc_out_voltage(self, input_photocurrent_file):
        """Calculates the output reconstructed voltage."""
        pass
    

