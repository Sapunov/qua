#!/usr/bin/env python3.5

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qua.settings")

application = get_wsgi_application()
