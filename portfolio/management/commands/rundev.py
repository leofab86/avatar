from django.conf import settings
from portfolio.management.commandclasses import SubprocessCommand


class Command(SubprocessCommand):
    help = 'Runs all dev servers necessary to work on Portfolio app'
    commands = [
        f'cd {settings.REACTSERVER_PATH} ; npm run build:devserver',
        f'cd {settings.REACTSERVER_PATH} ; npm run build:devclient',
        f'cd {settings.REACTSERVER_PATH} ; ' + settings.REACTSERVER_ENV + ' npm run watch:server',
        'python3 manage.py runserver',
    ]
