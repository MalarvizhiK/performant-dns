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

import logging

from ibm_boto3.session import Session
from ibm_botocore.client import Config, ClientError
from pathlib import PurePath

logger = logging.getLogger()

class CloudObjectStorage:
    def __init__(self, api_key=None, instance_id=None, iam_endpoint=None,
                 cos_endpoint=None, cos_bucket=None):
        try:
            self.cos_endpoint = cos_endpoint
            self.session = Session(
                ibm_api_key_id=api_key,
                ibm_service_instance_id=instance_id,
                ibm_auth_endpoint=iam_endpoint)
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("Unable to Init CloudObjectStorage: {0}".format(e))
        self.cos_bucket = cos_bucket

    # Method to get the item contents
    def get_item(self, item_name=None):
        try:
            cos = self.session.resource(
                service_name='s3',
                endpoint_url=self.cos_endpoint,
                config=Config(signature_version='oauth')
            )
            response = cos.Object(self.cos_bucket, item_name).get()['Body'].read()
            return response
        except ClientError as be:
            logger.error("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            logger.exception("Unable to get items from COS: {0}".format(e))


class COSError(Exception):
    """Exception class for errors when interacting with COS."""
    pass
