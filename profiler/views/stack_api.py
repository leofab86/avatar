import boto3
from django.utils import timezone
import time
import requests
from django.conf import settings
from django.http import JsonResponse
from common.errorhandling import request_validation
from common.utils import run_async_coroutine
from common.models import AvatarUser


cloudformation = boto3.client(
    'cloudformation',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)

autoscaling = boto3.client(
    'autoscaling',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)


def _create_stack(user):
    resp = cloudformation.create_stack(
        StackName=f'persistent-stack-{round(time.time())}',
        TemplateURL="https://s3-external-1.amazonaws.com/cf-templates-1m0qfa7x1atb4-us-east-1/2020264R2Q-template1mygctngnuoh",
        Parameters=[
            {
                "ParameterKey": "Subnets",
                "ParameterValue": "subnet-a6c329c0"
            },
            {
                "ParameterKey": "VpcId",
                "ParameterValue": "vpc-231b1d59"
            },
        ],
        ResourceTypes=[
            'AWS::*',
        ],
    )
    stack_id = resp['StackId']
    user.server_group_id = stack_id
    user.server_group_status = 'CREATE_IN_PROGRESS'
    user.save()
    return user


def _delete_stack(stack_id):
    cloudformation.delete_stack(StackName=stack_id)


def _check_stack(stack_id):
    resp = cloudformation.describe_stacks(StackName=stack_id)
    status = resp['Stacks'][0]['StackStatus']
    return_obj = {'status': status, 'address': ''}
    if status == 'CREATE_COMPLETE':
        return_obj['address'] = resp['Stacks'][0]['Outputs'][0]['OutputValue']
        try:
            attempt = requests.get(return_obj['address'], timeout=10)
        except:
            return return_obj

        if attempt.status_code == 200:
            return_obj['status'] = 'READY'
    return return_obj


def _start_timeout(user_model, check_time):
    def stack_timeout():
        minutes = 0
        while minutes <= 40:
            time.sleep(60)
            new_user_model = AvatarUser.objects.get(username=user_model.username)
            if check_time != new_user_model.last_check:
                return
            minutes = minutes + 1
        _delete_stack(user_model.server_group_id)
        user_model.server_group_status = 'DELETE_IN_PROGRESS'
        user_model.save()
    run_async_coroutine(stack_timeout)


@request_validation('GET')
def check_stack(request):
    username = request.user.username
    user_model = AvatarUser.objects.get(username=username)
    return_obj = {
        'username': username,
        'server_group_address': user_model.server_group_address,
        'server_group_status': user_model.server_group_status
    }

    check_time = timezone.now()
    user_model.last_check = check_time
    user_model.save()

    if user_model.server_group_status == 'OFF':
        return JsonResponse(return_obj)

    if user_model.server_group_id != '':
        stack = _check_stack(user_model.server_group_id)
        stack_status = stack['status']
        user_model.server_group_status = stack_status
        user_model.save()
        return_obj['server_group_status'] = stack_status

        if (
            stack_status != 'DELETE_IN_PROGRESS'
            and stack_status != 'DELETE_COMPLETE'
        ):
            _start_timeout(user_model, check_time)

    return JsonResponse(return_obj)


@request_validation('GET')
def check_stack_and_restart(request):
    username = request.user.username
    user_model = AvatarUser.objects.get(username=username)
    return_obj = {
        'username': username,
        'server_group_status': user_model.server_group_status,
        'server_group_address': user_model.server_group_address,
    }
    check_time = timezone.now()
    user_model.last_check = check_time
    user_model.save()

    def create_stack_start_timeout():
        updated_user_model = _create_stack(user_model)
        return_obj['server_group_status'] = updated_user_model.server_group_status
        return_obj['server_group_address'] = ''
        _start_timeout(user_model, check_time)

    if user_model.server_group_id != '':
        stack = _check_stack(user_model.server_group_id)
        stack_status = stack['status']
        return_obj['server_group_address'] = stack.get('server_group_address')
        if (
            stack_status != 'READY'
            and stack_status != 'CREATE_COMPLETE'
            and stack_status != 'CREATE_IN_PROGRESS'
        ):
            create_stack_start_timeout()
    else:
        create_stack_start_timeout()

    return JsonResponse(return_obj)


@request_validation('GET')
def check_stack_and_turn_off(request):
    username = request.user.username
    user_model = AvatarUser.objects.get(username=username)
    stack = _check_stack(user_model.server_group_id)
    stack_status = stack['status']

    if (
        stack_status != 'DELETE_IN_PROGRESS'
        and stack_status != 'DELETE_COMPLETE'
    ):
        _delete_stack(user_model.server_group_id)

    user_model.server_group_status = 'OFF'
    user_model.save()

    return JsonResponse({
        'username': username,
        'server_group_status': 'OFF',
    })
