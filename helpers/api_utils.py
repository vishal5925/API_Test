import requests


def get(request_api_uri, token_string=None, params=None):
    res = requests.get(request_api_uri, params=params, headers=dict(Authorization=token_string))
    return res.json() if res.ok else __get_http_error_msg(res)


def post(request_api_uri, token_string=None, params=None, json_body=None):
    res = requests.post(request_api_uri, params=params, headers=dict(Authorization=token_string), json=json_body)
    if res.ok and (res.content == ''):
        return None
    return res.json() if res.ok else __get_http_error_msg(res)


def __get_http_error_msg(res):
    return {
        400: lambda: res.text,
        401: lambda: res.reason,
        500: lambda: res.json()['ExceptionMessage']
    }[res.status_code]()


def post_auth(request_api_uri, json_body, token):
    resp = requests.post(request_api_uri, json=json_body, headers={'Authorization': token, 'content-type': 'application/x-www-form-urlencoded'})
    return resp.json() if resp.ok else __get_http_error_msg(resp)


def post_only(request_api_uri):
    resp = requests.post(request_api_uri)
    return resp.content if resp.ok else __get_http_error_msg(resp)


def post_xml(request_api_uri, xml_body):
    resp = requests.post(request_api_uri, data=xml_body, headers={'Content-Type': 'application/xml'})
    return resp.content if resp.ok else __get_http_error_msg(resp)


def put(request_api_uri, params=None):
    res = requests.put(request_api_uri, params=params)
    return res.status_code


def delete(request_api_uri, json_body):
    res = requests.delete(request_api_uri, json=json_body,headers={'Content-Type': 'application/json'})
    return res.status_code