from mongoengine import Document, StringField, ListField, ReferenceField


class TalpiSharedObjectType:
    FILE = "d"
    FOLDER = "folder"


class TalpiSharedObject(Document):
    file_id: str = StringField()
    name: str = StringField()
    tags: list = ListField()
    children: list = ListField(ReferenceField("TalpiSharedObject"), required=False, default=None)

    @staticmethod
    def new_object(file_id: str, name: str, tags: list, children: list = None):
        """
        creates a new TalpiSharedObject
        :param file_id: str - new file_id
        :param name: str - new name
        :param tags: list[str] - list of tags for the object
        :param children: list[TalpiSharedObject] - if the object is a folder, a list the children (can be empty), else None
        :return: the new object
        """
        return TalpiSharedObject(file_id=file_id, name=name, tags=tags, children=children)

    def add_tag(self, tag: str):
        """
        adds a new tag to the object
        :param tag: the tag to add
        :return: None
        """
        # TODO: check input for injection
        self.tags.append(tag)
        self.save()
        return self

    def add_child(self, child: Document, do_save=True):
        """
        adds a new tag to the object
        :param child: new child of folder
        :param do_save: indicates whether to save the object or not
        :return: None
        """
        # TODO: check input for injection
        if self.children is not None and isinstance(child, TalpiSharedObject):
            self.children.append(child)
            if do_save:
                self.save()
        return self
