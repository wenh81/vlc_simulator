####################################
####### General Library file #######
####################################

from .common_imports import *


# import pycuda.autoinit
# import pycuda.gpuarray as gpuarray
# ONLY FOR LINUX
# import skcuda.fft as cu_fft

def sampleSignal(signal, time, sample_frequency):
    """Apply sampling on given signal."""

    sampled_wave_time = []
    sampled_wave = []
    next_sample = 0
    
    # time interval between samples
    delta_t = 1/sample_frequency
    
    ## TODO -- maybe should interpolate first? .... 
    ## TODO -- Should it take the average of the signal on a given time span???

    # sample approximately on the correct timing
    for idx,time in enumerate(time):
        if time >= next_sample:
            next_sample += delta_t
            sampled_wave_time.append(time)
            sampled_wave.append(signal[idx])
            
    sampled_wave_time = np.array(sampled_wave_time)
    sampled_wave = np.array(sampled_wave)
    return sampled_wave, sampled_wave_time

def assembleWaveListSameInterval(signal_list, time_interval, time_step):
    """Given list of signals, concatenate them on a single np array, provided they have the same duration on each wave on list, and time step defining distance between points in each wave."""

    # variable to shift data right, for each time frame passed
    shift = 0
    
    number_of_points = int(time_interval/time_step)
    # all_zeros = np.zeros((1+len(signal_list))*number_of_points)
    all_zeros = np.zeros(len(signal_list)*number_of_points)
    out_wave_train = all_zeros.copy()*(0+0j)

    for data in signal_list:
        # starts vector with all zeros plus actual data
        new_data = sumVectosDiffSizes(all_zeros.copy()*(0+0j), data)
        
        new_data = np.roll(new_data, (shift)*number_of_points)
        shift += 1


        out_wave_train = sumVectosDiffSizes(out_wave_train, new_data)
        out_wave_time = np.arange(0, len(out_wave_train))*time_step
    
    return out_wave_train, out_wave_time

def assembleWaveListDifferentIntervals(signal_list, time_interval_list, num_symbols, time_step):
    """Given list of signals, list of time intervals for each symbol, and number of symbol for each, concatenate them on a single np array, given the same time step defining distance between points in each wave."""
    
    total_duration = np.sum([sym_duration*num_symbols[idx] for idx, sym_duration in enumerate(time_interval_list)])
    # total_duration = np.sum(time_interval_list)
    total_number_of_points = int(total_duration/time_step)
    all_zeros = np.zeros(total_number_of_points)

    printDebug(total_duration)

    out_wave = all_zeros.copy()*(0+0j)
    
    number_of_points = 0
    for idx,data in enumerate(signal_list):

        # starts vector with all zeros plus actual data
        new_data = sumVectosDiffSizes(all_zeros.copy()*(0+0j), data)
        
        # plotDebug(new_data, np.arange(0, len(new_data))*time_step)
        new_data = np.roll(new_data, number_of_points)
        # plotDebug(new_data, np.arange(0, len(new_data))*time_step)

        # current data number of points
        number_of_points += int(time_interval_list[idx]*num_symbols[idx]/time_step)

        out_wave = sumVectosDiffSizes(out_wave, new_data)
        out_wave_time = np.arange(0, len(out_wave))*time_step
    
    return out_wave, out_wave_time

def butterFilter(data, cuttof, filter_order = 20, filter_type = 'low', plot = False):
    """Apply Butterworth filter."""

    DEBUG = False
    # DEBUG = True

    # nyquist frequency
    nyq = 0.5 * Global.simul_frequency

    # adjsut cuttof frequency
    if isinstance(cuttof, list):
        cuttof_nyq = []
        cuttof_nyq[0] = cuttof[0] / nyq
        cuttof_nyq[1] = cuttof[1] / nyq
    else:
        cuttof_nyq = cuttof / nyq

    # data time frame
    number_points = len(data)
    time_frame = number_points*Global.time_step

    number_samples = int(Global.simul_frequency*time_frame)
    
    t = np.linspace(0, time_frame, number_samples, False)
    
    if DEBUG:
        # For testing
        f0 = 10e6
        f1 = 40e6
        data = np.sin(2*np.pi*f0*t) + np.sin(2*np.pi*f1*t)
        # data = np.sin(2*np.pi*f0*t)
    
    if plot:
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(t, data)
        ax1.set_title('Time domain signal')
        ax1.grid()

    # Create filter
    sos = signal.butter(filter_order, cuttof_nyq, btype=filter_type, output='sos')

    # yf = fftpack.fft(data)
    # xf = np.linspace(0.0, 1.0/(2.0*time_frame), int(number_samples/2))

    # fig, ax = plt.subplots()
    # ax.plot(xf, 2.0/number_samples * np.abs(yf[:number_samples//2]))
    # plt.show()


    # filtered signal
    filtered = signal.sosfilt(sos, data)

    # get filter frequency and absolute value
    w, h = signal.sosfreqz(sos, worN=number_points)
    
    if plot:
        ax2.plot(t, filtered)
        ax2.set_title('Filtered signal.')
        # ax2.axis([0, 1, -2, 2])
        ax2.set_xlabel('Time [seconds]')
        plt.tight_layout()
        ax2.grid()
        plt.show()

        plt.semilogx((Global.simul_frequency * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))

        plt.title('Butterworth filter frequency response')
        plt.xlabel('Frequency [radians / second]')
        plt.ylabel('Amplitude [dB]')
        plt.margins(0, 0.1)
        plt.grid(which='both', axis='both')
        plt.axvline(cuttof, color='green') # cutoff frequency
        # plt.grid()
        plt.show()

        # plotBode(data, time_frame, number_samples, cuttof, data2=filtered)
        plotBode(data, t, number_samples, cuttof, data2=filtered)
    
    return filtered

def plotBode(data, time, freq_ref, data2 = None, time2 = None):

    time_frame = np.max(time)
    number_samples = len(time)
    
    """Inrerpolate data to be in conformity with time vector."""
    yf = fftpack.fft(data)
    xf = np.linspace(0.0, 1.0/(2.0*time_frame), int(number_samples/2))
    if data2 is not None:
        yf2 = fftpack.fft(data2)
        if time2 is not None:
            time_frame2 = np.max(time2)
            number_samples2 = len(time2)
        else:
            time_frame2 = time_frame
            number_samples2 = number_samples
        xf2 = np.linspace(0.0, 1.0/(2.0*time_frame2), int(number_samples2/2))
    
    # plt.semilogx((Global.simul_frequency * 1 / np.pi) * w, 20 * np.log10(abs(yf)))
    plt.semilogx(xf*0.5, 20 * np.log10(abs(2.0/number_samples * np.abs(yf[:number_samples//2]))))
    if data2 is not None:
        plt.semilogx(xf2*0.5, 20 * np.log10(abs(2.0/number_samples2 * np.abs(yf2[:number_samples2//2]))))

    plt.title('Frequency response')
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    if data2 is not None:
        plt.legend(['data1', 'data2'], fontsize=10)
    else:
        plt.legend(['data'], fontsize=10)
    # plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    printDebug(freq_ref)
    plt.axvline(freq_ref, color='green') # cutoff frequency
    plt.show()

def interpolateData(time, signal, number_of_points, kind = 'linear'):
    """Inrerpolate data to be in conformity with time vector."""
    
    kind = Global.interpolation_type
    tx_interp = interpolate.interp1d(time, signal, kind=kind, fill_value="extrapolate")

    base_time_vector = np.arange(0, number_of_points)*Global.time_step

    # printDebug(tx_interp(Global.base_time_vector))
    # plotDebug(tx_interp(Global.base_time_vector), Global.base_time_vector, symbols='b-')
    return tx_interp(base_time_vector)
    

def plotDebug(signal, time = None, label = "", symbols='r-', hold = False, title = None):
    """Fast plot for debug."""

    if label == "":
        # Get function call
        function_call = inspect.stack()[1][-2][0].strip()
        # Extract function name
        func_name = function_call.split('(')[0]
        # Extract 
        label = function_call.split(func_name)[1].split(',')[0]
        if label[0] == '(':
            label = label[1:]
        if label[-1] == ')':
            label = label[:-1]
            # replace('(','').replace(')','').split(',')[0]
        
    if time is None:
        plt.plot(signal, symbols, label=label)
    else:
        plt.plot(time, signal, symbols, label=label)
    plt.grid(True)
    # plt.ylim(np.min(signal)*1.1, np.max(signal)*1.1)
    plt.legend(fontsize=10)
    if title is not None:
        plt.title(title)
    if not hold:
        plt.show()

def printDebug(signal = None, details = False, plot = False, stop = False, stop_message = ""):
    """Pretty debug signal print. Use details = True for more information on the object. Use stop = True to stop program after print."""

    print('\n---------------------------------------------------------------------------')

    if signal is None and stop:
        raise ValueError(f"\n\n***User called printDebug() to stop execution!\n")
    
    if signal is None:
        raise ValueError(f"\n\n***'None' signal passed to printDebug()!\n")
    
    # Get function call
    function_call = inspect.stack()[1][-2][0].strip()
    # Extract function name
    func_name = function_call.split('(')[0]
    # Extract 
    signal_name = function_call.split(func_name)[1].split(',')[0]
    if signal_name[0] == '(':
        signal_name = signal_name[1:]
    if signal_name[-1] == ')':
        signal_name = signal_name[:-1]
        # replace('(','').replace(')','').split(',')[0]
    
    print('> START <' + f"\t-->\t<{signal_name}>")
    # Actual print with value
    print(f"{type(signal)}")
    try:
        print(f"length = {len(signal)}")
    except:
        pass
    print(f"Value :\n{signal}")
    
    if details:
        print('\n>>> More details <<<\n')
        print(f">> All methods for {type(signal)}:")
        print(f"{dir(signal)}")
    
    if plot:
        plotDebug(signal, label = signal_name)

    print(f"{type(signal)}")
    try:
        print(f"length = {len(signal)}")
    except:
        pass
    print('>  END  <' + f"\t-->\t<{signal_name}>")
    print('---------------------------------------------------------------------------\n')

    if stop or stop_message != "":
        if stop_message != "":
            raise ValueError(f"\n\n***User called printDebug() to stop execution!\n")
        else:
            raise ValueError(stop_message)

def adjustRange(signal, new_max, new_min, old_max, old_min, offset):
    """Adjust signal to some new range."""
    
    # TODO --- Remove offset from here

    return (new_max - (new_min))/(old_max - old_min)\
        *(signal - old_min) + (new_min) + (offset)
    # return (new_max - (new_min + offset))/(old_max - old_min)\
    #     *(signal - old_min) + (new_min + offset)

def zeroClip(signal):
    """Returns the same signal, but clipped to zero"""
    
    return np.array([item if item >= 0 else 0 for item in signal])

def plotTxRxData(data, time, label, handle, sync_obj, show = False):
    """Plots Tx/Rx data."""
    
    sync_obj.appendToSimulationPath("plotTxRxData @ generalLibrary")
    
    # Set previous for debug
    sync_obj.setPrevious("generalLibrary")
    
    # plt.figure(figsize=(8,2))
    plt.plot(time, data, label=label)
    # plt.plot(time, data, 'bo-', label=label)
    # plt.plot((np.fft.ifft(data)), label=label)
    plt.legend(fontsize=10)
    plt.xlabel('Time'); plt.ylabel('$|x(t)|$')
    plt.grid(True)
    plt.show(show)

def removeOutliers(signal, sigma_threshold = 6, default_outlier = 0):
    """Get signal, find outliers, and remove"""

    # get std
    signal_std = np.std(signal)

    # find outliers
    outliers = abs(signal) > sigma_threshold*signal_std

    printDebug(outliers)

    # remove the outliers, settinf to default value
    signal[outliers] = default_outlier

    # get outlier positions
    outlier_positions = [index for index, out in enumerate(outliers) if out]
        

    return signal, outlier_positions

def sumVectosDiffSizes(a, b):
    """Sum vectors with different sizes: c = a + b."""

    if len(a) < len(b):
        c = b.copy()
        c[:len(a)] = c[:len(a)] + a
    else:
        c = a.copy()
        c[:len(b)] = c[:len(b)] + b
        
    return c

def mulVectosDiffSizes(a, b, shift = 0):
    """Multiply vectors with different sizes: c = a * b. Shift smaller by shift positions."""

    if len(a) < len(b):
        a = np.roll(sumVectosDiffSizes(b.copy()*0, a), shift)
        c = a*b
    else:
        b = np.roll(sumVectosDiffSizes(a.copy()*0, b), shift)
        c = a*b
        
    return c


# def plotTxRxDataList(data_list, time_list, label, handle, sync_obj, show = False):
def plotTxRxDataList(data_list, label, handle, sync_obj, show = False):
    """Plots Tx/Rx data list."""
    
    sync_obj.appendToSimulationPath("plotTxRxDataList @ generalLibrary")
    
    # Set previous for debug
    sync_obj.setPrevious("generalLibrary")
    
    shift = 0
    # concatenated_data = []
    # concatenated_data = 0
    # final_data = np.zeros((1+len(data_list))*Global.number_of_points)
    # final_data = np.zeros((1+len(data_list))*Global.number_of_points)
    all_zeros = np.zeros((1+len(data_list))*Global.number_of_points)
    final_data = all_zeros.copy()
    for data in data_list:
        # new_data = data
        # starts vector with all zeros plus actual data
        new_data = sumVectosDiffSizes(all_zeros.copy(), data)
        if shift >= 0:
            shift += 1
            new_data = np.roll(new_data, (shift-1)*Global.number_of_points)
        # elif shift > 1:
        #     # new_data = np.roll(data, Global.number_of_points)
        #     # shifts data to 
        #     shift += 1
        #     # new_data = np.roll(new_data, 100)
        #     pass
        
        # new_data = sumVectosDiffSizes(all_zeros.copy(), new_data)

        final_data = sumVectosDiffSizes(final_data, new_data)

        # concatenated_data += list(new_data)
        # # concatenated_data = concatenated_data + new_data
        printDebug(Global.number_of_points)
        # printDebug(Global.number_of_points*2)
        # # printDebug(new_data)
        # # plotDebug(new_data)
        # plotDebug(final_data)

    # interpolateData
    # plotDebug(concatenated_data)
    
    # concatenated_time = []
    # for idx,data in enumerate(data_list):
    #     concatenated_time += list(Global.base_time_vector + idx*Global.time_frame)
    
    # concatenated_data = np.array(final_data)
    # concatenated_time = np.array(concatenated_time)

    concatenated_time = np.arange(0, len(final_data))*Global.time_step
    # plotDebug(final_data, concatenated_time)
    
    # plot concatenated list
    plotTxRxData(
        data = final_data,
        time = concatenated_time,
        label = label,
        handle = handle,
        sync_obj = sync_obj,
        show = show
    )
    
def timer_dec(function):
    """Function to be used as decorator, for method timing calculations."""
    def timed_function(self, *args, **kw):
        start_time = timer()
        result = function(self, *args, **kw)
        elapsed = timer() - start_time
        print(f'>>>> Function "{function.__name__} (@ {self.__class__.__name__})" took {elapsed} seconds to complete.\n')
        
        return result
    return timed_function

def sync_track(function):
    """Function to be used as decorator, for SimulationSync object simulation path tracking."""
    def synced_function(self, *args, **kw):
        
        # curframe = inspect.currentframe()
        # calframe = inspect.getouterframes(curframe, 2)
        # # print('curframe:', curframe)
        # print('caller name:', calframe[1][3])
        
        # Get sync object
        sync_obj = self.__class__.getSyncObj(self)
        
        # If NO debug i set
        if not sync_obj.DEBUG["all"] and not sync_obj.DEBUG["SimulationSync"]:
            
            # apply function, and get result (with no DEBUG)
            result = function(self, *args, **kw)
            return result
        
        
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        # filename = module.__file__
        module_name = module.__name__
        
        
        # Set previous for debug
        sync_obj.setPrevious(f"{module_name}")
        # sync_obj.setPrevious(f"{self.__class__.__name__}")
        
        # SUPPORTS ONLY TWO NESTED DECORATORS!
        # Check if function name is one of the inner functions for decorators
        if function.__name__ in ["timed_function"]:
            # print()
            # print(function.__name__)
            # # print(frame.function)
            # print(frame.code_context)
            # print(frame.code_context[0].strip().replace("\n","").split('.')[-1])
            
            # Add function, called from within a decorator
            function_from_decorator = frame.code_context[0].strip().replace("\n","").split(".")[-1]
            sync_obj.appendToSimulationPath(f'{self.__class__.__name__}.{function_from_decorator} -- @{function.__name__}')
        
        else:
            # Add function, called from given class
            sync_obj.appendToSimulationPath(f"{self.__class__.__name__}.{function.__name__}()")
        
        
        # Set sync object
        self.__class__.setSyncObj(self, sync_obj)
        
        # # Print whole simul path
        # print(sync_obj.getSimulationPath())
        
        # apply function, and get result
        result = function(self, *args, **kw)
        
        return result
    
    return synced_function


# def for_all_methods(decorator):
#     def decorate(my_class):
#         for attribute in my_class.__dict__:
#             if attribute not in ['getSyncObj', 'setSyncObj', '__init__'] and callable(getattr(my_class, attribute)):
#                 print(attribute)
#                 # print(f"{[my_class, attribute, decorator(getattr(my_class, attribute))]}")
#                 setattr(my_class, f"self.{attribute}", decorator(getattr(my_class, attribute)))
#         return my_class
#     return decorate

# # Got from "https://www.idtools.com.au/gpu-accelerated-fft-compatible-numpy/"
# def ifft2_gpu(y, fftshift=False):
#     ''' This function produce an output that is 
#     compatible with numpy.fft.ifft2
#     The input y is a 2D complex numpy array'''
    
#     # Get the shape of the initial numpy array
#     n1, n2 = y.shape
    
#     # From numpy array to GPUarray. Take only the first n2/2+1 non redundant FFT coefficients
#     if fftshift is False:
#         y2 = np.asarray(y[:,0:n2//2 + 1], np.complex64)
#     else:
#         y2 = np.asarray(np.fft.ifftshift(y)[:,:n2//2+1], np.complex64)
#     ygpu = gpuarray.to_gpu(y2)
    
#     # Initialise empty output GPUarray 
#     x = gpuarray.empty((n1,n2), np.float32)
    
#     # Inverse FFT
#     plan_backward = cu_fft.Plan((n1, n2), np.complex64, np.float32)
#     cu_fft.ifft(ygpu, x, plan_backward)
    
#     # Must divide by the total number of pixels in the image to get the normalisation right
#     xout = x.get()/n1/n2
    
#     return xout

