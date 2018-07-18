# dart-daily-forecast-ingester
Triggered by an S3 put object event this lambda expects a video (latest forecast) file to be uploaded to the private ingest bucket.
This lambda will take this video file and create/update the following 3 files in the public latest forecast bucket:  
 - `latest_audio.mp3` - the normalised audio content from video file.
 - `latest_video.mp4` - a copy of the original video file with the audio normalised.
 - `latest.json` - a json file used for the alexa daily briefing feed. 

### building the zip for lambda
Turns out making a lambda deployment package when your using moviepy is non trivial!  
Here are the steps needed to build the package:

 1. spin up an EC2 instance using `Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type`     

 2. ssh onto your box and install Python 3.6 and virtualenv using the following steps:
    * `sudo yum install -y gcc zlib zlib-devel openssl openssl-devel `
    * `wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz `
    * `tar -xzvf Python-3.6.1.tgz `
    * `cd Python-3.6.1 && ./configure && make `
    * `sudo make install `
    * `sudo /usr/local/bin/pip3 install virtualenv `
    
 3. choose the virtual environment that was installed via pip3 /usr/local/bin/virtualenv 
    * `~/shrink_venv source`
    * `~/shrink_venv/bin/activate `
    
 4. install libraries in the virtual environment
	* `pip install moviepy`
	* `pip install requests`

 5. add the contents of lib and lib64 site-packages to your .zip file.  
Note that the following steps assume you used Python runtime version 3.6. If you used version 2.7 you will need to update accordingly.
	* `cd $VIRTUAL_ENV/lib/python3.6/site-packages`
	* `zip -r9 ~/moviepy.zip .`

 6. Add your python code to the .zip file
	* `cd ~`
	* `zip -g moviepy.zip lambda_function.py`

 7. set `IMAGEIO_USERDIR` environment variable to `/tmp` on your lambda to allow image.io write it's necessary files. 
  
### install / deploy
install moviepy locally:
`$ pip install moviepy -t .`

add lambda handler to zip & deploy:
`$ ./deploy.sh`
