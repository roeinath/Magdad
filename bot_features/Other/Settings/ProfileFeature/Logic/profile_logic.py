from APIs.TalpiotAPIs import User


class ProfileLogic:
    @staticmethod
    def get_user_description(user: User) -> [str]:
        messages = [
            '** שם משתמש: **' + user.name,
            '** מספר פלאפון: **' + user.phone_number,
            '** כתובת מייל: **' + user.email,
            '** מחזור:**' + str(user.mahzor)
        ]

        return messages
