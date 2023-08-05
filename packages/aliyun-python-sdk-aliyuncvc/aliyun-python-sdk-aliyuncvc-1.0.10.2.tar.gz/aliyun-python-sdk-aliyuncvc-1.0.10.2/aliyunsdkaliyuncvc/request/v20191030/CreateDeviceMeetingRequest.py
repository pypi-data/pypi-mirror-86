# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkaliyuncvc.endpoint import endpoint_data

class CreateDeviceMeetingRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'aliyuncvc', '2019-10-30', 'CreateDeviceMeeting','aliyuncvc')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_MeetingName(self):
		return self.get_body_params().get('MeetingName')

	def set_MeetingName(self,MeetingName):
		self.add_body_params('MeetingName', MeetingName)

	def get_OpenPasswordtag(self):
		return self.get_body_params().get('OpenPasswordtag')

	def set_OpenPasswordtag(self,OpenPasswordtag):
		self.add_body_params('OpenPasswordtag', OpenPasswordtag)

	def get_Token(self):
		return self.get_body_params().get('Token')

	def set_Token(self,Token):
		self.add_body_params('Token', Token)

	def get_Password(self):
		return self.get_body_params().get('Password')

	def set_Password(self,Password):
		self.add_body_params('Password', Password)

	def get_SN(self):
		return self.get_body_params().get('SN')

	def set_SN(self,SN):
		self.add_body_params('SN', SN)