from .common_imports import *

class SimulationSync(object):
    def __init__(self, previous, DEBUG=False, PLOT=False):
        """Constructor of SimulationSync. Used for overral simulation control and debug."""
        
        self.DEBUG = DEBUG
        
        self.PLOT = PLOT
        
        if self.DEBUG["all"] or self.DEBUG["SimulationSync"]:
            print('Running SimulationSync...')
        
        # String with the followed path for the whole simulation
        self.simulation_path = ""
        
        # Stores previous object, from where given object was called
        self.previous = previous
        
        # Dictionary with all information on the message frames
        # self.message_dict = {
        #     "n_frames": 0,
        #     "type": [],
        #     "send_iterations": []
        # }
        self.message_dict = {}
        
        
    def appendToSimulationPath(self, next_path):
        """Set new value for self.simulation_path"""
        
        # If simul sync is enabled
        if self.DEBUG["all"] or self.DEBUG["SimulationSync"]:
            # Append previous info
            next_path = f"Called << {next_path} >> From << {self.previous} >>"
            
            if self.simulation_path != "":
                # if "@" not in next_path:
                #     self.simulation_path = f"{self.simulation_path}\n>>> {next_path}"
                # else:
                #     self.simulation_path = f"{self.simulation_path}\n>>>\t{next_path}"
                self.simulation_path = f"{self.simulation_path}\n> {next_path};"
            else:
                self.simulation_path = f"> {next_path};"
            
    def showSimulationPath(self):
        """Returns value of self.simulation_path"""
        
        # If simul sync is not enabled
        if not self.DEBUG["all"] and not self.DEBUG["SimulationSync"]:
            return "<< SimulationSync DEBUG is disabled! >>"
        
        tabular_data = self.simulation_path.replace('\n', '')\
            .replace('<', '').replace('>', '')\
                .replace('Called', '').strip()
        tabular_data = [line for line in tabular_data.split(';')]
        tabular_data = [[item.strip() for item in line.split('From')] for line in tabular_data]
        
        tabular_data = tabulate(tabular_data, headers=['Called', 'From'])
        
        return f"""
************************* SIMULATION PATH *************************

{tabular_data}

*******************************************************************
"""

    def setSimulationPath(self, simulation_path):
        """Set new value for self.simulation_path"""
        
        self.simulation_path = simulation_path
    
    def getSimulationPath(self):
        """Get new value for self.simulation_path"""
        
        return self.simulation_path
    
    def getDebug(self, module = "all"):
        """Returns value of self.DEBUG"""
        
        return self.DEBUG[module]

    def setDebug(self, DEBUG, module = "all"):
        """Set new value for self.DEBUG"""
        
        self.DEBUG = DEBUG[module]
    
    def getPlot(self, module = "all"):
        """Returns value of self.PLOT"""
        
        return self.PLOT[module]

    def setPlot(self, PLOT, module = "all"):
        """Set new value for self.PLOT"""
        
        self.PLOT = PLOT[module]
    
    def getPrevious(self):
        """Returns value of self.previous"""
        
        return self.previous

    def setPrevious(self, previous):
        """Set new value for self.previous"""
        
        self.previous = previous
    
    def showMessageDict(self):
        """Returns value of self.message_dict"""
        
        # If simul sync is not enabled
        if not self.DEBUG["all"] and not self.DEBUG["SimulationSync"]:
            return "<< SimulationSync DEBUG is disabled! >>"
        
        all_descriptions = ['TX', 'RX', '# packets',\
            'Data type', 'BER (%)',\
                '# bit error', 'Total #bits']
        tabular_data = []
        # tabular_data.append(all_descriptions)
        for index in range(0, len(self.message_dict["tx_info"])):
            sub_list = [
                str(self.message_dict["tx_info"][index]),
                str(self.message_dict["rx_info"][index]),
                self.message_dict["packets"][index],
                self.message_dict["type"][index],
                f'{self.message_dict["BER"][index]} %',
                f'{self.message_dict["NBER"][index]} bits',
                f'{self.message_dict["n_bits"][index]} bits'
                
            ]
            # WRONG CALCULATION FOR IMAGES!!!!!!!!!!
            
            tabular_data.append(sub_list)
            
        # tabular_data = tabulate(tabular_data, headers=['TX', 'RX', 'Type', 'BER', 'NBER'])
        tabular_data = tabulate(tabular_data, headers = all_descriptions)
        
        return f"""
************************* RUN SUMMARY *************************

Number of frames sent: << {self.message_dict["n_frames"]} >>

Frames detail:

{tabular_data}

*******************************************************************
"""
        # return self.message_dict

    def setMessageDict(self, message_dict):
        """Set new value for self.message_dict"""
        
        self.message_dict = message_dict
    
    def getMessageDict(self):
        """Get new value for self.message_dict"""
        
        return self.message_dict
        
    def appendToMessageDict(self, key, value):
        """Set new value for self.message_dict"""
        
        # If simul sync is enabled
        if self.DEBUG["all"] or self.DEBUG["SimulationSync"]:
            
            # Create empty list, if does not exist yet
            if key not in self.message_dict.keys():
                self.message_dict[key] = []
            
            # Add to list
            if isinstance(value, list):
                self.message_dict[key] += value
            else:
                self.message_dict[key].append(value)
            
            # print("\n\nappendToMessageDict....")
            # print(self.message_dict[key])
            # print(key)
            # print(value)
            # print()
        