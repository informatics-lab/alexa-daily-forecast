import boto3
import json
import uuid
from datetime import datetime

latest_prefix = 'latest'
source_bucket = 'amos-latest-forecast'
destination_bucket = 'amos-latest-forecast'

s3 = boto3.client('s3')


def lambda_handler(event, context):

    print('whole event:')
    print(event)

    first_record = event['Records'][0]
    file_name = first_record['s3']['object']['key']

    if not file_name.startswith(latest_prefix):
        print(f'renaming {file_name}')
        copy_and_delete_file(file_name)
        print('updating latest json')
        update_latest_json()

    print('FIN')


def copy_and_delete_file(file_name):
    copy_source = {'Bucket': source_bucket, 'Key': file_name}
    new_key = latest_prefix+'_'+file_name
    s3.copy_object(Bucket=destination_bucket, Key=new_key, CopySource=copy_source, ACL='public-read')
    s3.delete_object(Bucket=source_bucket, Key=file_name)


def update_latest_json():
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.0Z")
    latest = {
        'uid': str(uuid.uuid4()),
        'titleText': 'UK Met Office Latest Forecast',
        'mainText': '',
        'publishedDate': now,
        'updateDate': now,
        'streamUrl': 'https://s3-eu-west-1.amazonaws.com/amos-latest-forecast/latest_audio.mp3',
        'videoUrl': 'https://s3-eu-west-1.amazonaws.com/amos-latest-forecast/latest_video.mp4',
        'redirectionUrl': 'https://www.metoffice.gov.uk/public/weather/forecast'
    }
    s3.put_object(Body = json.dumps(latest),
                  Bucket = destination_bucket,
                  Key = 'latest.json',
                  ACL = 'public-read',
                  ContentType = 'application/json')