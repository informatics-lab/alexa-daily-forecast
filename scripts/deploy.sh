#!/usr/bin/env bash

#####
# Setup

export REGION='eu-west-1'

#####
# amos-latest-forecast-rename

#cd amos-latest-forecast-rename
#zip -r code.zip lambda_function.py
#aws lambda --region ${REGION} update-function-code --function-name amos-latest-forecast-rename --zip-file fileb://$PWD/code.zip
#cd ..


#####
# amos-latest-forecast-copy

#cd amos-latest-forecast-copy
#zip -r code.zip lambda_function.py
#aws lambda --region ${REGION} update-function-code --function-name amos-latest-forecast-copy --zip-file fileb://$PWD/code.zip
#cd ..

####
# amos-rename-and-revolume

cd amos-rename-and-revolume
cd src 
zip -r ../deploy.zip lambda_function.py
aws lambda --region ${REGION} update-function-code --function-name amos-rename-and-revolume --zip-file fileb://$PWD/../deploy.zip
cd ../..