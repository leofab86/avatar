from django.core.management.base import BaseCommand

from subprocess import Popen
from sys import stdout, stdin, stderr, exit


class SubprocessCommand(BaseCommand):
    commands = []

    def handle(self, *args, **keywargs):
        proc_list = []

        for command in self.commands:
            print('RUNNING: ' + command)
            proc = {
                'command': command,
                'process': Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr),
            }
            proc_list.append(proc)

        try:
            for proc in proc_list:
                proc['process'].wait()
                print('COMPLETE: ' + proc['command'])
            exit()

        except KeyboardInterrupt:
            print(' ')
            print('KILLING: ')
            for proc in proc_list:
                print('  ' + proc['command'])
                exit()
