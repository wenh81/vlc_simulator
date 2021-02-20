####################################
####### General Library file #######
####################################

from matplotlib import pyplot as plt

import numpy as np

import Global

from timeit import default_timer as timer

import inspect

# import pycuda.autoinit

# import pycuda.gpuarray as gpuarray

# ONLY FOR LINUX
# import skcuda.fft as cu_fft

def plotDebug(signal, label = "", symbols='r-'):
    """Fast plot for debug."""

    if label == "":
        # Get function call
        function_call = inspect.stack()[1][-2][0].strip()
        # Extract function name
        func_name = function_call.split('(')[0]
        # Extract 
        label = function_call.split(func_name)[1].\
            replace('(','').replace(')','').split(',')[0]
        
    plt.plot(signal, symbols, label=label)
    plt.grid(True)
    # plt.ylim(np.min(signal)*1.1, np.max(signal)*1.1)
    plt.legend(fontsize=10)
    plt.show()

def printDebug(signal, details = False, plot = False):
    """Pretty debug signal print. Use details = True for more information"""

    print('\n---------------------------------------------------------------------------')
    
    # Get function call
    function_call = inspect.stack()[1][-2][0].strip()
    # Extract function name
    func_name = function_call.split('(')[0]
    # Extract 
    signal_name = function_call.split(func_name)[1].\
        replace('(','').replace(')','').split(',')[0]
    
    print('> START <' + f"\t-->\t<{signal_name}>")
    # Actual print with value
    print(f"{type(signal)}")
    print(f"Value :\n{signal}")
    
    if details:
        print('\n>>> More details <<<\n')
        print(f">> All methods for {type(signal)}:")
        print(f"{dir(signal)}")
    
    if plot:
        plotDebug(signal, label = signal_name)

    print('>  END  <' + f"\t-->\t<{signal_name}>")
    print('---------------------------------------------------------------------------\n')

def zeroClip(signal):
    """Returns the same signal, but clipped to zero"""
    
    return np.array([item if item >= 0 else 0 for item in signal])

def plotTxRxData(data, label, handle, sync_obj, show = False):
    """Plots Tx/Rx data."""
    
    sync_obj.appendToSimulationPath("plotTxRxData @ generalLibrary")
    
    # Set previous for debug
    sync_obj.setPrevious("generalLibrary")
    
    # plt.figure(figsize=(8,2))
    plt.plot((data), label=label)
    # plt.plot((np.fft.ifft(data)), label=label)
    plt.legend(fontsize=10)
    plt.xlabel('Time'); plt.ylabel('$|x(t)|$')
    plt.grid(True)
    plt.show(show)

def plotTxRxDataList(data_list, label, handle, sync_obj, show = False):
    """Plots Tx/Rx data list."""
    
    sync_obj.appendToSimulationPath("plotTxRxDataList @ generalLibrary")
    
    # Set previous for debug
    sync_obj.setPrevious("generalLibrary")
    
    concatenated_data = []
    for data in data_list:
        concatenated_data += list(data)
    
    concatenated_data = np.array(concatenated_data)
    
    # plot concatenated list
    plotTxRxData(
        data = concatenated_data,
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

