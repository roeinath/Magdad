import requests
import json


class GitlabAPI:
    def __init__(self, base_branch, access_token, project_id, name):
        self.base_branch = base_branch
        self.access_token = access_token
        self.project_id = project_id
        self.name = name

    def checkout(self, new_branch):
        response = requests.get(f"https://gitlab.com/api/v4/projects/{self.project_id}/repository/branches",
                                 params={"search":new_branch},
                                 headers={"PRIVATE-TOKEN": self.access_token})
        response = response.json()
        if response:
            raise GitLabException("This name already exists")
        if '-' in new_branch:
            raise GitLabException("Feature name can't contain -")
        response = requests.post(f"https://gitlab.com/api/v4/projects/{self.project_id}/repository/branches",
                                 params={"branch": new_branch + '-' + self.name, "ref": self.base_branch},
                                 headers={"PRIVATE-TOKEN": self.access_token})
        response = response.json()
        print(response)
        if 'message' in response.keys():
            raise GitLabException(response['message'])

    def create_merge_request(self, title, description, source_branch):
        if source_branch.split('-')[-1] != self.name:
            raise GitLabException("Unauthorized to commit to the repository")
        source_branch += '-' + self.name
        response = requests.post("https://gitlab.com/api/v4/projects/35159621/merge_requests",
                                 params={"source_branch": source_branch, "target_branch": self.base_branch,
                                         "description": description, "title": title},
                                 headers={"PRIVATE-TOKEN": self.access_token})
        response = response.json()
        if 'message' in response.keys():
            raise GitLabException(response['message'])

    def commit(self, commit_obj):
        if not self.is_authorized(commit_obj.branch):
            raise GitLabException("Unauthorized to commit to the repository")
        commit_obj.branch += '-' + self.name

        response = requests.post("https://gitlab.com/api/v4/projects/35159621/repository/commits",
                                 headers={"PRIVATE-TOKEN": self.access_token, "Content-Type": "application/json"},
                                 data=commit_obj.dump())
        response = response.json()
        commit_obj.branch = commit_obj.branch[:-len(self.name + '-')]
        """if "message" in response.keys():
            raise GitLabException(response["message"])"""
        return ''

    def get_commit_list(self, branch, is_recent=True):
        if is_recent:
            branch += '-' + self.name
        commits = []
        response = requests.get(f"https://gitlab.com/api/v4/projects/35159621/repository/commits/{branch}",
                                 headers={"PRIVATE-TOKEN": self.access_token})
        response = response.json()
        commits.append(response)
        for parent in response['parent_ids']:
            commits.extend(self.get_commit_list(parent, is_recent=False))
        return commits

    def is_authorized(self, branch):
        response = requests.get(f"https://gitlab.com/api/v4/projects/{self.project_id}/repository/branches",
                                params={"search": branch},
                                headers={"PRIVATE-TOKEN": self.access_token})
        response = response.json()
        return response[0]['name'] == branch + '-' + self.name

    def revert_commit(self, branch, commit_id):
        if not self.is_authorized(branch):
            raise GitLabException("Unauthorized to commit to the repository")
        branch += '-' + self.name
        response = requests.post(f"https://gitlab.com/api/v4/projects/{self.project_id}/repository/commits/{commit_id}/revert",
                                 params={"branch": branch}, headers={"PRIVATE-TOKEN": self.access_token})
        response = response.json()

    def force_cherry_pick(self, branch, commit_id):
        if not self.is_authorized(branch):
            raise GitLabException("Unauthorized to commit to the repository")
        i = 0
        commit_list = self.get_commit_list(branch)
        while commit_list[i]['id'] != commit_id:
            self.revert_commit(branch, api.get_commit_list(branch)[i]['id'])
            i += 1
        self.revert_commit(branch, api.get_commit_list(branch)[i]['id'])

    def delete_branch(self, branch):
        reponse = requests.delete(
            f"https://gitlab.com/api/v4/projects/{self.project_id}/repository/branches/{branch}",
            params={},
            headers={"PRIVATE-TOKEN": self.access_token}
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


if __name__ == '__main__':
    api = GitlabAPI("main", "glpat-4C72LNcPWNNFUuUvspqv", 35159621, 'a')
    api.checkout("new")