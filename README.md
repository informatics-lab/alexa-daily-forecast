# alexa-daily-forecast
Amazon Alexa Flash Briefing Skill for the UK Met Office daily forecast.

## dart-daily-forecast-ingest
*No Longer Used*  
This lambda listens for s3 created events on a bucket for video files.
It downloads `ffmpeg` wih `moviepy` (needs an environment variable) and transcodes the an audio and video file from the source normalising the audio.
The transcoded files are put into a new bucket overwriting the alexa audio and video files for that feed. 

## yt-daily-forecast-scraper
*No Longer Used*
This lambda was triggered by a cloudwatch event (30 min rule).
It scraped the MO youtube feed for the latest forecast video in the playlist and downloaded the audio and video files accordingly.
The files are put into a bucket overwriting the alexa audio and video files for that feed.

## amos-latest-forecast-copy / amos-latest-forecast-rename  

These lambdas function as part of the video ingest pipeline.

  - ~500mb video files sent to s3 ingest bucket from MO internal infrastructure.
    (morning forecast videos are sent in the afternoon of the day before)
  - files are renamed and copied into processing bucket
    (morning files are delayed until after 9pm by writing to sqs queue with delay)
  - when a video file is written to the processing bucket an elastic transcoder job is created 
    to make the audio / video files in the latest-forecast bucket
  - when new audio / video files arrive in the latest forecast bucket they are renamed to 
    overwrite the previous versions, the latest.json feed file is then updated.    

 
