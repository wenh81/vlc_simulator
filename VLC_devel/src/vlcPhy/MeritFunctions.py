from .common_imports import *

class MeritFunctions(object):
    
    def __init__(self, sync_obj):
        """Constructor of MeritFunctions."""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        # Get debug and plot flags
        self.DEBUG, self.PLOT = lib.getDebugPlot("MeritFunctions", self.sync_obj)
        
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

    @sync_track
    def calculateBER(self, tx_data, rx_data):
        """Calculates the BER, for each frame."""
        
        
        self.BER = []
        self.numb_bit_err = []
        
        # for idx in range(0, len(tx_data_list)):
            
            # rx_data = rx_data_list[idx]
            # tx_data = tx_data_list[idx]
            
        bit_err = 0
        diff = len(rx_data) - len(tx_data)
        diff_bits_rx = []
        diff_bits_tx = []
        for bit_idx in range(0, len(tx_data)):
            if rx_data[bit_idx + diff] != tx_data[bit_idx]:
                bit_err += 1
                diff_bits_rx.append(rx_data[bit_idx + diff])
                diff_bits_tx.append(tx_data[bit_idx])
            else:
                diff_bits_rx.append('.')
                diff_bits_tx.append('.')
        
        diff_bits_tx = ''.join(diff_bits_tx)
        diff_bits_rx = ''.join(diff_bits_rx)

        self.numb_bit_err.append(bit_err)
        self.BER.append(bit_err/len(rx_data)*100)
        
        
        self.pretty_diff = f"""
Number of bits with error << {self.numb_bit_err} >>
Obtained Bit error rate << {self.BER} >> % 

Tx data:
{tx_data}
Rx data:
{rx_data}
Diff bits at Tx:
{diff_bits_tx}
Diff bits at Rx:
{diff_bits_rx}
"""

        # if self.DEBUG:
        #     print(self.pretty_diff)
        
        return self.BER, self.numb_bit_err, self.pretty_diff
    

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