import json
import traceback
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from profiler.models import DatabaseProfile
from profiler.serializers import DatabaseProfileSerializer
from reactserver.views import HybridJsonView

# TODO: Move error handling to better location
def generate_error_resp(*, code, message, status):
    return JsonResponse({'code': code, 'message': message}, status=status)


def handle_database_exceptions(e):
    if type(e) is ValidationError:
        try:
            message = e.message_dict
        except:
            message = e.messages
        return generate_error_resp(code='VALIDATION_ERROR', message=message, status=422)
    print(type(e))
    print(e)
    traceback.print_exc()
    return generate_error_resp(
        code='DATABASE_ERROR',
        message='There was a problem communicating with the database',
        status=500
    )


class IndexView(HybridJsonView):
    def get_content(self, request):
        try:
            db_profiles = DatabaseProfileSerializer(
                DatabaseProfile.objects.all(),
                many=True,
                recursive_children=['teachers', 'classes', 'students']
            ).data
        except DatabaseProfile.DoesNotExist:
            db_profiles = []

        return {'db_profiles': db_profiles, 'title': 'Profiler'}


def create_database_profile(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    database_profile_data = json.loads(request.body.decode(encoding='utf-8'))
    new_profile = DatabaseProfile(**database_profile_data)
    try:
        new_profile.save()
    except Exception as e:
        return handle_database_exceptions(e)

    print('START SERIALIZATION')

    return JsonResponse({
        'db_profile': DatabaseProfileSerializer(
            new_profile, recursive_children=['teachers', 'classes', 'students']
        ).data
    })


def delete_database_profile(request):
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    body = json.loads(request.body.decode(encoding='utf-8'))
    try:
        db_profile_id = body['db_profile_id']
    except Exception as e:
        print(type(e))
        print(e)
        traceback.print_exc()
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    db_profile.delete()
    return HttpResponse(status=200)
