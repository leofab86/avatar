import asyncio
import boto3
import requests
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from profiler.models import DatabaseProfile
from profiler.serializers import DatabaseProfileSerializer
from reactserver.views import HybridJsonView
from common.errorhandling import handle_database_exceptions, request_validation, generate_error_resp
from profiler.utils import custom_data_optimization
from common.logging import logerror, Timing


dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)


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
            timing.start('generate_json')
            response = JsonResponse({'db_profile': [db_profile]})
            timing.end('generate_json')
            timing.end('full_api')
            timing.data['custom_optimization'] = custom_optimization_timing_data
            timing.log_queries()
            timing.add_data_to_response(response)
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

        timing.start('db_profile_query_and_serialize')
        serializer = DatabaseProfileSerializer(
            db_profile,
            many=True,
            student_levels=student_levels,
            class_levels=class_levels,
            teacher_levels=teacher_levels
        ).data
        timing_data_context = 'prefetch_related' if prefetch_related else None
        timing.end('db_profile_query_and_serialize', timing_data_context)

        timing.start('generate_json')
        response = JsonResponse({'db_profile': serializer})
        timing.end('generate_json')
        timing.end('full_api')
        timing.log_queries()
        timing.add_data_to_response(response)
        return response


@request_validation(['POST'])
def load_test_start(request, test_id):
    try:
        dynamodb.put_item(
            TableName='avatarLoadTest',
            Item={
                'test_id': {'S': str(test_id)},
                'completion': {'N': '0'},
                'results': {'S': ''},
            }
        )
    except Exception as e:
        logerror(e)
        return generate_error_resp(code='DYNAMODB ERROR', message='Error communicating with DynamoDb', status=500)

    loop = asyncio.new_event_loop()
    async def run_load_test():
        def try_run_load_test():
            try:
                requests.post(
                    'https://302vob5347.execute-api.us-east-1.amazonaws.com/prod',
                    json={'test_id': str(test_id), 'number_of_tests': 300},
                    headers={'content_type': 'application/json'}
                )
                print('finished load test')
            except Exception as e:
                logerror(e, message=f'avatarLoadTest lambda error')

        loop.run_in_executor(None, try_run_load_test)
    asyncio.run(run_load_test())
    loop.close()

    return JsonResponse({'test_id': test_id})


@request_validation(['GET'])
def load_test_check(request, test_id):
    response = dynamodb.get_item(
        TableName='avatarLoadTest',
        Key={'test_id': {'S': str(test_id)}},
    )
    item = response['Item']
    results = {}
    if item['completion']['N'] == "100":
        results['data'] = []
        results['data'].append(json.loads(item['batch_1']['S']))
        results['data'].append(json.loads(item['batch_2']['S']))
        results['data'].append(json.loads(item['batch_3']['S']))
        results['data'].append(json.loads(item['batch_4']['S']))
        results['data'].append(json.loads(item['batch_5']['S']))
        results['data'].append(json.loads(item['batch_6']['S']))
        results['data'].append(json.loads(item['batch_7']['S']))
        results['data'].append(json.loads(item['batch_8']['S']))
        results['data'].append(json.loads(item['batch_9']['S']))
        results.update(json.loads(item['batch_final']['S']))

    return JsonResponse({
        'load_test': {
            'completion': item['completion']['N'],
            'results': results,
            'test_id': item['test_id']['S']
        }
    })
