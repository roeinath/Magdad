from mongoengine import Document, DictField, StringField


# A bot command that should be located in the bot_commands collection
class BotCommand(Document):
    meta = {'collection': 'bot_commands'}

    command_name: str = StringField(required=True)
    data: dict = DictField(required=False)

    def get_command_name(self) -> str:
        return self.command_name
