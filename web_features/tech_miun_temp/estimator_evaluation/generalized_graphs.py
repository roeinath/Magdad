from os import mkdir, path
import os
from matplotlib.pyplot import scatter, xlabel, ylabel, show, savefig, clf
from web_features.tech_miun_temp.estimator_evaluation.helper_functions import delete_not_relevants, \
    open_file_and_save_graph

def create_generelized_graph(x_parameters, y_parameters, x_name, y_name, output_path):
    name = f'{y_name} as a function of {x_name}'
    x_parameters, y_parameters = delete_not_relevants(x_parameters, y_parameters)
    scatter(x_parameters, y_parameters)
    xlabel(f'{x_name}')
    ylabel(f'{y_name}')
    #open_file_and_save_graph(name, os.path.join(__file__,"..","results"), name)
    open_file_and_save_graph(name, output_path, name)
    clf()
