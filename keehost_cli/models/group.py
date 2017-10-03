from ..config import BASE_URL, TOKEN
from ..model import Model


class Group(Model):

    """ An Entry is a password document """

    name = ""
    icon = ""

    def fields_to_dict(self):
        return {
            'name': self.name,
            'icon': self.icon,
        }

    @classmethod
    def get_headers(cls):
        return {'Authorization': TOKEN}

    @classmethod
    def get_base_url(cls):
        return BASE_URL

    @classmethod
    def get_resource_name(cls):
        return 'groups'

    @classmethod
    def from_response(cls, response):

        """ Build the model from the response """

        group = Group()
        group = cls.get_meta(group, Model.from_response(response))
        group.name = response.get('name')
        group.icon = response.get('icon')
        return group
