# -*- mode:python; coding:utf-8 -*-

# Copyright (c) 2021 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3

from flask import Flask, request, jsonify, Response
from cos import CloudObjectStorage 

app = Flask(__name__)


@app.route("/")
def test_con():
    """
    A basic API to test the connection to the back-end.
    If the status is 200 then the connection is successful
    :return: {message: ''} and status is 200
    """
    resp = jsonify({'message': 'Able to connect to CPL back-end. Use URI (code) to send the file'})
    resp.status_code = 200
    return resp

def get_cos_client():
    cos_endpoint = environ.get('COS_ENDPOINT')
    if not cos_endpoint:
        logger.error('No valid COS endpoint specified')
        return None

    api_key = environ.get('APIKEY')
    if not api_key:
        logger.error('No IAM API key found')
        return None

    cos_bucket = environ.get('COS_BUCKET')
    if not cos_bucket:
        logger.error('Must specify a destination bucket')
        return None

    cos_instance_id = environ.get('COS_INSTANCE_ID')
    if not cos_instance_id:
        logger.error('No COS instance ID found')
        return None
    
    iam_endpoint = environ.get('IAM_ENDPOINT')
    if not iam_endpoint:
        logger.error('No IAM endpoint specified')
        return None

    try:
        cos_client = CloudObjectStorage(
            api_key=api_key,
            instance_id=cos_instance_id,
            iam_endpoint=iam_endpoint,
            cos_endpoint=cos_endpoint,
            cos_bucket=cos_bucket)
        print("client")
    except Exception as ex:
        print(str(ex))
        return None

    return cos_client



@app.route('/result', methods=['GET'])
def process_results():
    """
    This API if used for accepting the code files and run them
    Validates if the file is a valid one and the extension is accepted.
    Once validated it saves the file in the system and executes it.
    The return message is send back in the message
    :return: {message: ''} and status is 201 (400 in-case of Failure)
    """
    query_name = request.args.get("query_name")
    dns_resolver = request.args.get("resolver_0")
    print("query name ", query_name)
    print("resolver ", dns_resolver) 
    result = '{"resolver_1": "192.0.0.1"}'
    client=get_cos_client()
    result=client.get_item(item_name="history.json") 
    return Response(result, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run()
