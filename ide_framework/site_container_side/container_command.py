from mongoengine import Document, DictField, StringField


# A container command that should be located in the container_commands collection
class ContainerCommand(Document):
    meta = {'collection': 'container_commands', 'db_alias': 'talpiot_dev'}

    container_name: str = StringField(required=True)
    command_name: str = StringField(required=True)
    data: dict = DictField(required=False)


# Creates a new container commands and save it in db, so the containers can get it.
def add_container_command(container_name: str, command_name: str, data: dict):
    packet = ContainerCommand()
    packet.container_name = container_name
    packet.command_name = command_name
    packet.data = data
    packet.save()


# A wrapper for convenience
def start_container(container_name, db_name, branch_name):
    add_container_command(container_name, "start_container", {"db_name": db_name, "branch_name": branch_name})


# A wrapper for convenience
def stop_container(container_name):
    add_container_command(container_name, "stop_container", {})
