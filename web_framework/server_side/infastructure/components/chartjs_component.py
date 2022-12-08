from web_framework.server_side.infastructure.ui_component import UIComponent
import web_framework.server_side.infastructure.ids_manager as ids_manager

from typing import Callable, Dict
from web_framework.server_side.infastructure.constants import *

DEFAULT_SIZE = '40vw'


# for more references go to https://react-chartjs-2.js.org/examples/

class ChartjsComponent(UIComponent):
    LINE = 'line'
    BAR = 'bar'
    RADAR = 'radar'
    SCATTER = 'scatter'
    PIE = 'pie'
    DOUGHNUT = 'doughnut'

    def __init__(self, width: str = DEFAULT_SIZE, height: str = DEFAULT_SIZE):
        super().__init__()
        self.__height = height  # can be 100%, 100px, 100rem, 100vw, 100hw (any number)
        self.__width = width  # can be 100%, 100px, 100rem, 100vw, 100hw (any number)
        self.__datasets = []
        self.__labels = []
        self.__plugins = {'legend': None}
        self.__scales = {}

    def render(self):
        return {
            JSON_TYPE: 'ChartJsComponent',
            JSON_ID: self.id,
            'chart': {
                'data': {
                    'labels': self.__labels,
                    'datasets': self.__datasets
                },
            },
            'options': {
                'responsive': True,
                'plugins': self.__plugins,
                'scales': self.__scales,

            },
            JSON_WIDTH: self.__width,
            'height': self.__height
        }

    def plot(self, x, y, label=None, color=None, border_color=None, border_width=None, fill=None):
        self.__chart(self.LINE, x, y, label, color, border_color, border_width, fill)

    def bar(self, x, y, label=None, color=None, border_color=None, border_width=None, fill=None):
        self.__chart(self.BAR, x, y, label, color, border_color, border_width, fill)

    def radar(self, x, y, label=None, color=None, border_color=None, border_width=None, fill=None):
        self.__chart(self.RADAR, x, y, label, color, border_color, border_width, fill)

    def scatter(self, x, y, label=None, color=None, border_color=None, border_width=None, fill=None):
        self.__chart(self.SCATTER, x, [{'x': x_, 'y': y_} for x_, y_ in zip(x, y)], label, color, border_color,
                     border_width, fill)

    def pie(self, x, y, label=None, color=None, border_color=None, border_width=None, fill=None):
        self.__chart(self.PIE, x, y, label, color, border_color, border_width, fill)

    def doughnut(self, x, y, label=None, color=None, border_color=None, border_width=None, fill=None):
        self.__chart(self.DOUGHNUT, x, y, label, color, border_color, border_width, fill)

    def __chart(self, type: str, x, y, label=None, color=None, border_color=None, border_width=None, fill=None):
        dataset = {
            'type': type,
            'data': list(y),
            'label': label,
            'backgroundColor': color,
            'borderColor': border_color,
            'borderWidth': border_width,
            'fill': fill,
            'options': {
                'labels': {
                    'font': {
                        'size': 100
                    }
                }
            }
        }
        dataset = {key: value for key, value in dataset.items() if value is not None}

        self.__labels = x
        self.__datasets.append(dataset)

    def title(self, text: str, size: int = 50):
        self.__plugins['title'] = {
            'display': True,
            'text': text,
            'font': {'size': size}
        }

    def legend(self, size: int = 20, position: str = 'top'):
        self.__plugins['legend'] = {
            'position': position,
            'labels': {'font': {'size': size}}
        }

    def scale(self, label_name: str, min: int = 0, max: int = 6):
        scales = self.__scales.get(label_name, {})
        scales.update({'min': min, 'max': max})
        self.__scales[label_name] = scales

    def labels(self, label_name: str, size: int):
        scales = self.__scales.get(label_name, {})
        scales.update({'pointLabels': {'font': {'size': size}}})
        self.__scales[label_name] = scales
