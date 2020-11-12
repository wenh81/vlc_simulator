from Channel import Channel

from Receiver import Receiver

from Simulator import Simulator

from Global import Global

class Main(object):
    def __init__(self, transmitter_array, channel_obj, receiver_array, simulator_obj, global_obj):
        """Constructor"""

        # Array of transmitters
        self.transmitter_array = [Transmitter(parent_var1=parent_var1, parent_var2=parent_var2)]*Config.n_transmitters

        # Channel object
        self.channel_obj = Channel(ray_paths=ray_paths, ray_delays=ray_delays)

        # Array of receivers
        self.receiver_array = [Receiver()]*Config.n_receivers

        # Simulator object
        self.simulator_obj = Simulator()

        # Global object
        self.global_obj = Global()
    
        pass
