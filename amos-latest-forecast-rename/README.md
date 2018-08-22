# amos-latest-forecast-rename
Triggered by S3 object created events this lambda renames the latest transcoded video (`video.mp4`) and audio (`audio.mp3`) files so they are picked up by alexa requests.
Updates the `latest.json` file `published_dt` and `updated_dt` with time now.
