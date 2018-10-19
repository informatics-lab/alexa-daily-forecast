import os
import boto3
import json
import uuid
from datetime import datetime
from moviepy.editor import *
import os

latest_prefix = 'latest'
source_bucket = 'amos-mo-latest-forecast'
destination_bucket = 'amos-mo-latest-forecast'

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
            write_file_to_s3(tmp_audio_file, 'latest_audio.mp3')
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
            write_file_to_s3(tmp_video_file, 'latest_video.mp4')
            print('written {}'.format(tmp_video_file))
            # file_name = video_volume(file_name)
        else:
            print('unexpected file type')
            return

        delete_source_file_from_s3(file_name)
        print('updating latest json')
        update_latest_json()

    print('FIN')

def make_audio_from_new(file_name):
    tmp_audio_file = file_name
    #tmp_audio_file= '/tmp/' +file_name
    audio_file = AudioFileClip(file_name)
    audio_file.write_audiofile(tmp_audio_file, verbose=False, progress_bar=False, ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json', '-acodec', 'libmp3lame'])
    # audio_file.write_audiofile(tmp_audio_file, verbose=False, progress_bar=False, codec=None, ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json'])
    print(f'{tmp_audio_file} changed volume')
    return tmp_audio_file

def make_video_from_new(input_file_path):
    name, ext = os.path.basename(input_file_path).rsplit('.',1)
    outpath = f'/tmp/{name}-loud.{ext}'
    print(f"input={input_file_path}, output={outpath}",  "Exists = ", os.path.exists(input_file_path))
    video_file = VideoFileClip(input_file_path)
    # video_file.write_videofile(outpath, verbose=False, progress_bar=True, codec='libx264', ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json', '-acodec', 'aac'])
    #video_file.write_videofile(outpath, verbose=False, progress_bar=True, codec='libx264', ffmpeg_params=[ '-acodec', 'aac'])
    video_file.write_videofile(outpath, verbose=True, progress_bar=True, codec='libx264',
                                 temp_audiofile='/tmp/temp_audio.mp3', 
                                 ffmpeg_params=['-af', 'loudnorm=I=-14:TP=-3:LRA=11:print_format=json', '-codec', 'libx264', '-acodec', 'aac', '-vcodec', 'libx264'])
    print(f'{outpath} changed volume')
    return outpath

def delete_source_file_from_s3(file_name):
    s3.delete_object(Bucket=source_bucket, Key=file_name)

def get_file_from_s3(file_name):
    tmp_new_file = '/tmp/' +file_name
    print(f' dowloading {file_name} from {source_bucket} to {tmp_new_file}')
    s3.download_file(source_bucket, file_name, tmp_new_file)
    return tmp_new_file

def write_file_to_s3(file_name, key):
    print(f' uploading {file_name} to {destination_bucket}')
    s3.upload_file(file_name, destination_bucket, key, ExtraArgs={'ACL': 'public-read'})

def generate_latest_json():
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.0Z")
    return {
        'uid': str(uuid.uuid4()),
        'titleText': 'UK Met Office Latest Forecast',
        'mainText': '',
        'publishedDate': now,
        'updateDate': now,
        'streamUrl': f'https://s3-eu-west-1.amazonaws.com/{destination_bucket}/latest_audio.mp3',
        'videoUrl': f'https://s3-eu-west-1.amazonaws.com/{destination_bucket}/latest_video.mp4',
        'redirectionUrl': 'https://www.metoffice.gov.uk/public/weather/forecast'
    }


def update_latest_json():
    s3.put_object(Body = json.dumps(generate_latest_json()),
                  Bucket = destination_bucket,
                  Key = 'latest.json',
                  ACL = 'public-read',
                  ContentType = 'application/json')