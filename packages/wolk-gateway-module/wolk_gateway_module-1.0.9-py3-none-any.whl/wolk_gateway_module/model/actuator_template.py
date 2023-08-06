"""Actuator templates used for registering device on WolkAbout IoT Platform."""
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
from typing import Optional
from typing import Union

from wolk_gateway_module.model.data_type import DataType


class ActuatorTemplate:
    """
    Actuator template for registering device on Platform.

    :ivar description: Description detailing this actuator
    :vartype description: str or None
    :ivar name: Name of actuator
    :vartype name: str
    :ivar reference: Unique actuator reference
    :vartype reference: str
    :ivar unit: Actuator reading type measurement name and unit
    :vartype unit: dict
    """

    def __init__(
        self,
        name: str,
        reference: str,
        data_type: DataType = None,
        reading_type_name: str = None,
        unit: str = None,
        description: str = None,
    ):
        """
        Actuator template for device registration request.

        Define a reading type either by using the ``data_type`` to select a
        generic type (boolean, numeric, string) or use ``reading_type_name``
        and ``unit`` to use a custom reading type that was previously defined
        on WolkAbout IoT Platform.

        :param name: Actuator name
        :type name: str
        :param reference: Actuator reference
        :type reference: str
        :param data_type: Actuator data type
        :type data_type: Optional[DataType]
        :param reading_type_name: Custom reading type name
        :type reading_type_name: Optional[str]
        :param unit: Custom reading type measurement unit
        :type unit: Optional[str]
        :param description: Description detailing the actuator
        :type description: Optional[str]
        """
        self.name: str = name
        self.reference: str = reference
        self.description: Optional[str] = description

        if not (data_type or reading_type_name or unit):
            raise ValueError("Unable to create template")

        if data_type:
            if not isinstance(data_type, DataType):
                raise ValueError("Invalid data type given")
            if data_type == DataType.NUMERIC:
                self.unit: Dict[str, str] = {
                    "readingTypeName": "COUNT(ACTUATOR)",
                    "symbol": "count",
                }
            elif data_type == DataType.BOOLEAN:
                self.unit = {
                    "readingTypeName": "SWITCH(ACTUATOR)",
                    "symbol": "",
                }
            elif data_type == DataType.STRING:
                self.unit = {"readingTypeName": "TEXT(ACTUATOR)", "symbol": ""}
            return

        if not (reading_type_name and unit):
            raise ValueError(
                "Both reading type name and unit must be provided"
            )
        self.unit = {"readingTypeName": reading_type_name, "symbol": unit}

    def __repr__(self) -> str:
        """
        Make string representation of actuator template.

        :returns: representation
        :rtype: str
        """
        return (
            f"ActuatorTemplate(name='{self.name}', "
            f"reference='{self.reference}', description='{self.description}', "
            f"unit='{self.unit}')"
        )

    def to_dto(self) -> Dict[str, Union[int, float, str, Dict[str, str]]]:
        """
        Create data transfer object used for registration.

        :returns: dto
        :rtype: Dict[str, Union[int, float, str]]
        """
        dto: Dict[str, Union[int, float, str, Dict[str, str]]] = {
            "name": self.name,
            "reference": self.reference,
            "unit": self.unit,
        }

        dto["description"] = self.description if self.description else ""

        return dto
