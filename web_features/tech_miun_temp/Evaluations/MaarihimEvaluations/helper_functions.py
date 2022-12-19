# delete "not relevant" data in academic grade and face with typos -
# look at the data or ignore this function and understand
def delete_not_relevants(x_values, y_values):
    x_values_list = []
    y_values_list = []
    for x,y in zip(x_values, y_values):
        if y != "ל.ר" :
            x_values_list.append(x)
            y_values_list.append(float(str(y)[:4]))  # because typos
    return x_values_list, y_values_list