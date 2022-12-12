from APIs.TalpiotAPIs import User


class MentalDashboardPermissions:
    @staticmethod
    def is_user_admin(user: User):
        """
        Returns whether the user is an admin in the mental dashboard
        :return:
        """
        return user.name in ['יואב פלטו', 'יהלי אקשטיין', 'יואב רפאל סטרוגו']
