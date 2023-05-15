import pandas as pd
import numpy as np

STATISTICS_FUNCTIONS = 
{
    'no_func': no_func,
    'mean': mean,
    'std': std,
}

def no_func(data: pd.Series, row: int):
    '''
    returns the content in certain row in data array
    '''
    return data[row]

def mean(data: pd.Series)
    return data.mean()

def std(data: pd.Series):
   return data.std()


