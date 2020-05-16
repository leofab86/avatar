import json
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import serializers
from .logging import logerror


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
    logerror(e, message='handle_database_exceptions')
    return generate_error_resp(
        code='DATABASE_ERROR',
        message='There was a problem communicating with the database',
        status=500
    )


def handle_request_validation_error(e):
    if type(e) is serializers.ValidationError:
        return generate_error_resp(
            code='VALIDATION_ERROR',
            message=e.get_full_details(),
            status=400
        )
    logerror(e, message='handle_request_validation_error')
    return generate_error_resp(
        code='SERVER_ERROR',
        message='There was a problem processing your request',
        status=500
    )


def request_validation(methods, *, expected_body=None):
    def decorator(func):
        def handler(request, *args, **kwargs):
            if request.method not in methods:
                return HttpResponse(status=405)

            if expected_body:
                decoded_body = request.body.decode(encoding='utf-8')
                try:
                    json_body = json.loads(decoded_body)
                except:
                    return generate_error_resp(
                        code='REQUEST_ERROR',
                        message='request body is missing or malformed',
                        status=400
                    )
                try:
                    serializer = expected_body(data=json_body)
                    serializer.is_valid(raise_exception=True)
                except Exception as e:
                    return handle_request_validation_error(e)
                kwargs['body'] = serializer.data

            return func(request, *args, **kwargs)
        return handler
    return decorator

