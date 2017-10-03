# -*- coding: utf-8 -*-

import requests
from dateutil.parser import parse

def post_to_query_string(dico):

    """ Transform a dict to a query string
   
        >>> post_to_query_string({'foo': 'bar', 'where': {'foo': 'bar'}})
        ?foo=bar&where={"foo": "bar"}

        :params dico the dico to convert
    """

    querystring = "?"
    for key in dico:
        querystring += "%s=" % key
        if type(dico[key]) == dict:
            querystring += json.dumps(dico[key])
        else:
            querystring += str(dico[key])
        querystring += "&"
    return querystring.rstrip('&')

def merge_dicts(*args, **kwargs):
 
    """ Merge dict into one dict """
 
    final = {}
    for element in args:
        for key in element:
            final[key] = element[key]
    return final

class ModelIterator(object):

    """ Iterate over a list of eve document """

    def __init__(self,
                 max_results,
                 base_url,
                 model_class,
                 resource,
                 params={},
                 headers={}):

        """ Constructor """

        self._max_results = max_results
        self._base_url = base_url
        self._model_class = model_class
        self._resource = resource
        self._documents = []
        self._page = 1
        self._params = params
        self._headers = headers

    def retrieve_documents(self):

        """ Retrieve the list of models """

        params = {
            'max_results': self._max_results,
            'page': self._page,
            **self._params
        }
        try:
            response = requests.get(self._base_url + '/%s%s' % (self._resource, post_to_query_string(params)),
                                    headers=self._headers)
            if response.status_code != 200:
                return False
        except:
            return False
        for item in response.json().get('_items'):
            self._documents.append(self._model_class.from_response(item))
        self._page += 1
        return True

    def __iter__(self):

        """ Iterator: self """

        return self

    def __next__(self):

        """ Called when a new element is asked """

        status = True
        if len(self._documents) == 0:
            status = self.retrieve_documents()
        if not status or len(self._documents) == 0:
            raise StopIteration()
        return self._documents.pop()


class Model(object):

    """ A Eve Model Object """

    _created = None
    _updated = None
    _deleted = False
    _etag = None
    _id = None
    _links = {}
    _status = None

    def __init__(self):

        """ Constructor """

        pass



    @classmethod
    def get_resource_name(cls):

        """ Should return the name of the remote resource as string """

        raise NotImplementedError('Please, implement that method')

    @classmethod
    def get_base_url(cls):

        """ Should return the base api url as string """

        raise NotImplementedError('Please, implement that method')

    @classmethod
    def get_params(cls):

        """ Should return the optional params as dict """

        return {}

    @classmethod
    def get_headers(cls):

        """ Should return the optional headers (Authorization for example) as dict """

        return {}

    def fields_to_dict(self):

        """ Should return a dict with the resource fields .
      
            Will be used to save documents:

                >>> project = Project()
                >>> project.name = 'toto'
                >>> project.save()

            You sould return a dict:
                >>> print(project.fields_to_dict())
                {'name': 'toto'}
        """

        raise NotImplementedError('Please, implement that method')

    @classmethod
    def list(cls, params={}, headers={}):

        """ List all eve documents """

        params = merge_dicts(cls.get_params(), params)
        headers = merge_dicts(cls.get_headers(), headers)
        return ModelIterator(25, cls.get_base_url(), cls, cls.get_resource_name(), params, headers)

    @classmethod
    def find_one(cls, params={}, headers={}):

        """ Find only one element """
        
        items = cls.list(params, headers)
        item = None
        try:
            item = items.__next__()
        except:
            pass
        return item

    @classmethod
    def count(cls, params={}, headers={}):

        """ Count the total items """

        params = merge_dicts(cls.get_params(), params)
        headers = merge_dicts(cls.get_headers(), headers)
        r = requests.get(cls.get_base_url() + '/%s%s' % (cls.get_resource_name(), post_to_query_string(params)),
                         headers=headers)
        if r.status_code == 200:
            return int(r.json().get('_meta', {}).get('total', '0'))
        return 0

    def save(self, headers={}):

        """ Create a new instance of the document """

        params = self.fields_to_dict()
        headers = merge_dicts(self.get_headers(), headers)
        r = requests.post(self.get_base_url() + '/%s' % self.get_resource_name(), json=params, headers=headers)
        if r.status_code == 422:
            print("Unprocessable entity, Check the schema")
        return r.status_code == 201

    @classmethod
    def get(cls, identifier, headers={}):

        """ Retrieve one element by id """

        headers = merge_dicts(cls.get_headers(), headers)
        r = requests.get(cls.get_base_url() + '/%s/%s' % (cls.get_resource_name(), identifier), headers=headers)
        if r.status_code != 200:
            return None
        return cls.from_response(r.json())

    @classmethod
    def update(cls, identifier, etag, params={}, headers={}):

        """ Patch the document """

        headers = {
            'If-Match': etag,
            **headers
        }
        params = merge_dicts(cls.get_params(), params)
        headers = merge_dicts(cls.get_headers(), headers)
        r = requests.patch(cls.get_base_url() + '/%s/%s' % (cls.get_resource_name(), identifier),
                           json=params,
                           headers=headers)
        return r.status_code == 200

    @classmethod
    def delete(cls, identifier, etag, headers={}):

        """ Delete a specified document """

        headers = {
            'If-Match': etag,
            **headers
        }
        headers = merge_dicts(cls.get_headers(), headers)
        r = requests.delete(cls.get_base_url() + '/%s/%s' % (cls.get_resource_name(), identifier),
                            headers=headers)
        return r.status_code == 204

    @classmethod
    def get_meta(cls, child, data):

        """ Retrieve metadata and assign it to the given object 
        
            :param child The child model
            :param data The parent model with the meta data
        """

        child._created = data._created
        child._updated = data._updated
        child._id = data._id
        child._etag = data._etag
        child._deleted = data._deleted
        child._status = data._status
        child._links = data._links
        return child

    @classmethod
    def from_response(cls, response):

        """ This method should return a new instance of Model
            with the correct attributes from response.

            :params response the dict object returned by the requests module json object
        """
        
        m = Model()
        m._created = parse(response.get('_created'))
        m._updated = parse(response.get('_updated'))
        m._id = response.get('_id')
        m._etag = response.get('_etag')
        m._status = response.get('_status')
        m._deleted = response.get('_deleted')
        m._links = response.get('_links')
        return m
