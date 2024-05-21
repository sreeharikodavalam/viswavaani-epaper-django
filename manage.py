#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import psycopg2


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viswavaani.settings')
    try:
        from django.core.management import execute_from_command_line
        psycopg2.connect('postgres://avnadmin:AVNS_cvGTRncFoo9hx-h2cfE@pg-1da7257b-nichedesignz-3afe.h.aivencloud.com:21261/defaultdb?sslmode=require')

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
