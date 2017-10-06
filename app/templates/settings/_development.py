# -*- coding: utf-8 -*-
from .common import *
import sys
import os

from django.http import HttpResponse
from io import StringIO
import json


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = True


class NonHtmlDebugToolbarMiddleware(object):
    """
    From Benoss on GitHubGist: https://gist.github.com/Benoss/9592229

    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any non-HTML response in HTML if the request
    has a 'debug' query parameter (e.g. http://localhost/foo?debug).
    Special handling for json (pretty printing) and binary data (only show data length).
    """

    @staticmethod
    def process_response(request, response):
        debug = request.GET.get('debug', 'UNSET')

        if debug != 'UNSET':
            if response['Content-Type'] == 'application/octet-stream':
                new_content = '<html><body>Binary Data, ' \
                    'Length: {}</body></html>'.format(len(response.content))
                response = HttpResponse(new_content)
            elif response['Content-Type'] != 'text/html':
                content = response.content.decode('utf-8')
                try:
                    json_ = json.loads(content)
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse('<html><body><pre>{}'
                                        '</pre></body></html>'.format(content))
        return response


def custom_show_toolbar(self):
    return True
if not 'test' in sys.argv:

    DEBUG_TOOLBAR_PATCH_SETTINGS = True

    INTERNAL_IPS = ('127.0.0.1', '128.91.*.*',)

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'settings.development.NonHtmlDebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'settings.development.custom_show_toolbar'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<%= _.slugify(databaseName) %>',
        'USER': 'django_user',
        'PASSWORD': '1qaz2wsx',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
