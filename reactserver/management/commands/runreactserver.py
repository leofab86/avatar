from django.conf import settings
from reactserver.management.commandclasses import SubprocessCommand

run_server = f'cd {settings.REACTSERVER_PATH} ; ' + \
    settings.REACTSERVER_ENV + ' npm run start:server'


class Command(SubprocessCommand):
    help = 'Runs Portfolio reactserver'
    commands = [
        run_server
    ]
