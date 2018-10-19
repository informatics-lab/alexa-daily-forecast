# alexa-daily-forecast [![Build Status](https://travis-ci.com/informatics-lab/alexa-daily-forecast.svg?branch=master)](https://travis-ci.com/informatics-lab/alexa-daily-forecast)
Amazon Alexa Flash Briefing Skill for the UK Met Office daily forecast.

## Skill architecture

![Architecture diagram](https://images.informaticslab.co.uk/misc/6097753f879cc32eac1d20596c01adec.png)

## Lambda functions

These lambdas function as part of the video ingest pipeline.

### amos-ingest-and-transcode

  - ~500mb video files sent to s3 ingest bucket from MO internal infrastructure.
    (morning forecast videos are sent in the afternoon of the day before)
  - files are renamed and copied into processing bucket
    (morning files are delayed until after 9pm by writing to sqs queue with delay)
  - when a video file is written to the processing bucket an elastic transcoder job is created
    to make the audio / video files in the latest-forecast bucket

### amos-latest-forecast-rename

  - when new audio / video files arrive in the latest forecast bucket they are renamed to
    overwrite the previous versions, the latest.json feed file is then updated.
