import traceback
import time
import json
from django.conf import settings
from django.db import connections

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


class _Timer(object):
    def __init__(self, label):
        self.time_store = {}
        self.data = {}
        self.label = label

    def __getitem__(self, context):
        outer_self = self

        class TimerWithContext:
            def run(self, key):
                return outer_self.run(key, context)

        return TimerWithContext()

    def run(self, key, context=None):
        outer_self = self

        class TimerContext:
            def __enter__(self):
                outer_self.time_store[key] = time.time() * 1000

            def __exit__(self, exc_type, exc_val, exc_tb):
                location = outer_self.data[context] if context else outer_self.data
                location[key] = time.time() * 1000 - outer_self.time_store[key]

        return TimerContext()

    def apply_context(self, context):
        if context:
            self.data[context] = {}
            return self[context]
        return self

    def log_queries(self):
        self.data['queries'] = {'time': 0}
        queries = connections['profiler'].queries
        self.data['queries']['number'] = len(queries)
        for query in queries:
            self.data['queries']['time'] = self.data['queries']['time'] + float(query['time'])

    def add_data_to_response(self, response):
        response.content = response.content[:-1] + str.encode(', "timing_data":' + json.dumps(self.data) + '}')

    def write_server_timing_headers(self, response, concat_header=None):
        try:
            header = response['Server-Timing'] + ', '
        except:
            header = ''

        for key in self.data:
            if type(self.data[key]) is dict:
                for inner_key in self.data[key]:
                    duration = self.data[key][inner_key]
                    start = self.time_store[inner_key]
                    header = header + f'{inner_key};dur={duration};desc="{inner_key}";start={start}, '
            else:
                duration = self.data[key]
                start = self.time_store[key]
                header = header + f'{key};dur={duration};desc="{key}";start={start}, '

        if concat_header:
            header = header + concat_header

        response['Server-Timing'] = header


def timing(label, *, log_queries=False, timing_to_json=False):
    def decorator(func):
        def handler(request, *args, **kwargs):
            timer = _Timer(label)

            kwargs['timer'] = timer

            with timer.run('full-duration'):
                response = func(request, *args, **kwargs)

            timer.write_server_timing_headers(response)

            if log_queries:
                timer.log_queries()

            if timing_to_json:
                timer.add_data_to_response(response)

            return response
        return handler
    return decorator

