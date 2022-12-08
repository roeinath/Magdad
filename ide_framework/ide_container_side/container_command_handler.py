import time
import multiprocessing
from ide_framework.site_container_side.container_command import ContainerCommand
import os
import ide_framework.ide_container_side.run_container as run_container
from ide_framework.site_container_side.container_name_manager import ContainerName
from mongoengine import *
from APIs.TalpiotAPIs.User.user import User
import signal


# The function of the Command "start_container"
def start_container(p: multiprocessing.Process):
    print("Start container")
    p.start()


# The function of the Command "stop_container"
def stop_container(p: multiprocessing.Process):
    print("Stop container")
    os.kill(p.pid, signal.SIGKILL)
    print("killed")
    # p.terminate()
    # print('Process terminated:', p, p.is_alive())
    # p.join()
    # print('Process joined:', p, p.is_alive())
    # # p.close()


command_names_to_funcs = {"start_container": start_container, "stop_container": stop_container}


# This Class is a thread that listens to the contianerCommand collection and executes the commands it recieves
class ContainerCommandHandler:

    def __init__(self):
        print("starting to search for commands...")
        self.p = None

    # Checks for new container commands directed to this container in the collection and executes them
    def container_command_handler(self):
        while True:
            print("in command handler")
            container_commands = ContainerCommand.objects()
            for cmd in container_commands:
                feature_for_me = (cmd.container_name == os.environ['CONTAINER_NAME'])
                print(cmd.container_name, ", ", os.environ['CONTAINER_NAME'], ", ", feature_for_me)
                if feature_for_me:
                    print("got command for me now")
                    self.switch_parser(cmd)
                    cmd.delete()
            time.sleep(5)

    # Interprets the command and calls it's function
    def switch_parser(self, container_command: ContainerCommand):
        try:
            command_function = command_names_to_funcs[container_command.command_name]
        except:
            print("Error: bot command not found")
            return
        print(container_command.command_name)
        if container_command.command_name == "start_container":
            print("Starting container with feature", container_command.data["branch_name"])
            if self.p is not None:
                print("Stopping container before start again")
                stop_container(self.p)  # need to stop before re-run
                # create new process to run bot on container
            self.p = multiprocessing.Process(
                target=run_container.run_container,
                args=(container_command.data["db_name"], container_command.data["branch_name"],))
            start_container(self.p)
        if container_command.command_name == "stop_container" and self.p is not None:
            print("Stopping container with feature")
            stop_container(self.p)
        return
