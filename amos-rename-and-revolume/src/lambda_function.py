import boto3
import json
import uuid
from datetime import datetime
from moviepy.editor import *

latest_prefix = 'latest'
source_bucket = 'amos-latest-forecast'
destination_bucket = 'amos-latest-forecast-test'#make into an environment variable to point at a different bucket

s3 = boto3.client('s3')


def lambda_handler(event, context):

    print('whole event:')
    print(event)

    first_record = event['Records'][0]
    file_name = first_record['s3']['object']['key']

    if file_name.startswith(latest_prefix):
        print(f'renaming {file_name}')

        if file_name.startswith('audio'):
            file_name = audio_volume(file_name)
        elif file_name.startswith('video'):
            file_name = video_volume(file_name)
        else:
            print('unexpected file type')
            return

        copy_and_delete_file(file_name)
        print('updating latest json')
        update_latest_json()

    print('FIN')

def audio_volume(file_name):
    tmp_audio_file ='/tmp/' +file_name
    audio_file = AudioFileClip(file_name)
    audio_file.write_audio(tmp_audio_file, verbose=False, progress_bar=False, ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json','-acodec','libmp31ame'])
    return tmp_audio_file

def video_volume(file_name):
    tmp_video_file ='/tmp/' +file_name
    video_file = VideoFileClip(file_name)
    video_file.write_audio(tmp_video_file, verbose=False, progress_bar=False, codec='libx264', temp_audiofile='/tmp/temp_audio.mp3', ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json','-acodec','aac'])
    return tmp_video_file

def copy_and_delete_file(file_name):
    copy_source = {'Bucket': source_bucket, 'Key': file_name}
    new_key = latest_prefix+'_'+file_name
    s3.copy_object(Bucket=destination_bucket, Key=new_key, CopySource=copy_source, ACL='public-read')
    s3.delete_object(Bucket=source_bucket, Key=file_name)

def generate_latest_json():
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.0Z")
    return {
        'uid': str(uuid.uuid4()),
        'titleText': 'UK Met Office Latest Forecast',
        'mainText': '',
        'publishedDate': now,
        'updateDate': now,
        'streamUrl': 'https://s3-eu-west-1.amazonaws.com/amos-latest-forecast/latest_audio.mp3',
        'videoUrl': 'https://s3-eu-west-1.amazonaws.com/amos-latest-forecast/latest_video.mp4',
        'redirectionUrl': 'https://www.metoffice.gov.uk/public/weather/forecast'
    }


def update_latest_json():
    s3.put_object(Body = json.dumps(generate_latest_json()),
                  Bucket = destination_bucket,
                  Key = 'latest.json',
                  ACL = 'public-read',
                  ContentType = 'application/json')