from mongoengine import Document, StringField, ListField, ReferenceField, IntField


class TalpiSharedTag(Document):
    tag = StringField()
    priority = IntField()
