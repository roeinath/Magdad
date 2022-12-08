from abc import ABC, abstractmethod

from APIs.TalpiotAPIs.User.user import User


class UserConstraint(ABC):
    """
    Represents
    """

    @abstractmethod
    def satisfied(self, user: User):
        pass

    @staticmethod
    def get_users_with_constraint(constraint):
        users = User.objects
        res = []
        for u in users:
            if constraint.satisfied(u):
                res.append(u)
        return res


class AndUserConstraint(UserConstraint):

    def __init__(self, constraints):
        self.constraints = constraints

    def satisfied(self, user: User):
        for constraint in self.constraints:
            if not constraint.satisfied(user):
                return False
        return True


class MachzorConstraint(UserConstraint):

    def __init__(self, machzor):
        self.machzor = machzor

    def satisfied(self, user: User):
        return user.mahzor == self.machzor


class NotUserConstraint(UserConstraint):

    def __init__(self, constraint):
        self.constraint = constraint

    def satisfied(self, user: User):
        return not self.constraint.satisfied(user)


class OrUserConstraint(UserConstraint):

    def __init__(self, constraints: [UserConstraint]):
        self.constraints = constraints

    def satisfied(self, user: User):
        for constraint in self.constraints:
            if constraint.satisfied(user):
                return True
        return False


class RoleUserConstraint(UserConstraint):

    def __init__(self, role):
        self.role = role

    def satisfied(self, user: User):
        return self.role in user.role or "admin" in user.role


class NameUserConstraint(UserConstraint):

    def __init__(self, name):
        self.name = name

    def satisfied(self, user: User):
        return self.name == user.name
