#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import functools
print = functools.partial(print, flush=True)

SETTINGS_PATH = 'web_framework.server_side.TalpiBotSite.settings'

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_PATH)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print(sys.argv)
    execute_from_command_line(sys.argv)


def create_super_user():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_PATH)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(['manage.py', 'createsuperuser'])

def run_server():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_PATH)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(['manage.py', 'runserver'])


def migrate():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_PATH)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(['manage.py', 'migrate'])


def run_command(cmd):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_PATH)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(['manage.py', cmd])


if __name__ == '__main__':
    main()
