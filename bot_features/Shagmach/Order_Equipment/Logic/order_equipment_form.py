from bot_framework.Activity.FormActivity.Field import *
from bot_framework.Activity.FormActivity.form_activity import FormActivity
from bot_features.Shagmach.Order_Equipment.Logic import logic


class OrderEquipmentForm:
    BAD_PRODUCT = "בדוק את תקינות שם המוצר"
    BAD_QUANTITY = "בדוק את תקינות הכמות"


    def __init__(self):
        self.product = ChoiceField(name="שם הפריט", msg="הקלד את שם הפריט", options=logic.get_products())
        self.quantity = TextField(name="כמות", msg="הקלד את הכמות הדרושה")

    def validate(self):
        if self.product.value is None:
            raise FormActivity.ValidationException(OrderEquipmentForm.BAD_PRODUCT)

        if self.quantity.value is None or not self.quantity.value.isnumeric() or int(self.quantity.value) < 1\
                or len(self.quantity.value) > 4:
            raise FormActivity.ValidationException(OrderEquipmentForm.BAD_QUANTITY)

