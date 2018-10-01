import sys
sys.path.append('amos-latest-forecast-rename/src')

from unittest.mock import patch


@patch('boto3.client')
def test_generate_latest_json(mock_boto3_client):
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
