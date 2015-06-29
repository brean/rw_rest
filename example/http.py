# -*- coding: utf-8 -*-
"""
server for http_rest example
(file management example)
"""
import rw.http
import rw.routing

from rw_rest.model import Rest, Model
from rw_rest.provider import FileProvider
from . import http_example

root = rw.http.Module('example')
data_root = rw.http.Module('example', 'http_data')

root.mount('/data', data_root)
example_rest = Rest(module=data_root)
example_rest.add_model(model=http_example.Example(data_rest=data_root))

@root.get('/')
def main(handler):
    """show main page"""
    root.render_template("main.html")
