"""Stub method for getting current device status."""
#   Copyright 2019 WolkAbout Technology s.r.o.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from wolk_gateway_module.model.device_status import DeviceStatus


def get_device_status(device_key: str) -> DeviceStatus:
    """
    Get current device status.

    :param device_key: Device identifier
    :type device_key: str
    :returns: status
    :rtype: DeviceStatus
    """
    raise NotImplementedError
