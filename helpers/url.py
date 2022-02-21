from urlparse import urlparse, parse_qs


def check(raw_url, expected_uri, expected_params=None):
    url = urlparse(raw_url)
    url_path = url.path.lower()
    expected_url_path = expected_uri.lower()
    assert url_path == expected_url_path, 'actual uri={0}, expected uri={1}'.format(url_path, expected_url_path)

    if expected_params:
        params_as_lists = dict((k, [str(v)]) for k, v in expected_params.items())
        assert parse_qs(url.query) == params_as_lists, 'query params doesnt match'
    else:
        assert not parse_qs(url.query), 'url has query params when not expected'
