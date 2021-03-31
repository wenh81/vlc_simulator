from .common_imports import *


class BouncingPixel(ROIC):
    
    def __init__(self, gain, circuit_simulation, waves_name, DR, current_noise, SNR, roic_setup, sync_obj):
        """Constructor of BouncingPixel."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("BouncingPixel") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("BouncingPixel")
        
        if self.DEBUG:
            print('Running BouncingPixel...')
        
        # Stores the circuit topology.
        self.circuit_type = "BouncingPixel"
        
        # Stores the list of wave names to be derived
        self.waves_name = waves_name
        
        # Default value of transconductance gain (V/A) -- 60 mV/uA = 60*1e3
        self.transconductance_gain = gain
        
        # Flag to indicate use of circuit simulation.
        self.circuit_simulation = circuit_simulation

        # Dynamic range (in dB)
        self.DR = DR

        # input referred current noise (in A)
        self.current_noise = current_noise
        
        # SNR (in dB)
        self.SNR = SNR
        
        # Further ROIC setup (when needed)
        self.roic_setup = roic_setup

        ROIC.__init__(self, 
            circuit_type = self.circuit_type,
            waves_name = self.waves_name,
            transconductance_gain = self.transconductance_gain,
            circuit_simulation = self.circuit_simulation,
            DR = self.DR,
            current_noise = self.current_noise,
            SNR = self.SNR,
            roic_setup = self.roic_setup,
            sync_obj = sync_obj
            )
        

        # Curve that translates how to convert from photocurrent to voltage.
        self.linearity_curve = {"photocurrent": [], "voltage": []}
        
        # Stores the netlist of the circuit.
        self.netlist = None

        # Original Path to netlist of the circuit
        self.netlist_path = None
        
        # Path to netlist of the circuit to be simulated
        self.simul_netlist_path = None

        

    @sync_track
    def calculatesReconstructedVoltage(self, all_waves):
        """Depending on circuit simulator, calculates the reconstructed voltage from simulation."""
        
        if self.circuit_simulation:

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
        
        else:
            # If circuit simulation is off, then no need for voltage reconstruction
            # since the transconductance gain was directly applied to the input current
            return all_waves
                
    
    @sync_track
    def editNetlist(self):
        """Edit netlist to setup simulationt time, integration time, etc."""
        
        if self.which_simulator == "Tanner":
            
            # currents_path = Path.cwd()
            data_folder = Path(self.simulator_config[self.which_simulator][Global.operating_system]['data_folder'])
            
            # to store the currents files for Tanner
            currents_path = data_folder / "currents"
            
            # Creates the currents folder
            if not Path.exists(currents_path):
                Path.mkdir(currents_path)
            
            # to store simulation logs for Tanner
            simul_log_path = data_folder / "simulation_logs"

            # Creates the currents folder
            if not Path.exists(simul_log_path):
                Path.mkdir(simul_log_path)
            
            # open and edit netlist
            self.netlist_path = self.simulator_config[self.which_simulator][Global.operating_system]['netlist']
            with open(self.netlist_path, "r") as net:
                self.netlist = net.read().format(
                    simul_corner = self.simulator_config[self.which_simulator][Global.operating_system]['simul_corner'],
                    library = self.simulator_config[self.which_simulator][Global.operating_system]['library'],
                    temperature = int(Global.temperature) - 273,
                    vmin = self.roic_setup["vmin"],
                    vmax = self.roic_setup["vmax"],
                    stepTran = self.roic_setup["stepTran"],
                    currents_path = currents_path,
                    n_ml = "6"
                    )
            
            # get path of netlist to be simulated
            self.simul_netlist_path = simul_log_path / "BouncingPixel.sp"
            
            # Save netlist to a file
            with open(self.simul_netlist_path, "w") as net:
                net.write(self.netlist)


        elif self.which_simulator == "Virtuoso":
            raise ValueError(f"\n\n***Error --> Simulator < {self.which_simulator} > not supported yet for netlisting!\n")
        
        else:
            raise ValueError(f"\n\n***Error --> Simulator < {self.which_simulator} > not supported yet for netlisting!\n")


    @sync_track
    def getCircuitType(self):
        """Returns value of self.circuit_type"""
        
        return self.circuit_type

    @sync_track
    def setCircuitType(self, circuit_type):
        """Set new value for self.circuit_type"""
        
        self.circuit_type = circuit_type

    @sync_track
    def getCircuitSimulation(self):
        """Returns value of self.circuit_simulation"""
        
        return self.circuit_simulation

    @sync_track
    def setCircuitSimulation(self, circuit_simulation):
        """Set new value for self.circuit_simulation"""
        
        self.circuit_simulation = circuit_simulation

    @sync_track
    def getLinearityCurve(self):
        """Returns value of self.linearity_curve"""
        
        return self.linearity_curve

    @sync_track
    def setLinearityCurve(self, linearity_curve):
        """Set new value for self.linearity_curve"""
        
        self.linearity_curve = linearity_curve

    # @sync_track
    # def getWhichSimulator(self):
    #     """Returns value of self.which_simulator"""
        
    #     return self.which_simulator

    # @sync_track
    # def setWhichSimulator(self, which_simulator):
    #     """Set new value for self.which_simulator"""
        
    #     self.which_simulator = which_simulator

    # @sync_track
    # def getNetlist(self):
    #     """Returns value of self.netlist"""
        
    #     return self.netlist

    # @sync_track
    # def setNetlist(self, netlist):
    #     """Set new value for self.netlist"""
        
    #     self.netlist = netlist

    # @sync_track
    # def getNetlistPath(self):
    #     """Returns value of self.netlist_path"""
        
    #     return self.netlist_path

    # @sync_track
    # def setNetlistPath(self, netlist_path):
    #     """Set new value for self.netlist_path"""

    #     self.netlist_path = netlist_path

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj