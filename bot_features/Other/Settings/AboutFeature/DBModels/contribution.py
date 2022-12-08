from __future__ import annotations
from mongoengine import *

from APIs.TalpiotAPIs import User


class Contribution(Document):
    meta = {'collection': 'contributions'}

    user: User = ReferenceField(User, required=True)
    contribution: str = StringField(max_length=200, required=True)

    def __repr__(self):
        return self.user.name + f' ({self.user.mahzor}) ' + ' - ' + self.contribution

    def __str__(self):
        return repr(self)

    @staticmethod
    def create_new_contribution(user: User, contribution: str) -> None:
        contribution = Contribution(user=user, contribution=contribution)
        contribution.save()


def test():
    pass
    # Contribution.create_new_contribution(user=User.objects(name='טופז אנבר')[0], contribution="צוות פיתוח ליבה")
    # Contribution.create_new_contribution(user=User.objects(name='רזיאל גרצמן')[0], contribution="צוות פיתוח ליבה")
    # Contribution.create_new_contribution(user=User.objects(name='ירדן גלפן')[0], contribution="צוות פיתוח ליבה")
    # Contribution.create_new_contribution(user=User.objects(name='תור הדס')[0],
    #                                      contribution="כתיבת פיצ'רים ותרומה לליבת הקוד")
    # Contribution.create_new_contribution(user=User.objects(name='יואב שמעוני')[0], contribution="כתיבת פיצ'רים")
    # Contribution.create_new_contribution(user=User.objects(name="אלון בויאנג'ו")[0], contribution="כתיבת פיצ'רים")


if __name__ == '__main__':
    from settings import load_settings
    from APIs.TalpiotSystem import Vault

    load_settings()
    # Vault.get_vault().connect_to_db()
    test()
