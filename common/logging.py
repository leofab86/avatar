import traceback
import time
from django.conf import settings


def logerror(e, *, message='see traceback'):
    if settings.DEBUG:
        print(' ')
        print('**********************************************************')
        print(f'ERROR: {message}')
        print('**********************************************************')
        print(f'ERROR TYPE: {type(e)}')
        print(f'PRINT ERROR: {e}')
        print('TRACEBACK:')
        traceback.print_exc()
        print('**********************************************************')
        print(' ')


class Timing(object):
    time_store = {}
    time_list = []

    def __init__(self, label):
        self.label = label

    def _get_name(self, key):
        return f'{self.label}{f" - {key}" if key != "" else ""}'

    def start(self, key=''):
        if settings.DEBUG:
            name = self._get_name(key)
            if len(self.time_list) == 0:
                print(' ')
                print('**********************************************************')
                print(f'LOG TIME START: {name}')
                print(' ')
            else:
                print(f'START: {name}')
                print(' ')
        self.time_list.append(key)
        self.time_store[key] = time.process_time()

    def end(self, key=''):
        end = time.process_time() - self.time_store[key]
        name = self._get_name(key)
        if settings.DEBUG:
            print(f'END: {name}')
            print(end)
            if len(self.time_list) == 1:
                print('**********************************************************')
            print(' ')
        self.time_list.remove(key)
        return end
