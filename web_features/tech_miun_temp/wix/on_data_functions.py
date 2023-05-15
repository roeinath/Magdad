ON_DATA_FUNCTIONS = {
    'show': show
}

ON_DATA_COLUMN  _FUNCTIONS = {
    'std' = std
    'plot' = plot
}

def show(data: str):
    return data

def std(data: pd.Series):
   pass

def plot(x_data: pd.Series, y_data: pd.Series):
   pass
