import time
import _thread
from APIs.TalpiotSystem.bot_command import BotCommand

# The function that the handler needs to run for each name of command
command_names_to_funcs = {}


# Adds a command to the dict that connects between command names to command functions
def add_bot_command(command_name: str, command_function):
    if command_name not in command_names_to_funcs:
        command_names_to_funcs[command_name] = command_function
    else:
        print(f"The bot bot command handler with the name: '{command_name}' already exists, try renaming your command")
        print("This handler was skipped.")


# The import is here for a reason. In order not to create a circular import but keep the code as clean as it can be.


# This Class is a thread that listens to the botCommand collection and executes the commands it recieves
class BotCommandHandler:

    def __init__(self, ui):
        self.ui = ui
        print("starting to search for commands...")
        _thread.start_new_thread(self.bot_command_handler, ())

    # Checks for new bot commands in the collection and executes them
    def bot_command_handler(self):
        while True:
            bot_commands = BotCommand.objects()
            for cmd in bot_commands:
                self.switch_parser(cmd)
                cmd.delete()
            time.sleep(1)

    # Interprets the command and calls it's function
    def switch_parser(self, bot_command: BotCommand):
        try:
            command_function = command_names_to_funcs[bot_command.command_name]
        except:
            print("Error: bot command not found")
            return
        command_function(self.ui, bot_command.data)