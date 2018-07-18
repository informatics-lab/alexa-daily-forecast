# imports
from pytube import YouTube
import urllib.request
import xml.etree.ElementTree as ET
import json
import boto3

# constants
S3_URL = 'https://s3-eu-west-1.amazonaws.com'
BUCKET_NAME = 'youtube-daily-forecast'
LATEST_KEY = 'latest.json'
YT_PLAYLIST_ID = 'PLGVVqeJodR_Zew9xGAqYVtGjYHau-E2yL'
YT_FEED = 'https://www.youtube.com/feeds/videos.xml?playlist_id='
YT_URL = YT_FEED + YT_PLAYLIST_ID

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    main()


def main():
    s3_latest = get_s3_latest()
    yt_latest = get_yt_latest()
    if s3_latest is None or not is_latest(s3_latest, yt_latest):
        print("updating latest forecast")
        dl_yt_assets(yt_latest['url'])
        write_file_to_s3('latest_audio.mp4')
        write_file_to_s3('latest_video.mp4')
        write_json_to_s3('latest.json')
    else:
        print("current is latest, skipping update")
    print("FIN")


def get_s3_latest():
    try:
        latest_url = S3_URL + '/' + BUCKET_NAME + '/' + LATEST_KEY
        contents = urllib.request.urlopen(latest_url).read().decode('ascii')
        s3_latest = json.loads(contents)
        return s3_latest
    except:
        return None


def get_yt_latest():
    '''gets the latest video info from the yt playlist rss feed'''
    yt_playlist_rss_feed = urllib.request.urlopen(YT_URL).read().decode('ascii')
    xml_root_element = ET.fromstring(yt_playlist_rss_feed)
    xml_latest_entry = xml_root_element.find('{http://www.w3.org/2005/Atom}entry')
    uid = xml_latest_entry.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
    title = xml_latest_entry.find('{http://www.w3.org/2005/Atom}title').text
    published_dt = xml_latest_entry.find('{http://www.w3.org/2005/Atom}published').text.replace('+00:00', '.0Z')
    updated_dt = xml_latest_entry.find('{http://www.w3.org/2005/Atom}updated').text.replace('+00:00', '.0Z')
    url = xml_latest_entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
    latest = {
        'uid': uid,
        'titleText': title,
        'mainText': '',
        'publishedDate': published_dt,
        'updateDate': updated_dt,
        'streamUrl': 'https://s3-eu-west-1.amazonaws.com/youtube-daily-forecast/latest_audio.mp4',
        'videoUrl': 'https://s3-eu-west-1.amazonaws.com/youtube-daily-forecast/latest_video.mp4',
        'redirectionUrl': 'https://www.metoffice.gov.uk/public/weather/forecast',
        'url': url
    }
    with open('/tmp/'+LATEST_KEY, 'w') as file:
        file.write(json.dumps(latest))
    return latest


def is_latest(s3_latest, yt_latest):
    is_latest = False
    if s3_latest['uid'] == yt_latest['uid']:
        is_latest = True
    return is_latest


def dl_yt_assets(url):
    '''downloads the youtube video and audio assets'''

    yt = YouTube(url)
    video_file = dl_yt_video(yt)
    audio_file = dl_yt_audio(yt)
    return [video_file, audio_file]


def dl_yt_video(yt):
    file = 'latest_video'
    yt.streams.first().download(output_path='/tmp', filename=file)
    return file


def dl_yt_audio(yt):
    file = 'latest_audio'
    yt.streams.filter(only_audio=True, subtype='mp4').first().download(output_path='/tmp', filename=file)
    return file


def write_file_to_s3(filename):
    s3.meta.client.upload_file('/tmp/'+filename, BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read'})


def write_json_to_s3(filename):
    s3.meta.client.upload_file('/tmp/'+filename, BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read', 'ContentType': 'application/json'})
