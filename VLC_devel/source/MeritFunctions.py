from generalLibrary import timer_dec, sync_track

import numpy as np

class MeritFunctions(object):
    
    def __init__(self, sync_obj):
        """Constructor of MeritFunctions."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("MeritFunctions") or self.sync_obj.getDebug("all")
        
        self.PLOT = self.sync_obj.getPlot()
        
        self.sync_obj.appendToSimulationPath("MeritFunctions")
        
        if self.DEBUG:
            print('Running MeritFunctions...')
        
        print('''\n
********************************************************************

                            RESULTS

********************************************************************''')
        
        # List of Bit-Error Rates, for each frame.
        self.BER = None

        # Overall system Signal-To-Noise Ratio
        self.SNR = None

        # Average datarate for the whole process.
        self.DataRate = None
    
        pass

    @sync_track
    def calculateBER(self, tx_data_list, rx_data_list):
        """Calculates the BER, for each frame."""
        
        
        self.BER = []
        self.numb_bit_err = []
        
        for idx in range(0, len(tx_data_list)):
            
            rx_data = rx_data_list[idx]
            tx_data = tx_data_list[idx]
            
            bit_err = 0
            diff = len(rx_data) - len(tx_data)
            for bit_idx in range(0, len(tx_data)):
                if rx_data[bit_idx + diff] != tx_data[bit_idx]:
                    bit_err += 1
            
            self.numb_bit_err.append(bit_err)
            self.BER.append(bit_err/len(rx_data)*100)
        
        if self.DEBUG:
            print (f"Number of bits with error << {self.numb_bit_err} >> ")
            print (f"Obtained Bit error rate << {self.BER} >> % ")
        
        return self.BER
    

    @sync_track
    def calculateSNR(self):
        """Calculates the overall SNR."""
        pass
    

    @sync_track
    def calculateDataRate(self):
        """Calculates the overall Data Rate."""
        pass
    

    @sync_track
    def getBER(self):
        """Returns value of self.BER"""
        
        return self.BER

    @sync_track
    def setBER(self, BER):
        """Set new value for self.BER"""
        
        self.BER = BER

    @sync_track
    def getSNR(self):
        """Returns value of self.SNR"""
        
        return self.SNR

    @sync_track
    def setSNR(self, SNR):
        """Set new value for self.SNR"""
        
        self.SNR = SNR

    @sync_track
    def getDataRate(self):
        """Returns value of self.DataRate"""
        
        return self.DataRate

    @sync_track
    def setDataRate(self, DataRate):
        """Set new value for self.DataRate"""
        
        self.DataRate = DataRate

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj