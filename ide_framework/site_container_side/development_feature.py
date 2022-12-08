import random
import re
import os
from mongoengine import *
from ide_framework.site_container_side.container_command import add_container_command
import ide_framework.site_container_side.container_name_manager
from email.mime import base
from email.policy import default
from APIs.TalpiotAPIs.Gitlab import update_file_tree
from APIs.TalpiotAPIs.Gitlab.update_file_tree import Commit, GitlabAPI, GitLabException, UpdateFileTree
from APIs.TalpiotAPIs.User.user import User
from APIs.TalpiotAPIs.Gitlab.gitlab_file_tree import GitlabFileTree
from ide_framework.site_container_side.container_name_manager import ContainerNameManager

TEMPLATE_CODE = '''
from BotFramework import *
from Talpiot.ExternalAPIs import *
from Talpiot.TalpiotAPIs import *
from Talpiot.Database import *
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.ui.ui import UI, Button
from Talpiot.TalpiotAPIs.User.user import User


class YOUR_FEATURE_NAME(BotFeature):

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        pass

    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        pass

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "מתלם" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []

'''

INIT_TEMPLATE = '''
from BotFramework import FeatureSettings, FeatureType


def get_settings():
    return FeatureSettings(display_name="INSERT NAME IN INIT FILE", _type=FeatureType.REGULAR_FEATURE)

'''

class DevelopmentFeature(Document):
    meta = {'collection': 'development_features', 'db_alias': 'talpiot_dev'}
    feature_name: str = StringField(max_length=50)
    users = ListField(field=ReferenceField(User), max_length=10)
    container_name = StringField()
    commits = ListField(field=ListField(field=StringField(), max_length=2), max_length=5000, default=[])
    file_relative_paths = ListField(max_length=10)
    feature_base_path: str = StringField(max_length=70)
    branch_name: str = StringField(max_length=70)
    file_tree = ReferenceField('GitlabFileTree')

    def __init__(self, **kwargs):
        if 'port_host' in kwargs:
            del kwargs['port_host']
        super(DevelopmentFeature, self).__init__(**kwargs)

    @staticmethod
    def new_feature(feature_name: str, user: User, base_path: str):
        # make sure feature name is not taken
        if len(DevelopmentFeature.objects(feature_name=feature_name)) != 0:
            # raise Exception(f"feature name is not available")  # TODO show on screen?
            print("noooo")
            return None
        dev_feat = DevelopmentFeature(feature_name=feature_name, users=[user],
                                      branch_name="ide-feature-" + feature_name,
                                      feature_base_path=base_path)
        # TODO: Catch exception: this name already exists
        GitlabAPI.checkout(dev_feat.branch_name)
        print(f"Create new branch {dev_feat.branch_name}")
        dev_feat.save()
        dev_feat.file_tree = GitlabFileTree(name=feature_name, url=base_path[:-1], branch = dev_feat.branch_name)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), r"your_feature_name.py-template.txt"), encoding='utf-8') as template:
            dev_feat.commit_and_push(template.read(), relative_path=feature_name + ".py",
                                     commit_msg=f'initial commit: {user.name}')
        dev_feat.commit_and_push(INIT_TEMPLATE, relative_path="__init__.py",
                                     commit_msg=f'initial commit: {user.name}')
        return dev_feat

    @staticmethod
    def get_dev_features(user=None):
        return [feature.feature_name for feature in DevelopmentFeature.objects() if
                user in feature.users or user is None]

    def run(self, code: str):
        # get an available container name
        if self.container_name is None:  # for re-run
            self.container_name = ContainerNameManager.get_instance().fetch_container(self.users[0])
        data = {"db_name": "talpiot_dev", "branch_name": self.branch_name}
        # add new start-command for this container, with specified branch and db names.
        add_container_command(self.container_name, "start_container", data)

    def stop_run(self):
        # stop the running of the container, and free its name
        ContainerNameManager.get_instance().free(self.container_name)
        data = {"db_name": "talpiot_dev", "branch_name": "branch"}
        add_container_command(self.container_name, "stop_container", data)

    def commit_and_push(self, code: str, relative_path, commit_msg='Default commit messege'):
        existing_file = relative_path in self.file_relative_paths
        commit_obj = Commit(branch=self.branch_name)
        commit_obj.set_commit_msg(commit_msg=commit_msg)
        if existing_file:
            commit_obj.add_update(self.feature_base_path + relative_path, content=code)
        else:
            print("This is an add create commit")
            commit_obj.add_create(self.feature_base_path + relative_path, content=code)
            self.file_relative_paths.append(relative_path)

        print(relative_path, "\n", self.file_relative_paths)

        commit_token, commit_timestamp = GitlabAPI.commit(commit_obj)
        self.commits.append([commit_token, commit_timestamp])
        if not existing_file:
            """reversed_base_path = self.feature_base_path[:-1]
            reversed_base_path = reversed_base_path[::-1]
            reversed_base_path = reversed_base_path[reversed_base_path.find('/') + 1:]
            print('path to fetch file tree ' + self.feature_base_path[:-1])
            UpdateFileTree().update_file_tree(self.feature_base_path[:-1], self.branch_name)
            """
            path = ''
            directory = self.file_tree
            for name in relative_path.split('/'):
                print("new", name)
                tree_obj = GitlabFileTree(name=name, url=path + name, branch=self.branch_name)
                tree_obj.save()
                directory.children.append(tree_obj)
                directory.save()
                directory = tree_obj
                path += name + '/'
        self.save()
        print("Commited")

    def create_file(self, filename):
        self.commit_and_push("#SOME FILE TEMPLATE", relative_path=filename + '.py', commit_msg=f'new file: {filename}')

    def fetch_from_git(self, relative_path):
        print(self.file_relative_paths, relative_path)
        if relative_path not in self.file_relative_paths:
            return "No code"
        return GitlabAPI.get_file_code(self.feature_base_path + relative_path, self.branch_name)

    def publish(self, title="Default feature: ", description="Very detailed message"):
        if title == "Default feature: ":
            title += self.feature_name
        GitlabAPI.create_merge_request(title, description, self.branch_name)

    def delete_feature(self):
        GitlabAPI.delete_branch(self.branch_name)
        for obj in GitlabFileTree.objects(branch = self.branch_name):
            obj.delete()
        self.delete()

    def delete_file(self, file_path):
        self.file_relative_paths.remove(file_path)
        print(f'delete {file_path}')
        for child in self.file_tree.children:
            print(child.url)
            if child.url == file_path:
                print(f"deleting {child.url}")
                self.file_tree.children.remove(child)
                self.file_tree.save()
                print([child.url for child in self.file_tree.children])
                child.delete()
                break
        GitlabAPI.delete_file(self.branch_name, self.feature_base_path + file_path)
        print('deleted')
        self.save()
