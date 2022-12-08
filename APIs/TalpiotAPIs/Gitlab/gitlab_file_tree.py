from mongoengine import Document, StringField, ListField, ReferenceField


class GitlabFileTree(Document):
    name = StringField()
    url = StringField()
    children = ListField(ReferenceField('GitlabFileTree'), required=False)
    branch = StringField()

    def to_json(self):
        json_data = {'name': self.name, 'url': self.url}
        if self.children:
            json_data['children'] = [child.to_json() for child in self.children]
        return json_data
