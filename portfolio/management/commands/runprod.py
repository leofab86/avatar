from django.conf import settings
from portfolio.management.commandclasses import SubprocessCommand


class Command(SubprocessCommand):
    help = 'Builds Portfolio distribution files'
    commands = [
        'cd portfolio/reactserver ; npm run build:server',
        'cd portfolio/reactserver ; npm run build:client',
        'cd portfolio/reactserver ; ' + settings.REACTSERVER_ENV('production') + ' npm run start:server',
        'python manage.py runserver',
    ]
