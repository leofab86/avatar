from django.conf import settings
from reactserver.management.commandclasses import SubprocessCommand

install_and_build = f'cd {settings.REACTSERVER_PATH} ; ' + \
    'npm install ; ' + \
    'npm run build:server ; ' + \
    'npm run build:client ; ' + \
    'aws s3 cp /opt/bitnami/apps/django/django_projects/avatar/static/bundle.css s3://avatar-static/ --acl public-read ; ' + \
    'aws s3 cp /opt/bitnami/apps/django/django_projects/avatar/static/client.bundle.js s3://avatar-static/ --acl public-read;'


class Command(SubprocessCommand):
    help = 'Builds Portfolio distribution files'
    commands = [
        install_and_build
    ]
