from APIs.ExternalAPIs import GoogleCalendar
from bot_features.Shagmach.Classrooms.DBModels.classroom import *
from bot_features.Shagmach.Classrooms.DBModels.classroom_event import *
from bot_features.Shagmach.Classrooms.Static.class_rooms import class_list, short_name_list
from datetime import datetime


def reset_classroom_db():
    for classroom in Classroom.objects:
        classroom.delete()
    for i in range(len(class_list)):
        classroom = Classroom()
        classroom.name = class_list[i]
        classroom.short_name = short_name_list[i]
        classroom.save()


def reset_event_db(_date):
    for event in ClassroomEvent.objects:
        try:
            if event.classroom not in Classroom.objects:
                event.classroom = Classroom.objects[0]
                event.save()
            event.delete_self()
        except:
            continue

def smart_reset_classroom_db():
    classroom_events = list(ClassroomEvent.objects)
    classes_names = {e: e.classroom.name for e in classroom_events}
    reset_classroom_db()
    classes = {}
    for classroom in Classroom.objects:
        classes[classroom.name] = classroom
    for event in classroom_events:
        classroom_name = classes_names[event]
        if classroom_name in classes:
            event.classroom = classes[classroom_name]
            event.save()

def add_new_classes():
    print(Classroom.objects.names())