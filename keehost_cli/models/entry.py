from .group import Group
from ..config import BASE_URL, TOKEN
from ..model import Model

class Entry(Model):

    """ An Entry is a password document """

    name = ""
    value = ""
    key = ""
    url = ""
    icon = ""
    group = None

    def fields_to_dict(self):
        return {
            'name': self.name,
            'value': self.value,
            'key': self.key,
            'url': self.url,
            'icon': self.icon,
            'group': self.group.id if type(self.group) == Group else self.group
        }

    @classmethod
    def get_headers(cls):
        return {'Authorization': TOKEN}

    @classmethod
    def get_base_url(cls):
        return BASE_URL

    @classmethod
    def get_resource_name(cls):
        return 'entries'

    @classmethod
    def from_response(cls, response):

        """ Build the model from the response """

        entry = Entry()
        entry = cls.get_meta(entry, Model.from_response(response))
        entry.name = response.get('name')
        entry.value = response.get('value')
        entry.key = response.get('key')
        entry.url = response.get('url')
        entry.icon = response.get('icon')
        group = response.get('group')
        if type(group) == dict:
            entry.group = Group.from_response(group)
            pass
        else:
            entry.group = group
