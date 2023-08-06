from dataclasses import dataclass, field
from typing import Set

import forsyde.io.python.core as core


@dataclass(eq=True, repr=True, frozen=True)
class Host(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Host'
    required_ports: Set[str] = field(
        default_factory=lambda: set(
        ),
        repr=False
    )
    required_properties: Set[str] = field(
        default_factory=lambda: set(
        ),
        repr=False
    )

    def get_type_name(self):
        return self.type_name

    def get_required_ports(self):
        return self.required_ports

    def get_required_properties(self):
        return self.required_properties


@dataclass(eq=True, repr=True, frozen=True)
class OrderedExecution(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'OrderedExecution'
    required_ports: Set[str] = field(
        default_factory=lambda: set(
        ),
        repr=False
    )
    required_properties: Set[str] = field(
        default_factory=lambda: set(
        ),
        repr=False
    )

    def get_type_name(self):
        return self.type_name

    def get_required_ports(self):
        return self.required_ports

    def get_required_properties(self):
        return self.required_properties


class PortsFactory:
    """
    This class is auto generated.
    It enables import and export of ForSyDe-IO type models by stringification.
    """

    @classmethod
    def build_type(cls,
                   type_name: str,
                   strict: bool = True
                   ) -> core.Type:
        str_to_classes = {
            "Host": Host,
            "OrderedExecution": OrderedExecution
        }
        if type_name in str_to_classes:
            return str_to_classes[type_name]()
        if strict:
            raise NotImplementedError(
              f"The type '{type_name}' is not recognized."
            )
        else:
            return None
