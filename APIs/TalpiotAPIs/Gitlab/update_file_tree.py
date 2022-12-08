import asyncio
import urllib.parse
from mongoengine import *
import requests
import json

from APIs.TalpiotAPIs.Gitlab.gitlab_file_tree import GitlabFileTree
from APIs.TalpiotAPIs.Feature.feature import Feature

DEFAULT_BASE_BRANCH = "master"


class UpdateFileTree:
    def __init__(self):
        self.__root_path = ''
        self.__files = None

    def update_file_tree(self, path= '', branch=DEFAULT_BASE_BRANCH):
        old_tree = GitlabFileTree.objects(url=path)
        if old_tree:
            to_delete = [old_tree]
            while to_delete:
                obj = to_delete[0]
                if obj.children:
                    to_delete.append(obj.children)
                to_delete = to_delete[1:]
                obj.delete()
        response = requests.get(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/tree?path=",
                                params={"path": path, "ref": branch, "recursive":True},
                                headers={"PRIVATE-TOKEN": ACCESS_TOKEN}
                                )
        print(response.json())
        """reversed = path[::-1]
        name = (reversed[:reversed.find('/')])[::-1]
        files = []
        for entry in response.json():
            files.append(GitlabFileTree(name=entry['name'], url=entry['path']), branch = branch)
        for file in files:
            file    .save()
        root = GitlabFileTree(name=name, url=path, children=files,branch = branch)
        root.save()"""
        loop = self.get_or_create_eventloop()
        loop.run_until_complete(self.list_files(path, branch))

    @staticmethod
    def get_or_create_eventloop():
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()

    async def list_files(self, path='', branch=DEFAULT_BASE_BRANCH) -> list:
        print("list:", path)
        response = requests.get(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/tree?path=",
                                params={"path": path, "ref": branch},
                                headers={"PRIVATE-TOKEN": ACCESS_TOKEN}
                                )
        print(response.json(), str(response))
        files = []
        if response.status_code == 200:
            files += await asyncio.gather(*[self.extract_file_data(f,branch) for f in response.json()])
        if path == self.__root_path:
            self.__files = GitlabFileTree(name=self.__root_path, url=self.__root_path, children=files, branch = branch).to_json()
        return files

    async def extract_file_data(self, full_data, branch = DEFAULT_BASE_BRANCH):
        self.tree = GitlabFileTree(name=full_data['name'], url=full_data['path'], branch = branch)
        file_data = self.tree
        if full_data['type'] == 'tree' and not full_data['name'].startswith('.'):
            file_data.children = await self.list_files(full_data['path'])
        file_data.save()
        print("saved", file_data.url)
        return file_data

    @staticmethod
    def get_file_code(url):
        response = requests.get(
            f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/files/{urllib.parse.quote_plus(url)}/raw",
            params={},
            headers={"PRIVATE-TOKEN": ACCESS_TOKEN}
            )
        if response.status_code == 200:
            return response.content.decode() or "# FILE EMPTY"



ACCESS_TOKEN = "glpat-z9U7kWok3pAP5nJtH_8X"
PROJECT_ID = 25218462
NAME = "ide"

class GitlabAPI:
    #TODO: make functions staticmethod,
    # check status code of response before calling json()
    # base url (https://gitlab.com/api/v4/projects) should be a const
    # merge classes UpdateFileTree, GitlabAPI
    # rename file and put in TalpiotSystem
    @staticmethod
    def checkout(new_branch, base_branch = DEFAULT_BASE_BRANCH):
        response = requests.get(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/branches",
                                 params={"search":new_branch},
                                 headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
        response = response.json()
        if response:
            raise GitLabException("This name already exists")

        response = requests.post(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/branches",
                                 params={"branch": new_branch, "ref": base_branch},
                                 headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
        response = response.json()
        if 'message' in response.keys():
            print()
            raise GitLabException(response['message'])

    @staticmethod
    def create_merge_request(title, description, source_branch, base_branch = DEFAULT_BASE_BRANCH):
        response = requests.post(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/merge_requests",
                                 params={"source_branch": source_branch, "target_branch": base_branch,
                                         "description": description, "title": title},
                                 headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
        response = response.json()
        if 'message' in response.keys():
            raise GitLabException(response['message'])

    @staticmethod
    def commit(commit_obj):
        response = requests.post(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/commits",
                                 headers={"PRIVATE-TOKEN": ACCESS_TOKEN, "Content-Type": "application/json"},
                                 data=commit_obj.dump())
        response = response.json()
        print(response)
        """if "message" in response.keys():
            raise GitLabException(response["message"])"""
        return "", "" #response["id"],response["committed_date"]

    '''@staticmethod
    def get_commit_list(branch):
        commits = []
        response = requests.get(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/commits/{branch}",
                                 headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
        response = response.json()
        commits.append(response)
        for parent in response['parent_ids']:
            commits.extend(get_commit_list(parent))
        return commits

    @staticmethod
    def revert_commit(branch, commit_id):
        response = requests.post(f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/commits/{commit_id}/revert",
                                 params={"branch": branch}, headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
        response = response.json()'''

    """def force_cherry_pick(branch, commit_id):
        i = 0
        commit_list = get_commit_list(branch)
        while commit_list[i]['id'] != commit_id:
            revert_commit(branch, get_commit_list(branch)[i]['id'])
            i += 1
        revert_commit(branch, get_commit_list(branch)[i]['id'])"""

    @staticmethod
    def get_file_code(url, branch):
        print(urllib.parse.quote_plus(url))
        response = requests.get(
            f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/files/{urllib.parse.quote_plus(url)}/raw?ref={branch}",
            params={},
            headers={"PRIVATE-TOKEN": ACCESS_TOKEN}
            )

        if response.status_code == 200:
            return response.content.decode() or "# FILE EMPTY"

    @staticmethod
    def delete_branch(branch):
        if branch.startswith("ide-feature-") and "ide-feature-" in branch:
            response = requests.delete(
                f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/branches/{branch}",
                params={},
                headers={"PRIVATE-TOKEN": ACCESS_TOKEN}
            )
            #print(response.json())

    @staticmethod
    def delete_file(branch, file_path):
        if branch.startswith("ide-feature-") and "ide-feature-" in branch:
            response = requests.delete(
                f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/files/{urllib.parse.quote_plus(file_path)}",
                params={"branch": branch, "commit_message": "delete file"},
                headers={"PRIVATE-TOKEN": ACCESS_TOKEN}
            )

class GitLabException(Exception):
    pass

class Commit:
    def __init__(self, branch):
        self.branch = branch
        self.actions = []
        self.commit_msg = ''

    def add_create(self, file_path, content):
        self.actions.append({"action": "create", "file_path": file_path, "content": content})

    def add_delete(self, file_path):
        self.actions.append({"action": "delete", "file_path": file_path})

    def add_move(self, new_path, prev_path):
        self.actions.append({"action": "move", "file_path": new_path, "previous_path": prev_path})

    def add_update(self, file_path, content):
        self.actions.append({"action": "update", "file_path": file_path, "content": content})

    def set_commit_msg(self, commit_msg):
        self.commit_msg = commit_msg

    def dump(self):
        payload = {"branch": self.branch, "commit_message": self.commit_msg, "actions": self.actions}
        return json.dumps(payload)

