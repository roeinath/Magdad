from mongoengine import *

from APIs.TalpiotAPIs.Constraint.UserConstraint.user_constraint import UserConstraint, RoleUserConstraint, OrUserConstraint


class Feature(Document):
	meta = {'collection': 'features'}

	title: str = StringField(max_length=50)
	command: str = StringField(max_length=50)
	category: str = StringField(max_length=50)
	authorized_roles: [str] = ListField(default=["מתלם"])

	def get_constraint(self) -> UserConstraint:
		"""
		Returns a UserConstraint that will statisfy if the
		user has permission to access this Feature.

		:return: UserConstraint
		"""

		constraints = []
		for role in self.authorized_roles:
			c = RoleUserConstraint(role)
			constraints.append(c) 
		constraint = OrUserConstraint(constraints)

		return constraint
