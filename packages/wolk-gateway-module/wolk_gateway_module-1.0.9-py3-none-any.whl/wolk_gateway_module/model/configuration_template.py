"""Configuration template for registering device on WolkAbout IoT Platform."""
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
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from wolk_gateway_module.model.data_type import DataType


class ConfigurationTemplate:
    """
    Configuration template for registering device on Platform.

    :ivar data_type: Configuration data type
    :vartype data_type: DataType
    :ivar default_value: Default value of configuration
    :vartype default_value: str or None
    :ivar description: Description of configuration
    :vartype description: str or None
    :ivar labels: Labels of fields when data size > 1
    :vartype labels: List[str] or None
    :ivar name: Configuration name
    :vartype name: str
    :ivar reference: Unique configuration reference
    :vartype reference: str
    :ivar size: Data size
    :vartype size: int
    """

    def __init__(
        self,
        name: str,
        reference: str,
        data_type: DataType,
        description: Optional[str] = None,
        size: int = 1,
        labels: Optional[List[str]] = None,
        default_value: Optional[str] = None,
    ):
        """
        Configuration template for device registration request.

        :param name: Configuration name
        :type name: str
        :param reference: Configuration reference
        :type reference: str
        :param data_type: Configuration data type
        :type data_type: DataType
        :param description: Configuration description
        :type description: Optional[str]
        :param size: Configuration data size (max 3)
        :type size: Optional[int]
        :param labels: List of string lables when data size > 1
        :type labels: Optional[List[str]]
        :param default_value: Default configuration value
        :type default_value: Optional[str]
        """
        self.name: str = name
        self.reference: str = reference
        self.description: Optional[str] = description

        self.default_value: Optional[str] = default_value
        if size < 1 or size > 3:
            raise ValueError("Size can only be 1, 2 or 3")
        if size == 1:
            self.size: int = 1
            self.labels: Optional[List[str]] = None
        else:
            self.size = size
            if not labels:
                raise ValueError("Lables must be provided for size > 1")
            self.labels = labels
        if not isinstance(data_type, DataType):
            raise ValueError("Invalid data type given")
        self.data_type: DataType = data_type

    def __repr__(self) -> str:
        """
        Make string representation of configuration template.

        :returns: representation
        :rtype: str
        """
        return (
            f"ConfigurationTemplate(name='{self.name}', "
            f"reference='{self.reference}', description='{self.description}', "
            f"data_type='{self.data_type}', "
            f"default_value='{self.default_value}', "
            f"size='{self.size}', "
            f"labels='{self.labels}')"
        )

    def to_dto(self) -> Dict[str, Union[int, str, float, List[str]]]:
        """
        Create data transfer object used for registration.

        :returns: dto
        :rtype: Dict[str, Union[str, int, float, List[str]]]
        """
        dto: Dict[str, Union[str, int, float, List[str]]] = {
            "name": self.name,
            "reference": self.reference,
            "dataType": self.data_type.name,
        }

        if self.size != 1 and self.labels is not None:
            dto.update({"size": self.size})
            dto["labels"] = self.labels
        else:
            dto["labels"] = []

        if self.default_value:
            dto["defaultValue"] = str(self.default_value)

        return dto
