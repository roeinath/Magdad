# import os
from bot_features.Shagmach.Order_Equipment.DBModels.DB_equipment import OrderEquipment
from APIs.ExternalAPIs.GoogleSheets.google_sheets import GoogleSheets
from bot_features.Shagmach.Order_Equipment.Logic.data import *
ID = "1KAgw1F9ip9mk4lQ-Dsz0N5NwQrQHwyzDmrm32I2rUdI"
BASE_PATH = r"C:\Users\t8853461\Desktop\TalpiBot\Features\Shagmach\Order_Equipment\Logic"
LIST_OF_PRODUCTS = get_order_data()

EXCEL_DICT = get_excel_data()


def get_products():
    return LIST_OF_PRODUCTS


def add_order(mahzor, quantity, product, status):
    order = OrderEquipment(mahzor=mahzor, quantity=quantity, product=product, status=status)
    order.save()


def get_orders(mahzor):
    orders = []
    for order in OrderEquipment.objects(mahzor=mahzor):
        product_string = LIST_OF_PRODUCTS[order.product] + ", "
        quantity_string = str(order.quantity)
        if order.status == "מחכה לאישור":
            status_string = "❓"
        elif order.status == "מאושר":
            status_string = "✅"
        else:
            status_string = "❌"
        output_string = product_string + quantity_string + ".    " + status_string
        orders.append(output_string)
    return orders


def update_status(str_order: str, mahzor):
    index_dot = str_order.index(".")
    str_order = str_order[:index_dot]
    order = str_order.split(", ")
    for order_db in OrderEquipment.objects(mahzor=mahzor):
        if order[0] == LIST_OF_PRODUCTS[order_db.product] and order[1] == str(order_db.quantity):
            if order_db.status == "מחכה לאישור":
                order_db.status = "מאושר"
            elif order_db.status == "מאושר":
                order_db.status = "לא מאושר"
            else:
                order_db.status = "מחכה לאישור"
            order_db.save()
            break


def into_excel():
    with GoogleSheets.get_instance() as gc:
        for order in OrderEquipment.objects(status="מאושר"):
            my_product = LIST_OF_PRODUCTS[order.product]
            if my_product not in list(EXCEL_DICT.keys()):
                continue
            cell_to_edit = EXCEL_DICT[my_product]
            cell_data = gc.get_range(ID, "Equipment", cell_to_edit)
            cur_data = 0
            if cell_data is not None:
                cur_data = cell_data[0][0]
            gc.set_range(ID, "Equipment", cell_to_edit, [[str(int(cur_data) + order.quantity)]])
    OrderEquipment.objects().delete()

