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


def handle_request_validation_error(e, key):
    if type(e) is serializers.ValidationError:
        message = e.get_full_details()
        return generate_error_resp(
            code='VALIDATION_ERROR',
            message={key: list(map(lambda x: x['message'], message))},
            status=400
        )
    logerror(e, message='handle_request_validation_error')
    return generate_error_resp(
        code='SERVER_ERROR',
        message='There was a problem processing your request',
        status=500
    )


# TODO: Model fails to validate in certain cases (use Django Rest or views should use serializers)
def request_validation(methods, *, expected_body=None):
    def decorator(func):
        def handler(request, *args, **kwargs):
            if request.method not in methods:
                return HttpResponse(status=405)

            decoded_body = request.body.decode(encoding='utf-8')

            if decoded_body is not None and len(decoded_body) != 0:
                try:
                    request_body = json.loads(decoded_body)
                except Exception as e:
                    logerror(e, message='request_validation json.loads error')
                    request_body = {}

                if type(request_body) == str:
                    request_body = {}
            else:
                request_body = {}

            if expected_body:
                if decoded_body is None:
                    return generate_error_resp(
                        code='REQUEST_ERROR',
                        message='request body missing',
                        status=400
                    )

                for key in expected_body:
                    if key not in request_body:
                        return generate_error_resp(
                            code='VALIDATION_ERROR',
                            message={key: f'request body expects required {key} property'},
                            status=400
                        )
                    try:
                        # expected_body should be a dict using serializer fields which have the to_internal_value method
                        # that will raise a serializers.ValidationError if request body doesn't match serializer fields
                        expected_body[key].to_internal_value(request_body[key])
                    except Exception as e:
                        return handle_request_validation_error(e, key)

            kwargs['body'] = request_body
            return func(request, *args, **kwargs)
        return handler
    return decorator

