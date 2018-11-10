from datetime import date
import json
import time
import requests


api_url = "https://www.beeminder.com/api/v1/"


def _result_dict(res):
    if res.status_code == 200:
        return {"success?": True}
    else:
        return {"success?": False,
                "error_message": ("Status: %s\nResponse: %s" %
                                  (res.status_code, res.text))}


def add_datapoint(auth_token, slug, value):
    url = api_url + "users/me/goals/" + slug + "/datapoints.json"
    res = requests.post(url, data={"value": value,
                                   "auth_token": auth_token})
    return _result_dict(res)


def as_datapoint(value, timestamp=None, comment=None):
    if timestamp is None:
        timestamp = time.time()
    if comment is None:
        comment = ""
    requestid = str(date.fromtimestamp(timestamp))
    return {"value": value,
            "timestamp": int(timestamp),
            "comment": comment,
            "requestid": requestid}


def add_datapoints(auth_token, goal_slug, datapoints):
    """post a list of datapoints to beeminder

    each datapoint is a map containing
    * "timestamp" in epoch time
    * "value"
    * "comment"
    * optional "requestid"
    """
    url = api_url + "users/me/goals/" + goal_slug + "/datapoints/create_all.json"
    res = requests.post(url, data={"datapoints": json.dumps(datapoints),
                                   "auth_token": auth_token})
    return _result_dict(res)

