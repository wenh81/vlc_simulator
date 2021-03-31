from .common_imports import *


class VLC(object):
    
    @timer_dec
    def __init__(self):
        """Constructor"""
        
        self.DEBUG = Global.DEBUG["VLC"] or Global.DEBUG["all"]
        
        self.PLOT = Global.PLOT["VLC"] or Global.PLOT["all"]

        # Indicates if using IM/DD or not
        self.IM_DD = None
        
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
        # >>>>>>>>>> CLEAN LOG FILE

        try:
            os.remove(Global.log_results)
        except:
            pass

        ###########################################################################
        # >>>>>>>>>> CREATE MESSAGE OBJECT
        
        # Creates message object.
        self.message_obj = Message(
            # input_info=Global.input_info, ### this should be now inside 'seq_config' 
            n_frames=1, ## Use number of frames == 1. Should transmit only one payload (per burst)
            # n_frames=len(Global.input_info["data"]),
            seq_config = Global.burst_config, ### NEW: has all the information regarding the TX sequence configuration (what is being transmitted, and when)
            sync_obj = self.sync_obj
        )
        
        if self.DEBUG:
            print(self.message_obj.getInputInfo())
            pass
        
        ###########################################################################
        # >>>>>>>>>> CONVERT MESSAGES TO LIST OF BITSTREAMS
            
        # # Converts it from its original type to a stream of bits (stored in bitstream_frames)
        # self.message_obj.convertsToBitstream() ---- This is now called from within 'decodeBurstSequence'
        
        # Decode the input sequence for Tx.
        self.decoded_sequence = self.message_obj.decodeBurstSequence()
        # printDebug(self.decoded_sequence)
        
        ###########################################################################
        # >>>>>>>>>> FOR EACH MESSAGE, ITERATE THROUGH ITS BITSTREAM FROM TRANSMITTER UP TO RECEIVER
        
        # APPLY MULTIPROCESS ON THESE LOOP...
        # For loop for each frame bitstream (each information to be sent in Global.input_info)
        # for curr_frame in self.message_obj.getBitstreamFrames():

        ### TODO -- Remove the various 'frames'. At this level, we should only care about one tx burst.

        # for curr_frame in self.message_obj.getBitstreamFrames():
        for seq_idx in self.decoded_sequence['seq_idx']:

            # 'seq_idx' selects all correct config for current TX symbol:
            # modulation and mapping types, symbol duration

            printDebug(self.decoded_sequence['seq'][seq_idx])
            
            # Start number of packets
            self.sync_obj.appendToMessageDict("packets", 0)
            
            ###########################################################################
            # >>>>>>>>>> FOR THAT BITSTREAM, STARTS MODULATION, GIVEN MODULATION CONFIG
            
            # Modulator object.
            self.modulator_obj = Modulator(
                is_sync=self.decoded_sequence['seq_sync'][seq_idx],
                bitstream_frame=self.decoded_sequence['seq_data'][seq_idx],
                modulation_config=Global.modulation_config[self.decoded_sequence['seq_mod'][seq_idx]],
                mapping_config=Global.mapping_config[self.decoded_sequence['seq_map'][seq_idx]],
                mapping_pilot_config=Global.mapping_config[self.decoded_sequence['seq_pilot_map'][seq_idx]],
                symbol_duration=self.decoded_sequence['seq_duration'][seq_idx],
                sync_obj = self.sync_obj
            )
            
            ###########################################################################
            # >>>>>>>>>> CREATES MODULATION OBJECT, DEPENDING ON THE TYPE (EX: OFDM)
            
            # Creates the modulator object, depending on the 'modulation_type' in 'modulation_config'
            self.modulator_obj.createModulator()
            
            ###########################################################################
            # >>>>>>>>>> APPLY MODULATION GIVEN CHOOSEN TYPE (EX: OFDM)
            
            # Applies the modulation, with modulation object just created
            self.modulator_obj.applyModulation(
                decoded_sequence = self.decoded_sequence, ## get whole sequence
                seq_idx = seq_idx, ## and at which index we are now
            )
            
            ###########################################################################
            # >>>>>>>>>> GET THE LIST OF DATA TO BE TRANSMITTED, AFTER MODULATION
            # >>>>>>>>>> DEPENDING ON TRANSMITTER THROUGHPUT, MORE THAN ONE TX_DATA
            # >>>>>>>>>> IS NEEDED
            
            # Return a list of symbols to be transmitted.
            # This list is defined by the throughput of the modulator
            self.tx_data_list = self.modulator_obj.getTxDataList()

            # Add sample frequency do decode seq
            self.decoded_sequence['seq_sample_freq'].append(self.modulator_obj.getSampleFrequency())
            
            
            ###########################################################################
            # >>>>>>>>>> STARTS TRANSMITTER, GIVEN CONFIG
            
            # Transmitter object.
            self.transmitter_obj = Transmitter(
                transmitter_config = Global.transmitter_config,
                tx_data_list = self.tx_data_list,
                sync_obj = self.sync_obj
            )
            
            ###########################################################################
            # >>>>>>>>>> APPLY DAC ON TX_DATA, CONVERTING TO ANALOG. CAN BE 
            # >>>>>>>>>> BYPASSED BY Global.bypass_dict["DAC"]
            
            # Get modulation config, to check for further required actions on DAC
            modulation_config = Global.modulation_config[self.decoded_sequence['seq_mod'][seq_idx]]
            # default values before checking
            offset_value = 0
            
            
            # check if intensity modulation / direct detection
            if self.IM_DD is None:
                self.IM_DD = modulation_config["IM_DD"]
            elif self.IM_DD != modulation_config["IM_DD"]:
                raise ValueError(f"\n\n***Error --> Not allowed to use modulation configs with both IM_DD < {self.IM_DD} > and < {modulation_config['IM_DD']} >. Choose one!\n")

            try:
                OFDM_type = next(iter(modulation_config["ofdm_type"].keys()))
                if OFDM_type == "DCO-OFDM":
                    # get DCO-OFDM DC value
                    offset_value = modulation_config["ofdm_type"][OFDM_type][0]
            except:
                pass
            
            # Apply additional bias to LED if on IM/DD mode
            if self.IM_DD:
                offset_value += Global.tx_voltage_bias_add

            # Applies DAC:
            # Optional: Offset value will be applied AFTER DAC conversion, in analog domain
            # Optional: If IM_DD, make sure only non-negative values
            self.transmitter_obj.applyDAC(
                offset_value = offset_value,
                IM_DD = self.IM_DD,
                time_interval = self.decoded_sequence['seq_duration'][seq_idx]
            )
            
            ## TODO ---- MUST APPLY THE RECONSTRUCTION FILTER (if using zero-holder)
            
            # # Applies Low-Pass Filter
            # self.transmitter_obj.applyFilter(
            #     filter_order = 20,
            #     # cuttof = 400e6,
            #     # cuttof = Global.simul_frequency*(0.3),
            #     cuttof = Global.simul_frequency*(0.49),
            #     filter_type = 'low'
            # )


            ###########################################################################
            # >>>>>>>>>> CALCULATES OPTICAL POWER, DEPENDING ON THE LIGHTSOURCES
            # >>>>>>>>>> OR CAN BE BYPASSED BY Global.bypass_dict["LightSource"]
            
            # Calculates the optical power provided by the light sources
            self.transmitter_obj.calculatesOpticalPower()
            
            # Gets the list of optical powers to be transmitted
            tx_data_list = self.transmitter_obj.getTxOpticalOutList()
            
            # Get tx data list assembled into a single tx_wave
            tx_wave, tx_time = lib.assembleWaveListSameInterval(
                signal_list = tx_data_list,
                time_interval = self.decoded_sequence['seq_duration'][seq_idx],
                time_step = Global.time_step
            )
            
            # Store tx wave info for latter sync attempt at receiver end
            self.decoded_sequence['tx_wave_list'].append(tx_wave)
            self.decoded_sequence['tx_time_list'].append(tx_time)
            self.decoded_sequence['tx_num_symbols'].append(len(tx_data_list))

            # Store end time for tx wave for latter sync attempt at receiver end
            if self.decoded_sequence['seq_end_time'] != []:
                self.decoded_sequence['seq_end_time'].append(
                    len(tx_data_list)*self.decoded_sequence['seq_duration'][seq_idx] + \
                        self.decoded_sequence['seq_end_time'][-1]
                )
            else:
                self.decoded_sequence['seq_end_time'].append(len(tx_data_list)*self.decoded_sequence['seq_duration'][seq_idx])
            
            # Store start time for tx wave for latter sync attempt at receiver end
            if self.decoded_sequence['seq_start_time'] != []:
                self.decoded_sequence['seq_start_time'].append(
                        self.decoded_sequence['seq_end_time'][-2]
                )
            else:
                self.decoded_sequence['seq_start_time'].append(0)

            # printDebug(tx_wave)
            # plotDebug(tx_wave, tx_time, symbols='ro-')
            # printDebug()
        
        # Get tx data list assembled into a single tx_wave
        burst_tx_wave, burst_tx_time = lib.assembleWaveListDifferentIntervals(
            signal_list = self.decoded_sequence['tx_wave_list'],
            time_interval_list = self.decoded_sequence['seq_duration'],
            num_symbols = self.decoded_sequence['tx_num_symbols'],
            time_step = Global.time_step
        )

        # plotDebug(burst_tx_wave, burst_tx_time, symbols='b-')
        # printDebug()


        ###########################################################################
        # >>>>>>>>>> RETRIEVE TX_DATA LIST FOR THE CHANNEL
        
        
        # # Creates global full time vector with Global.time_frame * (number of symbols in current frame)
        # Global.full_time_vector = [np.arange(0, Global.number_of_points)*Global.time_step \
        #     + idx*Global.time_frame \
        #         for idx in range(len(tx_data_list))]


        tx_data_list = list(burst_tx_wave) ## TODO --- NEEDED?
        
        self.PLOT = True

        if self.PLOT:
            handle = plt.figure(figsize=(8,2))
            # lib.plotTxRxDataList(tx_data_list, Global.full_time_vector, 'TX DATA', handle, self.sync_obj, show = False)
            # printDebug(Global.full_time_vector)
            ################## lib.plotTxRxDataList(tx_data_list, Global.full_time_vector, 'TX DATA', handle, self.sync_obj, show = False)
            plotDebug(burst_tx_wave, burst_tx_time, symbols='b-', label = "TX DATA", hold=True)
        
        
        ###########################################################################
        # >>>>>>>>>> CREATES CHANNEL GIVEN INPUT TX_DATA LIST
        
        # Channel object
        self.channel_obj = Channel(
            tx_data = burst_tx_wave,
            tx_data_time = burst_tx_time,
            time_step = Global.time_step,
            IM_DD = self.IM_DD,
            channel_SNR = Global.rx_SNR_dB,
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
                # set fake channel impulse response from input (defined globaly here)
                ## get minimum time duration among the input symbols for better performance
                self.channel_obj.definesChannelResponse(
                    channel_list = Global.list_of_channel_response,
                    time_duration = np.min(self.decoded_sequence['seq_duration'])
                )
                # # Set single channel response (list of 1 position) ....
                # self.channel_obj.setChannelResponse(Global.list_of_channel_response)
        
        ###########################################################################
        # >>>>>>>>>> APPLY EACH CIR (FOR EACH LIGHTSOURCE) TO EACH TX_DATA.
        
        # After channel reponse set, apply it to each lamp. Do with time domain "convolution" or in "frequency domain"
        self.channel_obj.applyChannelResponse(do_convolution = True)
        # self.channel_obj.applyChannelResponse(do_convolution = False)

        
        ###########################################################################
        # >>>>>>>>>> GET RX_DATA LIST CONVOLVED BY CHANNEL AFTER ADDING NOISE.
        
        # Gets the list of optical powers at the receiver, after convolution on channel response, and noise addition.
        rx_data_list = self.channel_obj.getRxDataOut()
        rx_time = self.channel_obj.getRxTime() ## old Global.full_time_vector

        # # Re-calculates full time vector, after convolution
        # # Creates global full time vector with Global.time_frame * (number of symbols in current frame)
        # Global.full_time_vector = [np.arange(0, len(rx_data_list[idx]))*Global.time_step \
        #     + idx*Global.time_frame \
        #         for idx in range(len(rx_data_list))]
        
        if self.PLOT:
            # printDebug(rx_data_list)
            # plotDebug(tx_data_list[0], Global.full_time_vector[0], symbols='ro-')
            # plotDebug(tx_data_list[1], Global.full_time_vector[1], symbols='ro-')
            # plotDebug(rx_data_list[0], Global.full_time_vector[0], symbols='ro-')
            # plotDebug(rx_data_list[1], Global.full_time_vector[1], symbols='ro-')
            plotDebug(rx_data_list[0], rx_time, symbols='r-', label = "RX DATA", hold=False)

            # lib.plotTxRxDataList(rx_data_list, 'RX DATA', handle, self.sync_obj, show = True)
        

        # printDebug(rx_data_list)
        # plotDebug(rx_data_list[0], rx_time)


        
        ## TODO --- NEW FOR HERE?... CHECK HOW TO DECODE DATA...TRY TO DECODE FIELD BY FIELD?
        # for seq_idx in self.decoded_sequence['seq_idx']:
        
        
        ## TODO --- temp fix: rx is a list now
        
        # Reset IM/DD variable. Resets before the 'for', b/c it should be the same for all PDs below.
        self.IM_DD = None

        # Get the sample frequency defined so far
        sample_frequency = self.modulator_obj.getSampleFrequency()
        
        # Each tx [led] convolves with channel [pd x led], producing rx [pd].
        # get the rx_data wave for each receiver.
        for rx_data_pd in rx_data_list:
            
            # # printDebug(rx_data_pd)
            # plotDebug(rx_data_pd, rx_time)
            # plotDebug(rx_data_pd, rx_time, symbols="bo-")
            
            # Start the index to know where on the sequence we are, for each rx_data.
            # The trick here is that the for each rx_data, we have all phases of the modulation sequence.
            # And since they may come from different channel responses, delays may be different, etc.
            # So, should try to decode the sequence for EACH rx_data_pd.
            # The 'seq_idx' is the ID that controls where in the sequence we are, and should go from 0 to max 
            # during this 'for' loop. As long as it progresses, we increment 'seq_idx', and reset when loops back.
            seq_idx = 0


            ###########################################################################
            # >>>>>>>>>> STARTS RECEIVER, GIVEN CONFIG
            # Receiver object.
            self.receiver_obj = Receiver(
                receiver_config = Global.receiver_config,
                roic_config = Global.roic_config, # read-out integrated circuit config for that rx
                rx_data = rx_data_pd,
                rx_time = rx_time,
                sample_freq = sample_frequency,
                sample_phase = 0, ## TODO -- MUST BE APPLIED
                sync_obj = self.sync_obj
            )

            # while(seq_idx != MAX???):
            

            # lib.plotBode(rx_data_list[0], filtered, time_frame, number_samples, cuttof)

            
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
            
            # Until now, the 'seq_idx' index wasn't anaylsed, since we are converting from optical to voltage domain.
            # Now, we need info to know what kind of modulation is the first one, so we know if have to add any DC bias.
            # If DCO-OFDM, then all other parts of the sequence should have the same OFDM type, and getting first position is 
            # enough to know we need to add DC for whole wave.

            # Get modulation config
            modulation_config = Global.modulation_config[self.decoded_sequence['seq_mod'][seq_idx]]
            
            # default values before checking
            offset_value = 0
            
            # check if intensity modulation / direct detection
            if self.IM_DD is None:
                self.IM_DD = modulation_config["IM_DD"]
            try:
                OFDM_type = next(iter(modulation_config["ofdm_type"].keys()))
                if OFDM_type == "DCO-OFDM":
                    # Get DCO-OFDM DC value
                    offset_value = modulation_config["ofdm_type"][OFDM_type][0]
            except:
                pass

            # Subtract bias to voltege from the ROIC, if on IM/DD mode
            if self.IM_DD:
                offset_value -= Global.rx_voltage_bias_subtract

            # Applies ADC:
            # Passes sample frequency used on Modulator (TODO -- CHECK THIS VALUE FOR EACH)
            self.receiver_obj.applyADC(
                # sample_freq = self.modulator_obj.getSampleFrequency(),
                offset_value = offset_value
                # IM_DD = self.IM_DD
                # time_interval = self.decoded_sequence['seq_duration'][seq_idx],
            )

            # self.receiver_obj.applyADC(sample_freq = Global.N_FFT/Global.time_frame)

            # plotDebug(self.receiver_obj.adc_rx_data_list, symbols='ro-')
            # old = self.receiver_obj.adc_rx_data_list

            # # After sampling, apply digital filter
            # # Applies Low-Pass Filter
            # self.receiver_obj.applyFilter(
            #     filter_order = 20,
            #     # cuttof = 400e6,
            #     # cuttof = Global.simul_frequency*(0.3),
            #     # cuttof = Global.simul_frequency*(0.49),
            #     cuttof = 1e4,
            #     # cuttof = (1/Global.time_frame)*(0.5),
            #     filter_type = 'hp'
            # )

            # plotDebug(self.receiver_obj.adc_rx_data_list, symbols='ro-')
            # plotDebug(self.receiver_obj.adc_rx_data_list - old, symbols='ro-')
            # # Applies High-Pass Filter
            # self.receiver_obj.applyFilter(
            #     filter_order = 20,
            #     # cuttof = 400e6,
            #     # cuttof = Global.simul_frequency*(0.3),
            #     cuttof = 1/Global.time_frame,
            #     filter_type = 'hp'
            # )

            # plotDebug(self.receiver_obj.getAdcRxDataList().imag)

            # Starts the rx_data as NOT-synced
            self.rx_data_synced = False

            # Start delay steps and time variables
            self.delay_time = 0
            self.delay_steps = 0

            printDebug(self.decoded_sequence)
            # From here, we have the full wave, already sampled. Now, need to debug.
            # 'seq_idx' starts with 0. Then increments from here, as long as we progress on the sequence.
            # for seq_idx in range(0, len(self.decoded_sequence['seq_data'])):
            while seq_idx < len(self.decoded_sequence['seq']):
                # Current Sequence ID
                print(f"**********************************************************************************\n\
Starting sequence for field < {self.decoded_sequence['seq'][seq_idx].split('.')[0]} > and subfield < {self.decoded_sequence['seq'][seq_idx].split('.')[1]} >\n\
**********************************************************************************\n")

                # Re-create Modulator object, for the DeModulation, for each sequence step.
                self.modulator_obj = Modulator(
                    is_sync=self.decoded_sequence['seq_sync'][seq_idx],
                    bitstream_frame=self.decoded_sequence['seq_data'][seq_idx],
                    modulation_config=Global.modulation_config[self.decoded_sequence['seq_mod'][seq_idx]],
                    mapping_config=Global.mapping_config[self.decoded_sequence['seq_map'][seq_idx]],
                    mapping_pilot_config=Global.mapping_config[self.decoded_sequence['seq_pilot_map'][seq_idx]],
                    symbol_duration=self.decoded_sequence['seq_duration'][seq_idx],
                    sync_obj = self.sync_obj
                )

                # Re-create the modulator.
                self.modulator_obj.createModulator()

                # Re-set the sample frequency, for new modulator object.
                self.modulator_obj.setSampleFrequency(sample_frequency)
                
                ###########################################################################
                # >>>>>>>>>> GET ADC RX_DATA TO PASS FOR DE-MODULATOR
                
                # Set the rx_data and rx_time to modulator.
                self.modulator_obj.setRxData(
                    self.receiver_obj.getSampledWave()
                )
                self.modulator_obj.setRxTime(
                    self.receiver_obj.getSampledWaveTime()
                )

                # plotDebug(self.receiver_obj.getSampledWave(), self.receiver_obj.getSampledWaveTime(), symbols='ro-')

                # # # TODO ----- check if can del receiver object already...
                # del self.receiver_obj

                # # TODO ----- FROM HERE, WE HAVE THE WHOLE SAMPLED WAVE FOR A GIVEN RX. NEED TO DECODE THE WHOLE SEQUENCE NOW.
                
                ###########################################################################
                # >>>>>>>>>> SET THE ACTUAL CHANNEL RESPONSE, FOR FURTHER COMPARISSONS
                
                # Sets the list of channel responses, for further comparissons with estimated ones
                self.modulator_obj.setListOfChannelResponses(
                    self.channel_obj.getChannelResponse()
                )
                
                ###########################################################################
                # >>>>>>>>>> APPLY DE-MODULATION GIVEN TYPE CHOOSEN BEFORE (EX: OFDM)
                
                # Check how to do the demodulation, first on the remove group delay (need to use/check for the FLP method...)
                
                # Applies the modulation, with modulation object just created.
                # If on the 'sync' step, apply the synchronization first.
                self.rx_data_synced, self.delay_time, self.delay_steps = self.modulator_obj.applyDeModulation(
                    decoded_sequence = self.decoded_sequence, ## get whole sequence
                    seq_idx = seq_idx, ## and at which index we are now
                    rx_data_synced = self.rx_data_synced, ## get if data is sync or not
                    delay_time = self.delay_time, ## get delay in time
                    delay_steps = self.delay_steps ## get delay in steps
                )
                
                printDebug(self.delay_time)
                # Check if current sequence step is for 'sync' or for data.
                # if self.decoded_sequence['rx_data'][seq_idx] != 'sync':
                if 'sync' in self.decoded_sequence['rx_data'][seq_idx]:

                    separators = ''.join(30*['##'])

                    pretty_diff = f"""{separators}
ID for current sequence step: < {self.decoded_sequence['seq'][seq_idx]} >
Sync data, with found delay of:
    {self.delay_time} seconds
    or
    {self.delay_time*1e6} us
    or
    {self.delay_time*1e9} ns

"""
                    # Write to log file
                    with open(Global.log_results, "a") as results:
                        results.write(pretty_diff)

                elif 'sync' not in self.decoded_sequence['rx_data'][seq_idx]:

                    ###########################################################################
                    # >>>>>>>>>> RETRIEVE RX DATA
                    
                    # Get the received frame message
                    curr_rx_frame = self.modulator_obj.getRxBitstreamFrame()

                    # printDebug(curr_rx_frame)
                    
                    # handle = plt.figure(figsize=(8,2))
                    # lib.plotTxRxDataList(curr_rx_frame, 'TEST', handle, self.sync_obj, show = True)
                    
                    # if self.DEBUG:
                    #     print(f'curr_rx_frame = {curr_rx_frame}')
                    #     pass
                    
                    # Append current rx frame
                    # rx_frames.append(curr_rx_frame)
                    
                    # pp(self.receiver_obj)

                    ###########################################################################
                    # >>>>>>>>>> SET RECOVERED BITSTREAM TO MESSAGE OBJECT
                    
                    self.message_obj.setRxBitstreamFrames(curr_rx_frame)

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

                    # printDebug(self.decoded_sequence['seq_data'][seq_idx])
                    # printDebug(self.message_obj.getRxBitstreamFrames())
                    
                    # print BER
                    self.BER, self.NBER, self.pretty_diff = self.merit_functions_obj.calculateBER(
                        self.decoded_sequence['seq_data'][seq_idx],
                        self.message_obj.getRxBitstreamFrames()
                    )
                    
                    self.sync_obj.appendToMessageDict("BER", self.BER)
                    self.sync_obj.appendToMessageDict("NBER", self.NBER)
                    

                    ###########################################################################
                    # >>>>>>>>>> SHOW RX AND TX VALUES
                    
                    binary_rx_data = self.message_obj.BitstreamToMessage(
                        tx_data = self.decoded_sequence['seq_data'][seq_idx],
                        rx_data = curr_rx_frame,
                        bitstream_type = self.decoded_sequence['seq_data_type'][seq_idx]
                    )

                    if self.DEBUG:
                        pass
                        
                    self.message_obj.compareMessages(
                        seq_id = self.decoded_sequence['seq'][seq_idx],
                        tx_data = self.decoded_sequence['seq_data'][seq_idx],
                        rx_data = binary_rx_data,
                        pretty_diff = self.pretty_diff
                    )
                    
                    # Add input and received info to message dictionary
                    self.sync_obj.appendToMessageDict("tx_info", self.decoded_sequence['seq_data'][seq_idx])
                    self.sync_obj.appendToMessageDict("rx_info", binary_rx_data)
                    self.sync_obj.appendToMessageDict("n_bits", \
                        [len(stream) for stream in self.message_obj.getBitstreamFrames()])
                
                # Goes to next step on the sequence
                seq_idx += 1
        
        
        # Write to log file the decoded_sequence
        with open(Global.log_results, "a") as results:
            
            json_str = ''.join(30*['##']) + '\n'
            
            for seq_step in self.decoded_sequence.keys():
                if seq_step not in ["seq_all_mapped_info", "tx_time_list", "tx_wave_list", "seq_func_rx", "seq_func_tx"]:
                    json_str += f"## {seq_step} ##\n"
                    for data in self.decoded_sequence[seq_step]:
                        json_str += f"\t< {data} >\n"
            results.write(json_str)

        # printDebug(self.decoded_sequence['rx_data'])
        # # starts empty list with all received frames
        # rx_frames = self.decoded_sequence['rx_data']


        # self.message_obj.convertBackSequence

        # ###########################################################################
        # # >>>>>>>>>> SET RECOVERED BITSTREAM TO MESSAGE OBJECT
        
        # self.message_obj.setRxBitstreamFrames(rx_frames)
        
        
        # ###########################################################################
        # # >>>>>>>>>> CREATE MERIT FUNCTION OBJECT
        
        # # Merit Funcions object
        # self.merit_functions_obj = MeritFunctions(
        #     sync_obj = self.sync_obj
        # )
        
        
        # ###########################################################################
        # # >>>>>>>>>> GET < BER > FOR EACH FRAME
        # print()
        # print()
        # print()
        
        # # print BER
        # self.BER, self.NBER = self.merit_functions_obj.calculateBER(
        #     self.message_obj.getBitstreamFrames(),
        #     self.message_obj.getRxBitstreamFrames()
        # )
        
        # self.sync_obj.appendToMessageDict("BER", self.BER)
        # self.sync_obj.appendToMessageDict("NBER", self.NBER)
        
        
        # ###########################################################################
        # # >>>>>>>>>> SHOW RX AND TX VALUES
        
        # if self.DEBUG:
        #     pass
            
        # self.message_obj.compareMessages(
        #     Global.input_info["data"],
        #     self.message_obj.BitstreamToMessage()
        # )
        
        # # Add input and received info to message dictionary
        # self.sync_obj.appendToMessageDict("tx_info", Global.input_info["data"])
        # self.sync_obj.appendToMessageDict("rx_info", self.message_obj.BitstreamToMessage())
        # self.sync_obj.appendToMessageDict("n_bits", \
        #     [len(stream) for stream in self.message_obj.getBitstreamFrames()])
        
        
        
        ###########################################################################
        # >>>>>>>>>> PRINTS FULL SIMUL PATH, FOR DEBUG
        
        if self.DEBUG and False:
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
    