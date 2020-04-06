from django.conf import settings
from portfolio.management.commandclasses import SubprocessCommand


class Command(SubprocessCommand):
    help = 'Builds Portfolio distribution files and runs reactserver'
    commands = [
        'cd portfolio/reactserver ;' +
        'npm run build:server ; ' +
        'npm run build:client ; ' +
        'python3 manage.py collectstatic ; ' +
        settings.REACTSERVER_ENV('production') + ' npm run start:server',
    ]
