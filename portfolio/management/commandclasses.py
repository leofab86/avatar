from django.core.management.base import BaseCommand

from subprocess import Popen
from sys import stdout, stdin, stderr
import time, os, signal


class SubprocessCommand(BaseCommand):

    def handle(self, *args, **keywargs):
        proc_list = []

        for command in self.commands:
            print('Running: ' + command)
            proc_list.append({
                'command': command,
                'process': Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            })

        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print(' ')
            print('KILLING PROCESSES STARTED BY THESE COMMANDS: ')
            for proc in proc_list:
                print('  ' + proc['command'])
                os.kill(proc['process'].pid, signal.SIGKILL)