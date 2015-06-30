# -*- coding: utf-8 -*-
import os
import json
import uuid


class Provider(object):
    """
    default provider - used as interface/abstract
    """
    def exists(self, _id):
        raise NotImplementedError("check if item exists")

    def list(self):
        raise NotImplementedError("get list of items")

    def find(self, filter=None):
        raise NotImplementedError("find by filter")

    def load(self, _id):
        """
        load data for item with id _id
        """
        raise NotImplementedError("load item by id")

    def create(self, _id, data):
        """
        create/override item

        :param data: data you want to store
        :return:
        """
        raise NotImplementedError("create item")

    def delete(self, _id):
        """
        delete item by id

        :param _id:
        :return:
        """
        raise NotImplementedError("delete item")

    def update(self, _id, data):
        """
        update data
        :param _id:
        :param data:
        :return:
        """


class FileProvider(Provider):
    def __init__(self, path, ext='.json', id_key=None):
        self.path = path
        self.ext = ext
        self.id_key = id_key

    def exists(self, _id):
        """
        check, if file exists
        """
        filename = _id + self.ext
        path = os.path.join(self.path, filename)
        return os.path.exists(path)

    def list(self):
        """
        list all files from disc
        """
        ids = []
        for filename in os.listdir(self.path):
            _id, ext = os.path.splitext(filename)
            if ext == self.ext and self.exists(_id):
                ids.append(_id)
        return ids

    def find(self, filter=None):
        """
        find data by filter.
        to keep it simple filtering is only possible in databases, not files
        so we just use the limit key.
        to do more complex tasks (like filtering) you should use a database
        :param filter:
        :return:
        """
        if not filter:
            filter = {}
        limit = filter['limit'] if 'limit' in filter else 30
        data = []
        i = 0
        for filename in os.listdir(self.path):
            i += 1
            if i > limit:
                break
            _id, ext = os.path.splitext(filename)
            data.append(self.load(_id))

        return data

    def load(self, _id):
        """
        load data from disc
        """
        path = os.path.join(self.path, _id+self.ext)
        return json.loads(file(path, 'r').read())

    def create(self, data, _id):
        """
        create/override file
        :param data: data you want to store in the file
        :return:
        """
        if not _id:
            if self.id_key:
                _id = data[self.id_key]
            else:
                _id = uuid.uuid1()
        path = os.path.join(self.path, _id+self.ext)
        f = file(path, 'w')
        f.write(json.dumps(data, indent=2))
        f.close()

    def delete(self, _id):
        """
        delete data file from disc
        :param _id:
        :return:
        """
        path = os.path.join(self.path, _id+self.ext)
        os.remove(path)
