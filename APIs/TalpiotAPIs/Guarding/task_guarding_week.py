from typing import Dict, List

from APIs.TalpiotAPIs import User, Group
from APIs.TalpiotAPIs.Guarding.task_event import TaskEventData
from mongoengine import *


class TaskGuardingWeekClosingStatus(EmbeddedDocument):
    CLOSING_STATUS = {
        0: 'כל הסופ"ש',
        1: 'מקצר'
    }

    user = ReferenceField(User)
    closing_status = IntField(choices=CLOSING_STATUS.keys())
    only_if_not_guarding = BooleanField()
    carrying_weapon = BooleanField()


class TaskGuardingWeekClosingGroup(EmbeddedDocument):
    group = ReferenceField(Group)
    participants = EmbeddedDocumentListField(TaskGuardingWeekClosingStatus)


class TaskGuardingWeekRule(EmbeddedDocument):
    TASK_TYPES = {
        0: "רגיל",
        1: "רק לנושאי נשק",
        2: "עדיפות למקצרים"
    }

    startTime = DateTimeField()
    endTime = DateTimeField()
    participants = IntField()
    taskType = IntField(choices=TASK_TYPES.keys())


class CountOrPeople(EmbeddedDocument):
    count = IntField()
    taskType = IntField(choices=TaskGuardingWeekRule.TASK_TYPES.keys())
    participants = ListField(ReferenceField(User))


class TaskEventPlan(EmbeddedDocument):
    data = EmbeddedDocumentField(TaskEventData)
    countOrPeople = EmbeddedDocumentField(CountOrPeople)


class TaskGuardingWeek(Document):

    startDate = DateField()
    title = StringField()
    closing = EmbeddedDocumentListField(TaskGuardingWeekClosingGroup)
    schedule = EmbeddedDocumentListField(TaskEventPlan)
    rules = EmbeddedDocumentListField(TaskGuardingWeekRule)
    updated = BooleanField()

    def participants_by_group(self) -> Dict[Group, List[TaskGuardingWeekClosingStatus]]:
        result = dict()

        for group_record in self.closing:
            result[group_record.group] = group_record.participants

        return result

    def get_all_participants(self) -> List[TaskGuardingWeekClosingStatus]:
        users = []
        for group in self.closing:
            users += group.participants

        return users
