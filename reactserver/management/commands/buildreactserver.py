from django.conf import settings
from reactserver.management.commandclasses import SubprocessCommand

install_and_build = f'cd {settings.REACTSERVER_PATH} ; ' + \
    'npm install ; ' + \
    'npm run build:server ; ' + \
    'npm run build:client ;'


class Command(SubprocessCommand):
    help = 'Builds Portfolio distribution files'
    commands = [
        install_and_build
    ]
