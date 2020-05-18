import asyncio
import json
from django.http import JsonResponse, HttpResponse
from profiler.models import DatabaseProfile
from profiler.serializers import DatabaseProfileSerializer
from reactserver.views import HybridJsonView
from common.errorhandling import handle_database_exceptions, request_validation
from profiler.utils import custom_data_optimization
from common.logging import logerror, Timing
from django.db import connections


class IndexView(HybridJsonView):
    def get_content(self, request):
        try:
            db_profiles = DatabaseProfile.objects.filter(completion_progress=100)

        except DatabaseProfile.DoesNotExist:
            db_profiles = []

        serializer = DatabaseProfileSerializer(db_profiles, many=True)

        return {'db_profiles': serializer.data, 'title': 'Profiler'}


@request_validation(['POST'], expected_body=DatabaseProfileSerializer)
def create_database_profile(request, body):
    try:
        new_profile = DatabaseProfile(**body)
        new_profile.save()
    except Exception as e:
        return handle_database_exceptions(e)

    # Running save_sets inside of a asyncio coroutine makes the expensive save_sets() run much faster (not sure why)
    # and also runs it asynchronously in the background so the simple new_profile can be returned with its
    # db_profile_id and the front end can make subsequent calls to check on the completion_progress of new_profile
    # while save_sets() is running.
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

    return JsonResponse({'db_profile': DatabaseProfileSerializer(new_profile).data})


@request_validation(['GET'])
def check_progress(request, db_profile_id):
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    return JsonResponse({'db_profile': DatabaseProfileSerializer(db_profile).data})


@request_validation(['GET', 'DELETE'])
def database_profile(request, db_profile_id):
    timing = Timing('database_profile')
    timing.start('full_api')
    timing_data = {}
    if request.method == 'DELETE':
        try:
            db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
        except DatabaseProfile.DoesNotExist:
            return HttpResponse(status=404)
        db_profile.delete()
        return HttpResponse(status=200)

    if request.method == 'GET':
        teacher_levels = int(request.GET.get('teacher_levels')) if request.GET.get('teacher_levels') else 0
        class_levels = int(request.GET.get('class_levels')) if request.GET.get('class_levels') else 0
        student_levels = int(request.GET.get('student_levels')) if request.GET.get('student_levels') else 0
        prefetch_related = request.GET.get('prefetch_related')
        custom_optimization = request.GET.get('custom_optimization')

        if custom_optimization:
            db_profile, custom_optimization_timing_data = custom_data_optimization(
                db_profile_id, teacher_levels, class_levels, student_levels
            )
            timing.start('generate_json_response')
            response = JsonResponse({'db_profile': [db_profile]})
            timing_data['generate_json_response'] = timing.end('generate_json_response')
            timing_data['full_api'] = timing.end('full_api')
            timing_data.update(custom_optimization_timing_data)
            response.content = response.content[:-1] + str.encode(', "timing_data":' + json.dumps(timing_data) + '}')
            return response

        prefetch_related_args = ()
        if prefetch_related == "true":
            def generate_prefetch_command(commands):
                return lambda levels: "__".join(commands[:levels])

            prefetch_commands = {
                'teacher': generate_prefetch_command(['teacher_set', 'classes', 'student_set']),
                'class': generate_prefetch_command(['class_set', 'student_set', 'classes']),
                'student': generate_prefetch_command(['student_set', 'classes', 'student_set'])
            }

            if teacher_levels > 0:
                prefetch_related_args = prefetch_related_args + (prefetch_commands['teacher'](teacher_levels),)
            if class_levels > 0:
                prefetch_related_args = prefetch_related_args + (prefetch_commands['class'](class_levels),)
            if student_levels > 0:
                prefetch_related_args = prefetch_related_args + (prefetch_commands['student'](student_levels),)

        try:
            db_profile = DatabaseProfile.objects\
                .filter(db_profile_id=db_profile_id)\
                .prefetch_related(*prefetch_related_args)
        except DatabaseProfile.DoesNotExist:
            return HttpResponse(status=404)

        serializer = DatabaseProfileSerializer(
            db_profile,
            many=True,
            student_levels=student_levels,
            class_levels=class_levels,
            teacher_levels=teacher_levels
        )

        return JsonResponse({'db_profile': serializer.data})

