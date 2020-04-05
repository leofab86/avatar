from django.conf import settings
from portfolio.management.commandclasses import SubprocessCommand


class Command(SubprocessCommand):
    help = 'Runs all dev servers necessary to work on Portfolio app'
    commands = [
        'cd portfolio/reactserver ; npm run build:devserver',
        'cd portfolio/reactserver ; npm run build:devclient',
        'cd portfolio/reactserver ; ' + settings.REACTSERVER_ENV('development') + ' npm run start:server',
        'python manage.py runserver',
    ]
