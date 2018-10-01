import sys
sys.path.append('amos-latest-forecast-copy/src')


def test_regex():
    from lambda_function import p

    assert p.match('METOFFICE_NATIONAL_MORNING_260918.mp4')
    assert not p.match('METOFFICE_NATIONAL_MIDMORNING_260918.mp4')
