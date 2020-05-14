import asyncio
import json
from django.http import JsonResponse, HttpResponse
from profiler.models import DatabaseProfile
from profiler.serializers import DatabaseProfileSerializer
from reactserver.views import HybridJsonView
from common.errorhandling import handle_database_exceptions, request_validation
from common.logging import logerror, Timing


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


@request_validation(['POST'], expected_body=DatabaseProfileSerializer)
def create_database_profile(request, body):
    try:
        new_profile = DatabaseProfile(**body)
        new_profile.save()
    except Exception as e:
        return handle_database_exceptions(e)

    # Running save_sets inside of a asyncio coroutine makes the expensive save_sets() run much faster (because
    # asyncio coroutines are lightweight and inherently much faster) and also runs it asynchronously in the background
    # so the simple new_profile can be returned with its db_profile_id and the front end can make subsequent calls to
    # check on the completion_progress of new_profile while save_sets() is running.
    loop = asyncio.new_event_loop()
    async def save_sets():
        def try_save_sets():
            try:
                new_profile.save_sets()
            except Exception as e:
                logerror(e, message=f'{new_profile.db_profile_id} save_sets error')
        loop.run_in_executor(None, try_save_sets)
    asyncio.run(save_sets())
    # Closing the loop here causes an error when the async thread completes because it runs some code that checks
    # whether it is already closed. This error doesn't cause any problems because nothing is waiting on the loop.
    # So I prefer the error than potentially leaking resources from not closing the loop?
    # TODO: Figure out how to avoid this
    loop.close()

    response = JsonResponse({
        'db_profile': DatabaseProfileSerializer(new_profile).data
    })

    return response


@request_validation(['GET'])
def check_progress(request, db_profile_id):
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    children = ['teachers', 'classes', 'students'] if db_profile.completion_progress == 100 else None
    serialized = DatabaseProfileSerializer(db_profile, children=children).data
    return JsonResponse({'db_profile': serialized})


@request_validation(['DELETE'])
def delete_database_profile(request, db_profile_id):
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    db_profile.delete()
    return HttpResponse(status=200)
