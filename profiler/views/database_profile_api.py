from django.http import JsonResponse, HttpResponse
from profiler.models import DatabaseProfile
from profiler.serializers import DatabaseProfileSerializer
from common.errorhandling import handle_database_exceptions, request_validation
from .database_profile_custom_optimization import custom_data_optimization
from common.logging import logerror, timing
from common.utils import run_async_coroutine


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
    def save_sets():
        try:
            new_profile.save_sets()
        except Exception as e:
            logerror(e, message=f'{new_profile.db_profile_id} save_sets error')

    run_async_coroutine(save_sets)

    return JsonResponse({'db_profile': DatabaseProfileSerializer(new_profile).data})


@request_validation(['GET'])
def check_progress(request, db_profile_id):
    try:
        db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    except DatabaseProfile.DoesNotExist:
        return HttpResponse(status=404)
    return JsonResponse({'db_profile': DatabaseProfileSerializer(db_profile).data})


@timing(log_queries=True, timing_to_json=True)
@request_validation(['GET', 'DELETE'])
def database_profile(request, db_profile_id, timer):
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
            timer.apply_context('custom_optimization')
            db_profile = custom_data_optimization(
                db_profile_id, teacher_levels, class_levels, student_levels, timer
            )
            with timer.run('generate_json'):
                response = JsonResponse({'db_profile': [db_profile]})
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

        with timer.apply_context('prefetch_related' if prefetch_related else None)\
                .run('db_profile_query_and_serialize'):
            serializer = DatabaseProfileSerializer(
                db_profile,
                many=True,
                student_levels=student_levels,
                class_levels=class_levels,
                teacher_levels=teacher_levels
            ).data

        with timer.run('generate_json'):
            return JsonResponse({'db_profile': serializer})