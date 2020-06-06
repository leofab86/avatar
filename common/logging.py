import traceback
import time
import json
from django.conf import settings

print_logging = False


def logerror(e, *, message='see traceback'):
    if settings.DEBUG and print_logging:
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
    def __init__(self, label):
        self.time_store = {}
        self.time_list = []
        self.data = {}
        self.label = label

    def _get_name(self, key):
        return f'{self.label}{f" - {key}" if key != "" else ""}'

    def start(self, key=''):
        if settings.DEBUG and print_logging:
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
        return self.time_store[key]

    def end(self, key='', context=None):
        end = time.process_time() - self.time_store[key]
        name = self._get_name(key)
        if settings.DEBUG and print_logging:
            print(f'END: {name}')
            print(end)
            if len(self.time_list) == 1:
                print('**********************************************************')
            print(' ')
        self.time_list.remove(key)
        if context:
            self.data[context] = {key: end}
        else:
            self.data[key] = end
        return end

    def add_data_to_response(self, response):
        response.content = response.content[:-1] + str.encode(', "timing_data":' + json.dumps(self.data) + '}')

