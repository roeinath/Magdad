from mongoengine import *
from APIs.TalpiotAPIs.User.user import User


class ContainerName(Document):
    meta = {'collection': 'container_names', 'db_alias': 'talpiot_dev'}
    status = BooleanField(default=False, required=True)
    container_name: str = StringField(required=True)
    user: User = ReferenceField(User)


# def __init__(self, container_name):
#     self.status = False
#     self.container_name = container_name
#     # should be a variable with the type user
#     self.user = None
#
#     #  who is the one to set me free


def free(self):
    self.status = False
    self.user = None
    self.delete()


def dibs(self, user):
    self.status = True
    self.user = user
    self.save()
    # print("saved")


def is_available(self):
    return not self.status


def __repr__(self):
    return "container_name: " + str(self.container_name) + ",  in use: " + str(self.status) + ",  user: " + str(
        self.user)


class ContainerNameManager:
    __instance = None

    def __init__(self):
        if ContainerNameManager.__instance is not None:
            raise Exception("This class is a singleton")
        #
        # file = open(r"ide_framework\site_container_side\containers_names.txt", "r")
        # self.containers_names = file.read().split('\n')
        # file.close()
        # self.containers_list = [ContainerName(status=False, container_name=container_name, user=None) for
        #                         container_name in self.containers_names]
        ContainerNameManager.__instance = self

    @staticmethod
    def get_instance():
        if ContainerNameManager.__instance is None:
            ContainerNameManager()
        return ContainerNameManager.__instance

    # pick random available container-name, to run code on.
    def fetch_container(self, user):
        print("fetching container for " + user.name)
        for container in ContainerName.objects(status=False):
            if container is not None:
                container.dibs(user)
                return container.container_name
        raise Exception("\nALL CONTAINERS ARE IN USE\n\n" + str(self))

    def __repr__(self):
        st = ""
        for container in ContainerName.objects():
            st += str(container) + '\n'
        return st

    # make container-name available again, code isn't running on the container anymore.
    def free(self, container_name):
        container = ContainerName.objects(container_name=container_name)
        if container is not None:
            container.free()
            return
        raise Exception(
            "\nTRIED TO FREE A CONTAINER USING A NAME THAT DOES NOT EXIST\n\n the name is: " + str(
                container_name) + "\n" + str(
                self))

    @property
    def instance(self):
        return self.__instance
