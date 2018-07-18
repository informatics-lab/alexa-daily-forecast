#!/usr/bin/env bash
zip dart.zip lambda_function.py
aws lambda update-function-code --function-name amos-latest-forecast-ingest --zip-file fileb://$PWD/dart.zip
