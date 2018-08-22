import re
import json
import boto3
from datetime import datetime

p = re.compile('METOFFICE_NATIONAL_MORNING_(\d)+.mp4')

delay_queue_url = 'https://sqs.eu-west-1.amazonaws.com/536099501702/amos-latest-forecast-morning-queue'
source_bucket = 'amos-latest-forecast-ingest'
destination_bucket = 'amos-latest-forecast-process'

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
et = boto3.client('elastictranscoder')


def lambda_handler(event, context):

    print('whole event:')
    print(event)

    first_record = event['Records'][0]
    file_name = None

    # if event started from s3
    if first_record['eventSource'] == 'aws:s3':
        file_name = first_record['s3']['object']['key']

    # else if event started from sqs
    elif first_record['eventSource'] == 'aws:sqs':
        first_record = json.loads(first_record['body'])
        file_name = first_record['s3']['object']['key']

    else:
        print('unexpected event source!')
        return None

    # we have the filename variable set
    print('filename: '+file_name)

    # if file name is a 'morning' file
    if p.match(file_name):

        now = datetime.utcnow()
        if now.hour >= 21:
            # copy to process bucket
            print(f'sending {file_name} for transcoding')
            copy_and_delete_file(file_name)
            create_et_job()

        else:
            # write morning file event to delay queue
            print(f'sending {file_name} event to delay queue')
            sqs.send_message(QueueUrl=delay_queue_url, MessageBody=json.dumps(first_record), DelaySeconds=900)

    else:
        # copy to bucket
        print(f'sending {file_name} for transcoding')
        copy_and_delete_file(file_name)
        create_et_job()

    return 'FIN'


def copy_and_delete_file(file_name):
    copy_source = {'Bucket': source_bucket, 'Key': file_name}
    s3.copy_object(Bucket=destination_bucket, Key='latest_video.mp4', CopySource=copy_source)
    return s3.delete_object(Bucket=source_bucket, Key=file_name)


def create_et_job():
    et.create_job(
        PipelineId='1534851042735-45b91m',
        Input={
            'Key': 'latest_video.mp4'
        },
        Outputs=[
            {
                'Key': 'video.mp4',
                'PresetId': '1351620000001-000001'
            },
            {
                'Key': 'audio.mp3',
                'PresetId': '1351620000001-300010'
            }
        ])