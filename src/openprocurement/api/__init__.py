"""Main entry point
"""
import os
import pkg_resources
from pyramid.config import Configurator
from couchdb import Server
from openprocurement.api.design import tenders_all_view

VERSION = pkg_resources.get_distribution(__package__).version


def main(global_config, **settings):
    config = Configurator(settings=settings)
#    config.route_prefix = '/api/0.1'
#    config.include("cornice", route_prefix='/api/0.1')
    config.include("cornice")
    config.route_prefix = '/api/{}'.format(VERSION)
    config.scan("openprocurement.api.views")

    # CouchDB connection
    server = Server()
    config.registry.couchdb_server = server
    db_name = os.environ.get('DB_NAME', settings['couchdb.db_name'])
    if db_name not in server:
        server.create(db_name)
    config.registry.db = server[db_name]

    # sync couchdb views
    tenders_all_view.sync(config.registry.db)

    return config.make_wsgi_app()
