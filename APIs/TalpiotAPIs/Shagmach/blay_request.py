from mongoengine import Document, StringField, BooleanField, IntField, ReferenceField

from APIs.TalpiotAPIs import User


class ItemTypes:
    BOYS_SHIRT = 'חולצת א\' מדי בנים'
    BOYS_PANTS = 'מכנסי א\' מדי בנים'
    GIRLS_SHIRT = 'חולצת א\' מדי בנות'
    GIRLS_PANTS = 'מכנסי א\' מדי בנות'
    BOOTS = 'נעלי חי"ר'
    SHOES = 'נעלי קבע'
    COAT = 'מעיל א\''
    JUMPER = 'סוודר א\''
    OTHER = 'אחר'

    @staticmethod
    def get_list():
        return [ItemTypes.BOYS_SHIRT, ItemTypes.BOYS_PANTS, ItemTypes.GIRLS_SHIRT, ItemTypes.GIRLS_PANTS,
                ItemTypes.BOOTS, ItemTypes.SHOES,
                ItemTypes.COAT, ItemTypes.JUMPER, ItemTypes.OTHER]


class ItemFixRequest(Document):
    user: User = ReferenceField(User)
    soldier_id: str = StringField()
    item_type: str = StringField()
    amount: int = IntField()
    reason: str = StringField()
    size_required: str = StringField()
    comment: str = StringField()
    closed: bool = BooleanField(default=False)

    @staticmethod
    def new_request(user: User, soldier_id: str, item_type: ItemTypes, amount: int, reason: str, size_required: str):
        return ItemFixRequest(user=user, soldier_id=soldier_id, item_type=item_type, amount=amount, reason=reason, 
                                size_required=size_required, comment='', closed=False)
