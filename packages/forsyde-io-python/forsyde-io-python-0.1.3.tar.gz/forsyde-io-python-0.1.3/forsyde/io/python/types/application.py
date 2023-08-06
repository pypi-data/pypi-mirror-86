from dataclasses import dataclass, field
from typing import Set

import forsyde.io.python.core as core


@dataclass(eq=True, repr=True, frozen=True)
class DataType(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'DataType'
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
class NativeFunction(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'NativeFunction'
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
class Implementation(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Implementation'
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
class Implements(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Implements'
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
class Constructs(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Constructs'
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
class Types(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Types'
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
class Takes(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Takes'
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
class Writes(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Writes'
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
class Reads(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Reads'
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
class Input(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Input'
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
class Output(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Output'
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
class Description(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Description'
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


class ApplicationFactory:
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
            "DataType": DataType,
            "NativeFunction": NativeFunction,
            "Implementation": Implementation,
            "Implements": Implements,
            "Constructs": Constructs,
            "Types": Types,
            "Takes": Takes,
            "Writes": Writes,
            "Reads": Reads,
            "Input": Input,
            "Output": Output,
            "Description": Description
        }
        if type_name in str_to_classes:
            return str_to_classes[type_name]()
        if strict:
            raise NotImplementedError(
              f"The type '{type_name}' is not recognized."
            )
        else:
            return None
