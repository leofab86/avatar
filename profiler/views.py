import asyncio
from django.http import JsonResponse, HttpResponse
from profiler.models import DatabaseProfile
from profiler.serializers import DatabaseProfileSerializer
from rest_framework import serializers
from reactserver.views import HybridJsonView
from common.errorhandling import handle_database_exceptions, request_validation
from common.logging import Timing


class IndexView(HybridJsonView):
    def get_content(self, request):
        try:
            db_profiles = DatabaseProfileSerializer(
                DatabaseProfile.objects.filter(completion_progress=100),
                many=True,
                children=['teachers', 'classes', 'students']
            ).data
        except DatabaseProfile.DoesNotExist:
            db_profiles = []

        return {'db_profiles': db_profiles, 'title': 'Profiler'}


@request_validation(['POST'])
def create_database_profile(request, *, body):
    new_profile = DatabaseProfile(**body)
    try:
        new_profile.save()

        # The following asyncio implementation is roughly copied from a stack overflow post. I dont at all understand
        # how it works, but, it manages to both run the save_sets work in a separate thread without blocking the
        # view returning the simple profile (before save_sets), and also make the save_sets work MUCH MUCH faster...
        # TODO: Figure this out
        loop = asyncio.new_event_loop()

        async def save_sets():
            loop.run_in_executor(None, new_profile.save_sets)

        loop.run_until_complete(save_sets())

    except Exception as e:
        return handle_database_exceptions(e)

    response = JsonResponse({
        'db_profile': DatabaseProfileSerializer(
            new_profile, children=False
        ).data
    })

    return response


@request_validation(['GET'])
def check_progress(request, db_profile_id, **kwargs):
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    children = ['teachers', 'classes', 'students'] if db_profile.completion_progress == 100 else False
    serialized = DatabaseProfileSerializer(db_profile, children=children).data
    return JsonResponse({'db_profile': serialized})


@request_validation(['DELETE'])
def delete_database_profile(request, db_profile_id, **kwargs):
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    db_profile.delete()
    return HttpResponse(status=200)
