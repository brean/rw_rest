# -*- coding: utf-8 -*-
import json
import tornado.web


class Rest(object):
    def __init__(self, module, models=None):
        """
        basic REST model

        inspired by SAILS JS blueprint API
        http://sailsjs.org/#!/documentation/reference/blueprint-api/
        :param module:
        :param models:
        :return:
        """
        if models:
            self.models = models
        else:
            self.models = {}

        @module.post('/<name:str>')
        def _post(handler, name):
            handler.finish(self.model(name).post(json.loads(handler.request.body)))

        @module.get('/<name:str>')
        def _get_all(handler, name):
            handler.finish(self.model(name).get_all())

        @module.get('/<name:str>/<_id:str>')
        def _get(handler, name, _id):
            handler.finish(self.model(name).get(_id))

        @module.delete('/<name:str>/<_id:str>')
        def _delete(handler, name, _id):
            handler.finish(self.model(name).delete(_id))

    def add_model(self, model, name=None):
        if not name:
            name = model.name
        self.models[name] = model

    def model(self, name):
        """
        get model by name
        :param name: name of the model
        :return:
        """
        if name in self.models:
            return self.models[name]
        else:
            raise tornado.web.HTTPError(404)


class Model(object):
    def __init__(self, provider, name):
        """

        :param provider.Provider provider:
        :param str name:
        :return:
        """
        self.provider = provider
        self.name = name

    def get(self, _id):
        """
        find/get data by id
        :param _id:
        :return:
        """
        if not self.provider.exists(_id):
            raise tornado.web.HTTPError(404)
        return json.dumps(self.provider.load(_id), indent=2)

    def get_all(self):
        """
        find data by filter
        :return:
        """
        return json.dumps(self.provider.find(), indent=2)

    def delete(self, _id):
        if not self.provider.exists(_id):
            raise tornado.web.HTTPError(404)
        data = self.get(_id)
        self.provider.delete(_id)
        return data

    def post(self, data):
        return self.provider.create(data)
