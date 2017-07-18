import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

# mail sever settings
MAIL_SERVER = 'eriksatie1993@gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



#administrator list
ADMINS = ['eriksatie1993@gmail.com']

# pagination
POSTS_PER_PAGE = 3

#
WHOOSH_BASE = os.path.join(basedir,'search.db')

MAX_SEARCH_RESULTS = 50
# -*- coding: utf-8 -*-
# available languages
LANGUAGES = {
    'en':'English'
}


MSEARCH_INDEX_NAME = 'whoosh_index'
# simple,whoosh
MSEARCH_BACKEND = 'whoosh'
# auto create or update index
MSEARCH_ENABLE = True

