import boto3
import json
import uuid
from datetime import datetime
from moviepy.editor import *

latest_prefix = 'latest'
source_bucket = 'amos-latest-forecast-test'
destination_bucket = 'amos-latest-forecast-test'#make into an environment variable to point at a different bucket

s3 = boto3.client('s3')


def lambda_handler(event, context):

    print('whole event:')
    print(event)

    first_record = event['Records'][0]
    file_name = first_record['s3']['object']['key']

    if not file_name.startswith(latest_prefix):
        print(f'renaming {file_name}')

        if file_name.startswith('audio'):
            print(f'renaming and chaniging volume {file_name}')
            tmp_new_file = get_file_from_s3(file_name)
            print('got {}'.format(tmp_new_file))
            print('creating latest files')
            tmp_audio_file = make_audio_from_new(tmp_new_file)
            print('made {}'.format(tmp_audio_file))
            # write new files to public s3 bucket
            print('writing files to {}'.format(destination_bucket))
            write_file_to_s3(tmp_audio_file)
            print('written {}'.format(tmp_audio_file))
            # file_name = audio_volume(file_name)
        elif file_name.startswith('video'):
            print(f'renaming and chaniging volume {file_name}')
            tmp_new_file = get_file_from_s3(file_name)
            print('got {}'.format(tmp_new_file))
            print('creating latest files')
            tmp_video_file = make_video_from_new(tmp_new_file)
            print('made {}'.format(tmp_video_file))
            # write new files to public s3 bucket
            print('writing files to {}'.format(destination_bucket))
            write_file_to_s3(tmp_video_file)
            print('written {}'.format(tmp_video_file))
            # file_name = video_volume(file_name)
        else:
            print('unexpected file type')
            return

        copy_and_delete_file(file_name)
        print('updating latest json')
        update_latest_json()

    print('FIN')

def make_audio_from_new(file_name):
    tmp_audio_file ='/tmp/' +file_name
    audio_file = AudioFileClip(file_name)
    # audio_file.write_audiofile(tmp_audio_file, verbose=False, progress_bar=False, ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json', '-acodec', 'libmp3lame'])
    audio_file.write_audiofile(tmp_audio_file, verbose=False, progress_bar=False, codec=None, ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json'])
    ptint(f'{tmp_audio_file} changed volume')
    return tmp_audio_file

def make_video_from_new(file_name):
    tmp_video_file ='/tmp/' +file_name
    video_file = VideoFileClip(file_name)
    video_file.write_videofile(tmp_video_file, verbose=False, progress_bar=False, codec='libx264', temp_audiofile='/tmp/temp_audio.mp3', ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json', '-acodec', 'aac'])
    print(f'{tmp_video_file} changed volume')
    return tmp_video_file

def copy_and_delete_file(file_name):
    copy_source = {'Bucket': source_bucket, 'Key': file_name}
    new_key = latest_prefix+'_'+file_name
    s3.copy_object(Bucket=destination_bucket, Key=new_key, CopySource=copy_source, ACL='public-read')
    s3.delete_object(Bucket=source_bucket, Key=file_name)

def get_file_from_s3(file_name):
    tmp_new_file = '/tmp/'+file_name
    print(f'dowloading {file_name} from {source_bucket} to {tmp_new_file}')
    s3.download_file(source_bucket, file_name, tmp_new_file)
    return tmp_new_file

def write_file_to_s3(file_to_write):
    s3.upload_file(file_to_write, destination_bucket, ExtraArgs={'ACL': 'public-read'})

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