from tabulate import tabulate

class SimulationSync(object):
    def __init__(self, previous, DEBUG=False):
        """Constructor of SimulationSync. Used for overral simulation control and debug."""
        
        self.DEBUG = DEBUG
        
        if self.DEBUG:
            print('Running SimulationSync...')
        
        # String with the followed path for the whole simulation
        self.simulation_path = ""
        
        # Stores previous object, from where given object was called
        self.previous = previous
        

    def appendToSimulationPath(self, next_path):
        """Set new value for self.simulation_path"""
        
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

    def getSimulationPath(self):
        """Returns value of self.simulation_path"""
        
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
    
    def getDebug(self):
        """Returns value of self.DEBUG"""
        
        return self.DEBUG

    def setDebug(self, DEBUG):
        """Set new value for self.DEBUG"""
        
        self.DEBUG = DEBUG
    
    def getPrevious(self):
        """Returns value of self.previous"""
        
        return self.previous

    def setPrevious(self, previous):
        """Set new value for self.previous"""
        
        self.previous = previous
