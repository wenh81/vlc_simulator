from Message import Message

from Mapping import Mapping

from Modulator import Modulator

from Transmitter import Transmitter

from Channel import Channel

from Receiver import Receiver

from MeritFunctions import MeritFunctions

from SimulationSync import SimulationSync

import Global

from beeprint import pp
# import beeprint as pp

import numpy as np

from matplotlib import pyplot as plt

import generalLibrary as lib

from generalLibrary import timer_dec, sync_track

from generalLibrary import printDebug, plotDebug

from timeit import default_timer as timer

from scipy import signal

# first time random is imported
import random
random.seed(Global.rand_seed)

class VLC(object):
    
    @timer_dec
    def __init__(self):
        """Constructor"""
        
        self.DEBUG = Global.DEBUG["VLC"] or Global.DEBUG["all"]
        
        self.PLOT = Global.PLOT["VLC"] or Global.PLOT["all"]
        
        self.start_timer = timer()
        
        if self.DEBUG:
            print('Running VLC...')
            pass
        
        ###########################################################################
        # >>>>>>>>>> CREATE SIMULATION SYNC OBJECT
        
        # Create object for SimulationSync, used for overral simulation control and debug.
        self.sync_obj = SimulationSync(
            DEBUG = Global.DEBUG,
            PLOT = Global.PLOT,
            previous = "VLC"
            )
        
        ###########################################################################
        # >>>>>>>>>> CREATE MESSAGE OBJECT
        
        # Creates message object.
        self.message_obj = Message(
            input_info=Global.input_info,
            n_frames=len(Global.input_info["data"]),
            sync_obj = self.sync_obj
        )
        
        if self.DEBUG:
            print(self.message_obj.getInputInfo())
            pass
        
        ###########################################################################
        # >>>>>>>>>> CONVERT MESSAGES TO LIST OF BITSTREAMS
            
        # Converts it from its original type to a stream of bits (stored in bitstream_frames)
        self.message_obj.convertsToBitstream()
        
        ###########################################################################
        # >>>>>>>>>> FOR EACH MESSAGE, ITERATE THROUGH ITS BITSTREAM FROM TRANSMITTER UP TO RECEIVER
        
        # starts empty list with all received frames
        rx_frames = []
        
        # APPLY MULTIPROCESS ON THESE LOOP...
        # For loop for each frame bitstream (each information to be sent in Global.input_info)
        for curr_frame in self.message_obj.getBitstreamFrames():
            
            # Start number of packets
            self.sync_obj.appendToMessageDict("packets", 0)
            
            # if self.DEBUG:
            #     print(f'curr_frame = {curr_frame}')
            #     pass
            
            ###########################################################################
            # >>>>>>>>>> FOR THAT BITSTREAM, STARTS MODULATION, GIVEN MODULATION CONFIG
            
            # Modulator object.
            self.modulator_obj = Modulator(
                bitstream_frame=curr_frame,
                modulation_config=Global.modulation_config[Global.modulation_index],
                mapping_config=Global.mapping_config[Global.mapping_index],
                sync_obj = self.sync_obj
            )
            
            ###########################################################################
            # >>>>>>>>>> CREATES MODULATION OBJECT, DEPENDING ON THE TYPE (EX: OFDM)
            
            # Creates the modulator object, depending on the 'modulation_type' in 'modulation_config'
            self.modulator_obj.createModulator()
            
            ###########################################################################
            # >>>>>>>>>> APPLY MODULATION GIVEN CHOOSEN TYPE (EX: OFDM)
            
            # Applies the modulation, with modulation object just created
            self.modulator_obj.applyModulation()
            
            ###########################################################################
            # >>>>>>>>>> GET THE LIST OF DATA TO BE TRANSMITTED, AFTER MODULATION
            # >>>>>>>>>> DEPENDING ON TRANSMITTER THROUGHPUT, MORE THAN ONE TX_DATA
            # >>>>>>>>>> IS NEEDED
            
            # Return a list of symbols to be transmitted.
            # This list is defined by the throughput of the modulator
            self.tx_data_list = self.modulator_obj.getTxDataList()
            
            
            ###########################################################################
            # >>>>>>>>>> STARTS TRANSMITTER, GIVEN CONFIG
            
            # Transmitter object.
            self.transmitter_obj = Transmitter(
                transmitter_config = Global.transmitter_config,
                tx_data_list = self.tx_data_list,
                sync_obj = self.sync_obj
            )

            printDebug(len(self.tx_data_list))
            printDebug(self.tx_data_list)
            # plotDebug(self.tx_data_list[0])
            # plotDebug(self.tx_data_list[1])
            # sad
            
            ###########################################################################
            # >>>>>>>>>> APPLY DAC ON TX_DATA, CONVERTING TO ANALOG. CAN BE 
            # >>>>>>>>>> BYPASSED BY Global.bypass_dict["DAC"]
            
            # Applies Low-Pass Filter
            self.transmitter_obj.applyFilter(
                filter_order = 20,
                # cuttof = 400e6,
                # cuttof = Global.simul_frequency*(0.3),
                cuttof = Global.simul_frequency*(0.49),
                filter_type = 'low'
            )
            
            # Applies DAC
            self.transmitter_obj.applyDAC(offset_value = 0)
            
            ## TODO ---- ADD HERE THE ADDITION OF THE DC VALUE OF DCO-OFDM MODULATION (VOLTAGE DOMAIN)
            
            ###########################################################################
            # >>>>>>>>>> CALCULATES OPTICAL POWER, DEPENDING ON THE LIGHTSOURCES
            # >>>>>>>>>> OR CAN BE BYPASSED BY Global.bypass_dict["LightSource"]
            
            # Calculates the optical power provided by the light sources
            self.transmitter_obj.calculatesOpticalPower()
            
            ###########################################################################
            # >>>>>>>>>> RETRIEVE TX_DATA LIST FOR THE CHANNEL
            
            # Gets the list of optical powers to be transmitted
            tx_data_list = self.transmitter_obj.getTxOpticalOutList()
            
            # Creates global full time vector with Global.time_frame * (number of symbols in current frame)
            Global.full_time_vector = [np.arange(0, Global.number_of_points)*Global.time_step \
                + idx*Global.time_frame \
                    for idx in range(len(tx_data_list))]

            printDebug(Global.full_time_vector)
            printDebug(len(Global.full_time_vector))

            if self.PLOT:
                handle = plt.figure(figsize=(8,2))
                # lib.plotTxRxDataList(tx_data_list, Global.full_time_vector, 'TX DATA', handle, self.sync_obj, show = False)
                # printDebug(Global.full_time_vector)
                ################## lib.plotTxRxDataList(tx_data_list, Global.full_time_vector, 'TX DATA', handle, self.sync_obj, show = False)
            
            
            ###########################################################################
            # >>>>>>>>>> CREATES CHANNEL GIVEN INPUT TX_DATA LIST
            
            # Channel object
            self.channel_obj = Channel(
                tx_data_in = tx_data_list,
                sync_obj = self.sync_obj
            )
            
            
            # If not bypassing Channel, calculates the channel impulse response (CIR)
            if not Global.bypass_dict["Channel"]:
                
                ###########################################################################
                # >>>>>>>>>> CALCULATES CHANNEL RESPONSE FOR EACH LIGHTSOURCE, IF NOT BYPASSED
                
                raise ValueError(f"\n\n***Error --> Calculation of channel response for each LightSource, when NOT bypassing 'Channel', not implemented yet!\n")
            
                # calculates the impulse response
                self.channel_obj.calculatesChannelResponse()
                
            else:
                
                ###########################################################################
                # >>>>>>>>>> IF BYPASSING (Global.bypass_dict["Channel"]) MUST SET THE 
                # >>>>>>>>>> CIR FOR EACH LIGHTSOURCE
                
                # sets the channel response for each lamp
                # If lightsource is not bypassed
                if not Global.bypass_dict["LightSource"]:
                    # setChannelResponse for each lamp
                    raise ValueError(f"\n\n***Error --> Set channel response for each LightSource, when bypassing 'Channel', not implemented yet!\n")
                    # self.channel_obj.setChannelResponse([...])
                    
                else:
                    # set fake channel impulse response from input
                    self.channel_obj.definesChannelResponse()
                    # # Set single channel response (list of 1 position) ....
                    # self.channel_obj.setChannelResponse(Global.list_of_channel_response)
            
            ###########################################################################
            # >>>>>>>>>> APPLY EACH CIR (FOR EACH LIGHTSOURCE) TO EACH TX_DATA.
            
            # After channel reponse set, apply it to each lamp.
            self.channel_obj.applyChannelResponse()

            
            ###########################################################################
            # >>>>>>>>>> GET RX_DATA LIST CONVOLVED BY CHANNEL AFTER ADDING NOISE.
            
            # Gets the list of optical powers at the receiver, after convolution on channel response, and noise additi-YCon.
            rx_data_list = self.channel_obj.getRxDataOut()

            # Re-calculates full time vector, after convolution
            # Creates global full time vector with Global.time_frame * (number of symbols in current frame)
            Global.full_time_vector = [np.arange(0, len(rx_data_list[idx]))*Global.time_step \
                + idx*Global.time_frame \
                    for idx in range(len(rx_data_list))]
            
            if self.PLOT:
                printDebug(len(rx_data_list[0]))
                printDebug(len(Global.full_time_vector[0]))
                # printDebug(rx_data_list)
                # plotDebug(tx_data_list[0], Global.full_time_vector[0], symbols='ro-')
                # plotDebug(tx_data_list[1], Global.full_time_vector[1], symbols='ro-')
                # plotDebug(rx_data_list[0], Global.full_time_vector[0], symbols='ro-')
                # plotDebug(rx_data_list[1], Global.full_time_vector[1], symbols='ro-')
                
                lib.plotTxRxDataList(rx_data_list, 'RX DATA', handle, self.sync_obj, show = True)
                # lib.plotTxRxDataList(rx_data_list, 'RX DATA', handle, self.sync_obj, show = True)
            
            ###########################################################################
            # >>>>>>>>>> STARTS RECEIVER, GIVEN CONFIG
            
            # Receiver object.
            self.receiver_obj = Receiver(
                receiver_config = Global.receiver_config,
                roic_config = Global.roic_config, # read-out integrated circuit
                rx_data_list = rx_data_list,
                sync_obj = self.sync_obj
            )

            # Assemble wave train. That is, get list of convoluted signals,
            # and assemble single wave train. This is because the convolution adds 1 OFDM symbol 
            # from the total o N symbols (total of N + 1). On the modulator, this will be solved 
            # when group delay is considered (that is, after data sync). The rx wave train 
            # will be converted into a list, again.
            self.receiver_obj.assembleWaveTrain()

            # lib.plotBode(rx_data_list[0], filtered, time_frame, number_samples, cuttof)

            # b = signal.firwin(80, 0.5, window=('kaiser', 8))
            # # plotDebug(tx_data_list[0])
            # H = np.abs(np.fft.fft(rx_data_list[0]))
            # # H = np.fft.fft(rx_data_list[0])
            # plotDebug(H, symbols='r-')
            # w, h = signal.freqz(rx_data_list[0])
            # w = w[1:]
            # h = h[1:]
            # fig = plt.figure()
            # plt.title('Digital filter frequency response')
            # ax1 = fig.add_subplot(111)
            # plt.plot(w, 20 * np.log10(abs(h)), 'b')
            # plt.ylabel('Amplitude [dB]', color='b')
            # plt.xlabel('Frequency [rad/sample]')
            # ax2 = ax1.twinx()
            # angles = np.unwrap(np.angle(h))
            # plt.plot(w, angles, 'g')
            # plt.ylabel('Angle (radians)', color='g')
            # plt.grid()
            # plt.axis('tight')
            # plt.show()
            
            ###########################################################################
            # >>>>>>>>>> CALCULATES PHOTOCURRENTS, DEPENDING ON THE DETECTORS
            
            # Calculates the photocurrents, provided by the detectors
            # This provides an 'analog' voltage, with time equal to 2*Global.number_of_points
            # This is because of the channel convolution, that will expand the signal due to delays
            self.receiver_obj.calculatesPhotocurrent()
            
            ###########################################################################
            # >>>>>>>>>> CALCULATES THE OUTPUT VOLTAGE
            
            # Calculates the output voltage.
            # Here is where the current signal is sampled on the input clock sample frequency
            self.receiver_obj.calculatesOutVoltage()
            
            ###########################################################################
            # >>>>>>>>>> APPLY ADC ON RX_DATA, CONVERTING FROM ANALOG TO DIGITAL
            
            ## TODO ---- ADD HERE THE REMOVAL OF THE DC VALUE OF DCO-OFDM DEMODULATION  (VOLTAGE DOMAIN)

            # Applies ADC. Passes sample frequency used on Modulator (TODO -- CHECK THIS VALUE FOR EACH)
            self.receiver_obj.applyADC(sample_freq = self.modulator_obj.getSampleFrequency())
            # self.receiver_obj.applyADC(sample_freq = Global.N_FFT/Global.time_frame)

            # # Applies Low-Pass Filter
            # self.receiver_obj.applyFilter(
            #     filter_order = 20,
            #     # cuttof = 400e6,
            #     # cuttof = Global.simul_frequency*(0.3),
            #     cuttof = Global.simul_frequency*(0.49),
            #     filter_type = 'low'
            # )
            
            
            ###########################################################################
            # >>>>>>>>>> GET ADC RX_DATA TO PASS FOR DE-MODULATOR
            
            self.modulator_obj.setRxDataList(
                self.receiver_obj.getAdcRxDataList()
            )
            self.modulator_obj.setRxTime(
                self.receiver_obj.getSampledWaveTime()
            )
            
            ###########################################################################
            # >>>>>>>>>> SET THE ACTUAL CHANNEL RESPONSE, FOR FURTHER COMPARISSONS
            
            # Sets the list of channel responses, for further comparissons with estimated ones
            self.modulator_obj.setListOfChannelResponses(
                self.channel_obj.getChannelResponse()
            )
            
            ###########################################################################
            # >>>>>>>>>> APPLY DE-MODULATION GIVEN TYPE CHOOSEN BEFORE (EX: OFDM)
            
            # Applies the modulation, with modulation object just created
            self.modulator_obj.applyDeModulation()
            
            ###########################################################################
            # >>>>>>>>>> RETRIEVE RX DATA
            
            # Get the received frame message
            curr_rx_frame = self.modulator_obj.getRxBitstreamFrame()
            
            # handle = plt.figure(figsize=(8,2))
            # lib.plotTxRxDataList(curr_rx_frame, 'TEST', handle, self.sync_obj, show = True)
            
            # if self.DEBUG:
            #     print(f'curr_rx_frame = {curr_rx_frame}')
            #     pass
            
            # Append current rx frame
            rx_frames.append(curr_rx_frame)
            
            # pp(self.receiver_obj)
        
        ###########################################################################
        # >>>>>>>>>> SET RECOVERED BITSTREAM TO MESSAGE OBJECT
        
        self.message_obj.setRxBitstreamFrames(rx_frames)
        
        
        ###########################################################################
        # >>>>>>>>>> CREATE MERIT FUNCTION OBJECT
        
        # Merit Funcions object
        self.merit_functions_obj = MeritFunctions(
            sync_obj = self.sync_obj
        )
        
        
        ###########################################################################
        # >>>>>>>>>> GET < BER > FOR EACH FRAME
        print()
        print()
        print()
        
        # print BER
        self.BER, self.NBER = self.merit_functions_obj.calculateBER(
            self.message_obj.getBitstreamFrames(),
            self.message_obj.getRxBitstreamFrames()
        )
        
        self.sync_obj.appendToMessageDict("BER", self.BER)
        self.sync_obj.appendToMessageDict("NBER", self.NBER)
        
        
        ###########################################################################
        # >>>>>>>>>> SHOW RX AND TX VALUES
        
        if self.DEBUG:
            pass
            
        self.message_obj.compareMessages(
            Global.input_info["data"],
            self.message_obj.BitstreamToMessage()
        )
        
        # Add input and received info to message dictionary
        self.sync_obj.appendToMessageDict("tx_info", Global.input_info["data"])
        self.sync_obj.appendToMessageDict("rx_info", self.message_obj.BitstreamToMessage())
        self.sync_obj.appendToMessageDict("n_bits", \
            [len(stream) for stream in self.message_obj.getBitstreamFrames()])
        
        
        
        ###########################################################################
        # >>>>>>>>>> PRINTS FULL SIMUL PATH, FOR DEBUG
        
        if self.DEBUG:
            # Prints full simulation path
            print(self.sync_obj.showSimulationPath())
            self.total_time = timer() - self.start_timer
            print(f"\nTotal execution time was << {self.total_time} >> seconds.\n")
            
        # ,
        #     self.message_obj.getRxBitstreamFrames()
        print(self.sync_obj.showMessageDict())

    @sync_track
    def getBER(self):
        """Returns value of self.BER"""
        
        return self.BER

    @sync_track
    def setBER(self, BER):
        """Set new value for self.BER"""
        
        self.BER = BER
    
    @sync_track
    def getNBER(self):
        """Returns value of self.NBER"""
        
        return self.NBER

    @sync_track
    def setNBER(self, NBER):
        """Set new value for self.NBER"""
        
        self.NBER = NBER

    @sync_track
    def getMessageObj(self):
        """Returns value of self.message_obj"""
        
        return self.message_obj

    @sync_track
    def setMessageObj(self, message_obj):
        """Set new value for self.message_obj"""
        
        self.message_obj = message_obj

    @sync_track
    def getMappingObj(self):
        """Returns value of self.mapping_obj"""
        
        return self.mapping_obj

    @sync_track
    def setMappingObj(self, mapping_obj):
        """Set new value for self.mapping_obj"""
        
        self.mapping_obj = mapping_obj

    @sync_track
    def getModulatorObj(self):
        """Returns value of self.modulator_obj"""
        
        return self.modulator_obj

    @sync_track
    def setModulatorObj(self, modulator_obj):
        """Set new value for self.modulator_obj"""
        
        self.modulator_obj = modulator_obj

    @sync_track
    def getTransmitterObj(self):
        """Returns value of self.transmitter_obj"""
        
        return self.transmitter_obj

    @sync_track
    def setTransmitterObj(self, transmitter_obj):
        """Set new value for self.transmitter_obj"""
        
        self.transmitter_obj = transmitter_obj

    @sync_track
    def getChannelObj(self):
        """Returns value of self.channel_obj"""
        
        return self.channel_obj

    @sync_track
    def setChannelObj(self, channel_obj):
        """Set new value for self.channel_obj"""
        
        self.channel_obj = channel_obj

    @sync_track
    def getReceiverObj(self):
        """Returns value of self.receiver_obj"""
        
        return self.receiver_obj

    @sync_track
    def setReceiverObj(self, receiver_obj):
        """Set new value for self.receiver_obj"""
        
        self.receiver_obj = receiver_obj

    @sync_track
    def getMeritFunctionsObj(self):
        """Returns value of self.merit_functions_obj"""
        
        return self.merit_functions_obj

    @sync_track
    def setMeritFunctionsObj(self, merit_functions_obj):
        """Set new value for self.merit_functions_obj"""
        
        self.merit_functions_obj = merit_functions_obj
    
    
# if __name__ == "__main__":
    
#     print("Starting VLC Simulator...")
    
#     vlc_obj = VLC()
    