# amos-latest-forecast-copy
Triggered by S3 object created events this lambda copies the latest national forecast videos from the ingest bucket to the process bucket ready to be transcoded.

This is a necessary step as 'morning' forecast videos are delivered to our bucket in the afternoon of the day before.
This lambda will continually write the created event belonging to this 'morning' file to a queue with a timeout of 15min (max timeout). 
This functionality ends once the hours (UTC) have passed 9pm at which point the 'morning' file is sent for transcoding.

Once a file has been written to the processing bucket to be transcoded a transcoding job is created for that file and the original file is removed. 