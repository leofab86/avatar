import boto3
import requests
import json
import time
from django.conf import settings
from django.http import JsonResponse
from common.errorhandling import request_validation, generate_error_resp
from common.logging import logerror
from common.utils import run_async_coroutine

dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)


@request_validation(['POST'])
def load_test_start(request, test_id):
    dynamodb.create_table(
        TableName=str(test_id),
        KeySchema=[
            {'AttributeName': 'batch', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'batch', 'AttributeType': 'S'},
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    # Test that dynamodb table is ready
    timeout = 20
    count = 0
    successful_query = None
    while count < timeout:
        count += 1
        time.sleep(1)
        try:
            successful_query = dynamodb.query(
                TableName=str(test_id),
                KeyConditionExpression='#_batch_ = :b',
                ExpressionAttributeValues={
                    ':b': {'S': 'b'}
                },
                ExpressionAttributeNames={
                    '#_batch_': 'batch'
                }
            )
        except Exception as e:
            '''do nothing'''

        if successful_query:
            break

    if not successful_query:
        return generate_error_resp(code='DYNAMO_ERROR', message='Error initiating load test', status=400)

    def run_load_test():
        try:
            requests.post(
                'https://302vob5347.execute-api.us-east-1.amazonaws.com/prod',
                json={
                    'test_id': str(test_id),
                    'tests_per_second': 5,
                    'seconds': 5,
                    'preview_config_url': request.body.decode('utf-8')
                },
                headers={'content_type': 'application/json'}
            )
            print('finished load test')
        except Exception as e:
            logerror(e, message=f'avatarLoadTest lambda error')

    run_async_coroutine(run_load_test)

    return JsonResponse({'test_id': test_id})


@request_validation(['GET'])
def load_test_check(request, test_id, batch):
    dynamodb.update_item(
        TableName=str(test_id),
        Key={'batch': {'S': 'status'}},
        UpdateExpression='set latest_status_check=:c',
        ExpressionAttributeValues={
            ':c': {'S': str(time.time() * 1000)},
        }
    )
    response = dynamodb.query(
        TableName=str(test_id),
        KeyConditionExpression='#_batch_ = :b',
        ExpressionAttributeValues={
            ':b': {'S': batch}
        },
        ExpressionAttributeNames={
            '#_batch_': 'batch'
        }
    )
    items = response['Items']
    results = []
    total = None
    completion = 0
    for batch_result in items:
        total = batch_result['total_batches']['N']
        results.append(json.loads(batch_result['data']['S']))

    if total:
        completion = int(int(batch) / int(total) * 100)

    return JsonResponse({
        'load_test': {
            'completion': completion,
            'results': results,
            'test_id': test_id
        }
    })