# -*- coding: utf-8 -*-

from .models import Group, Entry

class RestClient(object):

    """ The RESTClient class used to interact with the api """

    group = Group
    entry = Entry

    def __init__(self, base_url, token):

        self._base_url = base_url
        self._token = token

