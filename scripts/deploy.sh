#!/usr/bin/env bash

#####
# Setup

export REGION='eu-west-1'
export AWS_PROFILE='alexahandover'


#####
# amos-ingest-and-transcode

cd amos-ingest-and-transcode/src
zip -r ../code.zip *
aws lambda --region ${REGION} update-function-code --function-name amos-ingest-and-transcode --zip-file fileb://$PWD/../code.zip
cd ../..

####
# amos-revolume-and-save-as-latest

cd amos-revolume-and-save-as-latest/src
zip -r ../deploy.zip lambda_function.py
aws lambda --region ${REGION} update-function-code --function-name amos-revolume-and-save-as-latest --zip-file fileb://$PWD/../deploy.zip
cd ../..