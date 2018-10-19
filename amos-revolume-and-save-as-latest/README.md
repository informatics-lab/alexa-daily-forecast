# amos-revolume-and-save-as-latest
Triggered by S3 object created events.
This lambda re-volumes (increases) the audio and video files and renames the as video (`video.mp4`) and audio (`audio.mp3`) files so they are picked up by alexa requests.
Updates the `latest.json` file `published_dt` and `updated_dt` with time now.


Lambda runtime needs updating to ~?? (15min currently)
Lambda mem needs updating to ? (3008Mb currently)
Lambda env var must include:
`IMAGEIO_USERDIR=/tmp`