
from bot_framework.session import Session
from bot_framework.ui.ui import UI
from bot_framework.Commands.bot_command_handler import add_bot_command

#The function of the Command "simple_send_message", sends a messege to a list of users
def simple_send_message(ui:UI,data:dict):
    user_list = data["user_list"]
    for user in user_list:
        print("sending", data["text"], "to", reversed(user.name))
        session = Session("General", user ,ui)
        ui.create_text_view(session, data["text"]).draw()

#Adds the command, so the interpreter will call the function when a command with the name "simple_send_message" is received
add_bot_command("simple_send_message", simple_send_message)



# Template for adding new commands that the bot will be able to excute:
# 
# You should decied the name of your command. make sure it implies on the commads fuctionality.
# Let's say the command's name is "send_schedualed_messege_command". Your code should look like:
# 
# def send_schedualed_messege_command(ui:UI,data:dict):
#   your code here
# 
# add_bot_command("send_schedualed_messege_command", send_schedualed_messege_command)
# 
