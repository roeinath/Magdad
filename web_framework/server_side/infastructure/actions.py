from APIs.TalpiotSystem.bot_command import BotCommand


# Creates a new bot commands and sends it to the bot
def add_bot_command(command_name: str, data: dict):
    packet = BotCommand()
    packet.command_name = command_name
    packet.data = data
    packet.save()


# A wraper for convinience
def simple_send_message(text, user_list):
    add_bot_command("simple_send_message", {"text": text, "user_list": user_list})
