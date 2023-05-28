
from numpy import std, mean
from matplotlib.pyplot import hist, show, xlabel, ylabel, title, plot, scatter, legend, savefig, clf, gca
from os import mkdir, path
import os 

def delete_not_relevants(x_values, y_values):
    x_values_list = []
    y_values_list = []
    for x,y in zip(x_values, y_values):
        if y != "ל.ר":
            x_values_list.append(x)
            y_values_list.append(float(str(y)[:4]))  # because typos
    return x_values_list, y_values_list
    
def open_file_and_save_graph(name,address,test_name):
     if not path.exists(os.path.join(address, name)):
         mkdir(os.path.join(address, name))
     savefig(os.path.join(address, name, f'{test_name}.png'))
