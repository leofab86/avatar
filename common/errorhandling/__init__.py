import json
import traceback
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import serializers


def generate_error_resp(*, code, message, status):
    return JsonResponse({'code': code, 'message': message}, status=status)


def generate_error_page(request, *, code, message, status):
    return render(
        request,
        'common/default-error.html',
        {'code': code, 'message': message, 'status': status},
        status=status
    )


def handle_database_exceptions(e):
    if type(e) is ValidationError:
        try:
            message = e.message_dict
        except:
            message = e.messages
        return generate_error_resp(code='VALIDATION_ERROR', message=message, status=400)
    print(type(e))
    print(e)
    traceback.print_exc()
    return generate_error_resp(
        code='DATABASE_ERROR',
        message='There was a problem communicating with the database',
        status=500
    )


def handle_request_validation_error(e, key):
    if type(e) is serializers.ValidationError:
        message = e.get_full_details()
        return generate_error_resp(
            code='VALIDATION_ERROR',
            message={key: list(map(lambda x: x['message'], message))},
            status=400
        )
    print(type(e))
    print(e)
    traceback.print_exc()
    return generate_error_resp(
        code='SERVER_ERROR',
        message='There was a problem processing your request',
        status=500
    )


def request_validation(methods, *, data=None):
    def decorator(func):
        def handler(request, *args, **kwargs):
            if request.method not in methods:
                return HttpResponse(status=405)
            body = json.loads(request.body.decode(encoding='utf-8'))
            if data:
                for key in data:
                    if key not in body:
                        return generate_error_resp(
                            code='VALIDATION_ERROR',
                            message={key: f'request expects required {key} property'},
                            status=400
                        )
                    try:
                        data[key].to_internal_value(body[key])
                    except Exception as e:
                        return handle_request_validation_error(e, key)

            kwargs['body'] = body
            return func(request, *args, **kwargs)
        return handler
    return decorator

