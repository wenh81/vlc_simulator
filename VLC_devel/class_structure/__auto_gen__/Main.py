from Message import Message

from Mapping import Mapping

from Modulator import Modulator

from Transmitter import Transmitter

from Channel import Channel

from Receiver import Receiver

from MeritFunctions import MeritFunctions

from Global import Global

class Main(object):
    def __init__(self, DEBUG=False):
        """Constructor"""
        
        if DEBUG:
            print('Running Main...')
        
        

        # Message object.
        self.message_obj = Message(input_info=input_info, n_frames=n_frames)

        # Mapping object.
        self.mapping_obj = Mapping(bitstream_frames=bitstream_frames, mapping_type=mapping_type, bits_per_symbol=bits_per_symbol)

        # Modulator object.
        self.modulator_obj = Modulator(mapped_info=mapped_info, modulation_type=modulation_type)

        # Transmitter object.
        self.transmitter_obj = Transmitter(transmitter_config=transmitter_config, tx_data=tx_data, bypass=bypass)

        # Channel object
        self.channel_obj = Channel(tx_data_in=tx_data_in, raytrace=raytrace)

        # Receiver object.
        self.receiver_obj = Receiver(receiver_config=receiver_config, rx_data=rx_data, bypass=bypass)

        # Merit Funcions object
        self.merit_functions_obj = MeritFunctions()

        # Global object.
        self.global_obj = Global()
    
        pass

    def getMessageObj(self):
        """Returns value of self.message_obj"""
        
        return self.message_obj

    def setMessageObj(self, message_obj):
        """Set new value for self.message_obj"""
        
        self.message_obj = message_obj

    def getMappingObj(self):
        """Returns value of self.mapping_obj"""
        
        return self.mapping_obj

    def setMappingObj(self, mapping_obj):
        """Set new value for self.mapping_obj"""
        
        self.mapping_obj = mapping_obj

    def getModulatorObj(self):
        """Returns value of self.modulator_obj"""
        
        return self.modulator_obj

    def setModulatorObj(self, modulator_obj):
        """Set new value for self.modulator_obj"""
        
        self.modulator_obj = modulator_obj

    def getTransmitterObj(self):
        """Returns value of self.transmitter_obj"""
        
        return self.transmitter_obj

    def setTransmitterObj(self, transmitter_obj):
        """Set new value for self.transmitter_obj"""
        
        self.transmitter_obj = transmitter_obj

    def getChannelObj(self):
        """Returns value of self.channel_obj"""
        
        return self.channel_obj

    def setChannelObj(self, channel_obj):
        """Set new value for self.channel_obj"""
        
        self.channel_obj = channel_obj

    def getReceiverObj(self):
        """Returns value of self.receiver_obj"""
        
        return self.receiver_obj

    def setReceiverObj(self, receiver_obj):
        """Set new value for self.receiver_obj"""
        
        self.receiver_obj = receiver_obj

    def getMeritFunctionsObj(self):
        """Returns value of self.merit_functions_obj"""
        
        return self.merit_functions_obj

    def setMeritFunctionsObj(self, merit_functions_obj):
        """Set new value for self.merit_functions_obj"""
        
        self.merit_functions_obj = merit_functions_obj

    def getGlobalObj(self):
        """Returns value of self.global_obj"""
        
        return self.global_obj

    def setGlobalObj(self, global_obj):
        """Set new value for self.global_obj"""
        
        self.global_obj = global_obj
