import sys
sys.path.append('amos-latest-forecast-copy/src')

from unittest.mock import patch


@patch('boto3.client')
def test_regex(mock_boto3_client):
    from lambda_function import p

    assert p.match('METOFFICE_NATIONAL_MORNING_260918.mp4')
    assert not p.match('METOFFICE_NATIONAL_MIDMORNING_260918.mp4')
