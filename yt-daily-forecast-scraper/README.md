# yt-daily-forecast-scraper
Triggered by CloudWatch events this lambda will scrape the youtube daily forecast playlist xml feed. 
Checking against the public bucket's `latest.json` file if the feed has a different first entry this lambda will 
create/update the following three files:   
 - `latest_audio.mp3` - audio content from youtube latest video.
 - `latest_video.mp4` - youtube latest video.
 - `latest.json` - a json file used for the alexa daily briefing feed.
 
This functionality is only intended for use as a proof of concept.
 
### install / deploy
Install pytube:
`$ pip install pytube -t .`

Zip dir:
`$ zip -r yt.zip .`
