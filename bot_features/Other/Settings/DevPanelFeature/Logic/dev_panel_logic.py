from APIs.TalpiotSystem.talpiot_git import TalpiBotGitCommit, TalpiBotGit


class DevPanelLogic:
    @staticmethod
    def get_last_commit_information() -> [str]:
        last_commit: TalpiBotGitCommit = TalpiBotGit.get().get_last_commit()

        infos = []
        infos.append("תאריך עדכון: " + last_commit.time_changed)
        infos.append("נכתב על ידי: " + last_commit.author)
        infos.append("הודעת עדכון: " + '\n' + last_commit.message)

        return infos
