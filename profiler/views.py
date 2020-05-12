from django.http import JsonResponse, HttpResponse
from profiler.models import DatabaseProfile
from profiler.serializers import DatabaseProfileSerializer
from rest_framework import serializers
from reactserver.views import HybridJsonView
from common.errorhandling import handle_database_exceptions, request_validation


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


@request_validation(['POST'])
def create_database_profile(request, *, body):
    new_profile = DatabaseProfile(**body)
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


@request_validation(['DELETE'], data={'db_profile_id': serializers.IntegerField()})
def delete_database_profile(request, *, body):
    db_profile_id = body['db_profile_id']
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    db_profile.delete()
    return HttpResponse(status=200)
