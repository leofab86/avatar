from django.conf import settings
from portfolio.management.commandclasses import SubprocessCommand


class Command(SubprocessCommand):
    help = 'Builds Portfolio distribution files'
    commands = [
        f'cd {settings.REACTSERVER_PATH} ; ' +
        'npm install ; ' +
        'npm run build:server ; ' +
        'npm run build:client'
    ]
