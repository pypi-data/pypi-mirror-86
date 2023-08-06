"""Service for exchanging data with WolkGateway."""
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
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import List
from typing import Optional

from wolk_gateway_module.model.message import Message


class ConnectivityService(ABC):
    """Responsible for exchanging data with WolkGateway."""

    @abstractmethod
    def set_inbound_message_listener(
        self, on_inbound_message: Callable[[Message], None]
    ) -> None:
        """
        Set the callback function to handle inbound messages.

        :param on_inbound_message: Callable that handles inbound messages
        :type on_inbound_message: Callable[[Message], None]
        """
        raise NotImplementedError

    @abstractmethod
    def set_lastwill_message(self, message: Message) -> None:
        """
        Send offline state for module devices on disconnect.

        :param message: Message to be published
        :type message: Message
        """
        raise NotImplementedError

    @abstractmethod
    def add_subscription_topics(self, topics: List[str]) -> None:
        """
        Add subscription topics.

        :param topics: List of topics
        :type topics: List[str]
        """
        raise NotImplementedError

    @abstractmethod
    def remove_topics_for_device(self, device_key: str) -> None:
        """
        Remove topics for device from subscription topics.

        :param device_key: Device identifier
        :type device_key: str
        """
        raise NotImplementedError

    @abstractmethod
    def connected(self) -> bool:
        """
        Return if currently connected.

        :returns: connected
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> Optional[bool]:
        """Establish connection with WolkGateway."""
        raise NotImplementedError

    @abstractmethod
    def reconnect(self) -> Optional[bool]:
        """Reestablish connection with WolkGateway."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> Optional[bool]:
        """Terminate connection with WolkGateway."""
        raise NotImplementedError

    @abstractmethod
    def publish(self, message: Message) -> bool:
        """
        Publish serialized data to WolkGateway.

        :param message: Message to be published
        :type message: Message
        :returns: result
        :rtype: bool
        """
        raise NotImplementedError
