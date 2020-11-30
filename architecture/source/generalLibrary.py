####################################
####### General Library file #######
####################################

from matplotlib import pyplot as plt

import numpy as np

import Global

from timeit import default_timer as timer

def plotTxRxData(data, label, handle, sync_obj, show = False):
    """Plots Tx/Rx data."""
    
    sync_obj.appendToSimulationPath("plotTxRxData @ generalLibrary")
    
    # Set previous for debug
    sync_obj.setPrevious("generalLibrary")
    
    # plt.figure(figsize=(8,2))
    plt.plot((data), label=label)
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
    def new_function(*args, **kw):
        start_time = timer()
        result = function(*args, **kw)
        elapsed = timer() - start_time
        print(f'>>>> Function "{function.__name__}" took {elapsed} seconds to complete.\n')
        
        return result
    return new_function