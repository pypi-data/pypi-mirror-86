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

class CreateMeetingRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'aliyuncvc', '2019-10-30', 'CreateMeeting','aliyuncvc')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_MeetingName(self):
		return self.get_body_params().get('MeetingName')

	def set_MeetingName(self,MeetingName):
		self.add_body_params('MeetingName', MeetingName)

	def get_UserId(self):
		return self.get_body_params().get('UserId')

	def set_UserId(self,UserId):
		self.add_body_params('UserId', UserId)

	def get_OpenPasswordFlag(self):
		return self.get_body_params().get('OpenPasswordFlag')

	def set_OpenPasswordFlag(self,OpenPasswordFlag):
		self.add_body_params('OpenPasswordFlag', OpenPasswordFlag)

	def get_Password(self):
		return self.get_body_params().get('Password')

	def set_Password(self,Password):
		self.add_body_params('Password', Password)

	def get_MasterEnableFlag(self):
		return self.get_body_params().get('MasterEnableFlag')

	def set_MasterEnableFlag(self,MasterEnableFlag):
		self.add_body_params('MasterEnableFlag', MasterEnableFlag)

	def get_MeetingMode(self):
		return self.get_body_params().get('MeetingMode')

	def set_MeetingMode(self,MeetingMode):
		self.add_body_params('MeetingMode', MeetingMode)