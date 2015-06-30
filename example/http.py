# -*- coding: utf-8 -*-
"""
server for http_rest example
(file management example)
"""
import os
import rw.http
import rw.routing

from rw_rest.model import Rest, Model
from rw_rest.provider import FileProvider


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')

root = rw.http.Module('example')

provider = FileProvider(DATA_PATH)
example = Model(provider=provider, name='example')

example_rest = Rest(module=root)
example_rest.add_model(model=example)


@root.get('/')
def main(handler):
    """show main page"""
    handler['examples'] = example.provider.list()
    root.render_template("main.html")
