# from general import *
import datetime
from web_framework.server_side.infastructure.ui_component import UIComponent

from APIs.TalpiotAPIs import User
from mongoengine import Document, StringField, DateField, DateTimeField

from web_framework.server_side.infastructure.components.button import Button
from web_framework.server_side.infastructure.components.datagrid import DataGrid
from web_framework.server_side.infastructure.components.form import Form
from web_framework.server_side.infastructure.page import Page

class Edit_Users(Page):
    def __init__(self):
        pass
    
    def get_page_ui(self) -> UIComponent:
        data = list(User.objects)
        return(DataGrid(data))


