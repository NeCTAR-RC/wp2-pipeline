#!/usr/bin/env python3
"""
Simple example: pushing messages to the kafka-reporting API.
"""

import json
import os
import platform
import random
import sys
import time
import uuid

import requests

HOSTNAME = platform.node()
SESSION = str(uuid.uuid4())
SCHEMA = "hello-world"

REQUIRED_ENVIRONMENT = ["REPORTING_%s" % suffix
                        for suffix in ["SERVER", "TOPIC", "USERNAME", "TOKEN"]]
MISSING_ENVIRONMENT = [var for var in REQUIRED_ENVIRONMENT
                       if var not in os.environ]


def post(server, topic, username, token, https_verify):
    """Post a single message to the API."""

    url = "https://%s/v1/topic/%s" % (server, topic)

    data = json.dumps([{
        "id": str(uuid.uuid4()),
        "session": SESSION,
        "schema": SCHEMA,
        "version": 1,
        "data": {
            "timestamp": int(time.time()),
            "hostname": HOSTNAME,
            "foo": "bar",
            "bar": 42 * random.random()
        }
    }])

    return requests.post(url,
                         auth=(username, token),
                         headers={"content-type": "application/json"},
                         data=data,
                         verify=https_verify)


if __name__ == "__main__":
    if len(MISSING_ENVIRONMENT) > 0:
        sys.exit("Missing environment variables: %s" %
                 " ".join(MISSING_ENVIRONMENT))

    print(post(os.getenv("REPORTING_SERVER"), os.getenv("REPORTING_TOPIC"),
               os.getenv("REPORTING_USERNAME"), os.getenv("REPORTING_TOKEN"),
               os.getenv("REPORTING_HTTPS_VERIFY", "true").lower() == "true"))
