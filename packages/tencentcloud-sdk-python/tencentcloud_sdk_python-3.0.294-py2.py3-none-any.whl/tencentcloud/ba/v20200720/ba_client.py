# -*- coding: utf8 -*-
# Copyright (c) 2017-2018 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.ba.v20200720 import models


class BaClient(AbstractClient):
    _apiVersion = '2020-07-20'
    _endpoint = 'ba.tencentcloudapi.com'


    def CreateWeappQRUrl(self, request):
        """创建渠道备案小程序二维码

        :param request: Request instance for CreateWeappQRUrl.
        :type request: :class:`tencentcloud.ba.v20200720.models.CreateWeappQRUrlRequest`
        :rtype: :class:`tencentcloud.ba.v20200720.models.CreateWeappQRUrlResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateWeappQRUrl", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateWeappQRUrlResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)