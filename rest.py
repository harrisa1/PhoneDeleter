#!/usr/bin/env python

import json
import requests

__author__ = 'evanellis' #modified by Greg Smith


class REST(object):
    """
    Creates compound REST calls and stores session info. Just pass in any string for a name.
    All subsequent calls to the same session object will use a session maintained throughout the life of your use.
    The session will help keep resource use low and facilitate easy storing of cookies.
    This implementation supports JSON and raw text for POST and PUT.
    """
    def __init__(self, session_name):
        self.session_name = session_name

    # This object can hold your cookies!
    s = requests.Session()

    # "app_json" transforms the request body to json
    # GET Formatting
    def get(self, url, headers=None,params=None):
        result = self.s.get(url, headers=headers,params=params)
        #result.raise_for_status()
        return result

    # POST Formatting
    def post(self, url,  data, headers, app_json=False):
        if app_json is False:
            result = self.s.post(url, data=data, headers=headers)
            result.raise_for_status()
            return json.loads(str(result.content, encoding="utf-8"))
        elif app_json is True:
            result = self.s.post(url, data=json.dumps(data), headers=headers)
            result.raise_for_status()
            return json.loads(str(result.content, encoding="utf-8"))

    # POST Formatting
    def post_statusCode(self, url,  data, headers, app_json=False):
        if app_json is False:
            result = self.s.post(url, data=data, headers=headers)
            result.raise_for_status()
            return result.status
        elif app_json is True:
            result = self.s.post(url, data=json.dumps(data), headers=headers)
            #result.raise_for_status()
            return result.status_code
    #return whole object
    def post_object(self, url,  data, headers, app_json=False):
        if app_json is False:
            result = self.s.post(url, data=data, headers=headers)
            result.raise_for_status()
            return result
        elif app_json is True:
            result = self.s.post(url, data=json.dumps(data), headers=headers)
            #result.raise_for_status()
            return result


    # PUT Formatting
    def put(self, url,  data, headers, app_json=False):
        if app_json is False:
            result = self.s.put(url, data=data, headers=headers)
            result.raise_for_status()
            return result.json()
        elif app_json is True:
            result = self.s.put(url, data=json.dumps(data), headers=headers)
            result.raise_for_status()
            return result.json()


    # PUT Formatting
    def put_statusCode(self, url,  data, headers, app_json=False):
        if app_json is False:
            result = self.s.put(url, data=data, headers=headers)
            result.raise_for_status()
            return result.status_code
        elif app_json is True:
            result = self.s.put(url, data=json.dumps(data), headers=headers)
            result.raise_for_status()
            return result.status_code


    def put_object(self, url, data, headers, app_json=False):
        if app_json is False:
            result = self.s.put(url, data=data, headers=headers)
            return result
        elif app_json is True:
            result = self.s.put(url, data=json.dumps(data), headers=headers)
            return result

    # DELETE Formatting
    def delete(self, url, headers=None):
        result = self.s.delete(url, headers=headers)
        result.raise_for_status()
        return result