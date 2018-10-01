import sys
sys.path.append('amos-latest-forecast-rename/src')

import unittest.mock as mock


@mock.patch('boto3')
def test_generate_latest_json():
    from lambda_function import generate_latest_json

    latest_json = generate_latest_json()

    assert 'uid' in latest_json
    assert 'titleText' in latest_json
    assert 'mainText' in latest_json
    assert 'publishedDate' in latest_json
    assert 'updateDate' in latest_json
    assert 'streamUrl' in latest_json
    assert 'videoUrl' in latest_json
    assert 'redirectionUrl' in latest_json
