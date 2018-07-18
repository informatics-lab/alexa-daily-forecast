# imports
import json
import boto3
import uuid
import datetime
from moviepy.editor import *


# constants
NEW_FILE = 'new_video.mp4'
AUDIO_FILE = 'latest_audio.mp3'
VIDEO_FILE = 'latest_video.mp4'
JSON_FILE = 'latest.json'
INGEST_BUCKET_NAME = 'amos-latest-forecast-ingest'
LATEST_BUCKET_NAME = 'amos-latest-forecast'
S3 = boto3.resource('s3')


def lambda_handler(event, context):
    #extract file name from event
    key = event['Records'][0]['s3']['object']['key']
    print('updating latest forecast to {}'.format(key))
    main(key)


def main(new_key):
    #get new file from ingest bucket
    print('getting {} from {}'.format(new_key, INGEST_BUCKET_NAME))
    tmp_new_file = get_file_from_s3(new_key)
    print('got {}'.format(tmp_new_file))

    #create audio & video from new file normalizing audio
    print('creating latest files')
    tmp_audio_file = make_audio_from_new(tmp_new_file)
    print('made {}'.format(tmp_audio_file))
    tmp_video_file = make_video_from_new(tmp_new_file)
    print('made {}'.format(tmp_video_file))
    tmp_json_file = make_latest_json()
    print('made {}'.format(tmp_json_file))

    #write new files to public s3 bucket
    print('writing files to {}'.format(LATEST_BUCKET_NAME))
    write_file_to_s3(tmp_audio_file, AUDIO_FILE)
    print('written {}'.format(tmp_audio_file))
    write_file_to_s3(tmp_video_file, VIDEO_FILE)
    print('written {}'.format(tmp_video_file))
    write_json_to_s3(tmp_json_file, JSON_FILE)
    print('written {}'.format(tmp_json_file))

    print('FIN')


def make_audio_from_new(new_file_name):
    tmp_audio_file = '/tmp/'+AUDIO_FILE
    audio_file = AudioFileClip(new_file_name)
    audio_file.write_audiofile(tmp_audio_file, verbose=False, progress_bar=False, ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json', '-acodec', 'libmp3lame'])
    return tmp_audio_file


def make_video_from_new(new_file_name):
    tmp_video_file = '/tmp/'+VIDEO_FILE
    video_file = VideoFileClip(new_file_name)
    video_file.write_videofile(tmp_video_file, verbose=False, progress_bar=False, codec='libx264', temp_audiofile='/tmp/temp_audio.mp3', ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json', '-acodec', 'aac'])
    return tmp_video_file


def make_latest_json():
    now = datetime.datetime.now()
    latest = {
        'uid': str(uuid.uuid4()),
        'titleText': 'UK Met Office Latest Forecast',
        'mainText': '',
        'publishedDate': now.strftime('%Y-%m-%dT%H:%M:%S.0Z'),
        'updateDate': now.strftime('%Y-%m-%dT%H:%M:%S.0Z'),
        'streamUrl': 'https://s3-eu-west-1.amazonaws.com/'+LATEST_BUCKET_NAME+'/'+AUDIO_FILE,
        'videoUrl': 'https://s3-eu-west-1.amazonaws.com/'+LATEST_BUCKET_NAME+'/'+VIDEO_FILE,
        'redirectionUrl': 'https://www.metoffice.gov.uk/public/weather/forecast'
    }
    tmp_json_file = '/tmp/'+JSON_FILE
    with open(tmp_json_file, 'w+') as file:
        file.write(json.dumps(latest))
    return tmp_json_file


def get_file_from_s3(file_name):
    tmp_new_file = '/tmp/'+NEW_FILE
    S3.Bucket(INGEST_BUCKET_NAME).download_file(file_name, tmp_new_file)
    return tmp_new_file


def write_file_to_s3(file_to_write, key):
    S3.meta.client.upload_file(file_to_write, LATEST_BUCKET_NAME, key, ExtraArgs={'ACL': 'public-read'})


def write_json_to_s3(file_to_write, key):
    S3.meta.client.upload_file(file_to_write, LATEST_BUCKET_NAME, key, ExtraArgs={'ACL': 'public-read', 'ContentType': 'application/json'})