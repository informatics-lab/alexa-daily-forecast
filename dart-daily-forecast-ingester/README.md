# dart-daily-forecast-ingester
Triggered by an S3 put object event this lambda expects a video (latest forecast) file to be uploaded to the private ingest bucket.
This lambda will take this video file and create/update the following 3 files in the public latest forecast bucket:  
 - `latest_audio.mp3` - the normalised audio content from video file.
 - `latest_video.mp4` - a copy of the original video file with the audio normalised.
 - `latest.json` - a json file used for the alexa daily briefing feed. 

### install / deploy
Install moviepy:
`$ pip install moviepy -t .`

Zip dir:
`$ zip -r dart.zip .`
