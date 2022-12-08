from mongoengine import Document, DictField, StringField, ReferenceField
from mongoengine import  DEFAULT_CONNECTION_NAME as DB_ALIAS
from APIs.TalpiotAPIs.User.user import User

#A bot command that should be located in the bot_commands collection
class MissingReason(Document):
    meta = {'collection': 'missing_reasons', 'db_alias': DB_ALIAS}

    user:User = ReferenceField(User)
    reason:str = StringField()