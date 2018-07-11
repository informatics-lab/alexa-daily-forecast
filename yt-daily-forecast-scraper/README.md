
#yt-daily-forecast-scraper
Scrapes the latest forecast video/audio from Youtube and writes it to S3.
Updates the latest.json file in S3 - also serves as the Alexa feed url.

- Not suitable for production as downloading from Youtube is a no-no.

## installation
Clone repo.

Install pytube:
`$ pip install pytube -t`

## deployment

Zip source code:
`$ zip -r yt.zip .`

Replace lambada with zip file.
