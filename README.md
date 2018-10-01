# alexa-daily-forecast
Amazon Alexa Flash Briefing Skill for the UK Met Office daily forecast.

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


