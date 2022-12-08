import base64


class FileToUpload(object):
    name: str = ''
    type: str = ''
    content: str = ''
    size: int = 0
    last_modified: str = ''

    def __init__(self, name='', file_type='', content='', size=0, last_modified='', url=''):
        self.name = name
        self.type = file_type
        self.content = content
        self.size = size
        self.last_modified = last_modified
        self.url = url

    @staticmethod
    def load_from_json(data):
        # data: dict = json.loads(json_string)
        instance = FileToUpload()
        for attr, value in data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        return instance

    def get_content(self):
        head, data = self.content.split(',')
        decoded = base64.urlsafe_b64decode(data)
        return decoded

    def get_mimetype(self):
        return self.type
