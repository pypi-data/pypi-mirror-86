from dataclasses import dataclass, field
from typing import Set

import forsyde.io.python.core as core
from forsyde.io.python.types.vertexes.moc import MoCFactory


@dataclass(eq=True, repr=True, frozen=True)
class Process(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Process'
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
class SporadicTask(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'SporadicTask'
    required_ports: Set[str] = field(
        default_factory=lambda: set(
          'minArrival'
        ),
        repr=False
    )
    required_properties: Set[str] = field(
        default_factory=lambda: set(
          'minArrival'
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
class TriggeredTask(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'TriggeredTask'
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
class AbstractOrdering(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'AbstractOrdering'
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
class AbstractGrouping(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'AbstractGrouping'
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
class AbstractPhysicalComponent(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'AbstractPhysicalComponent'
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
class AbstractProcessingComponent(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'AbstractProcessingComponent'
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
class AbstractCommunicationComponent(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'AbstractCommunicationComponent'
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
class TimeDivisionMultiplexer(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'TimeDivisionMultiplexer'
    required_ports: Set[str] = field(
        default_factory=lambda: set(
          'slots'
        ),
        repr=False
    )
    required_properties: Set[str] = field(
        default_factory=lambda: set(
          'slots'
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
class WCET(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'WCET'
    required_ports: Set[str] = field(
        default_factory=lambda: set(
          'time'
        ),
        repr=False
    )
    required_properties: Set[str] = field(
        default_factory=lambda: set(
          'time'
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
class AbstractStorageComponent(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'AbstractStorageComponent'
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
class ComputationalTile(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'ComputationalTile'
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
class AbsractInterfaceComponent(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'AbsractInterfaceComponent'
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
class ConstructedProcess(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'ConstructedProcess'
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
class Signal(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'Signal'
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
class FIFOSignal(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'FIFOSignal'
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
class WCCT(core.Type):
    """
    This class has been automatically generated from forsyde-io.
    Any modifications therein are likely going to be overwritten.
    """

    type_name: str = 'WCCT'
    required_ports: Set[str] = field(
        default_factory=lambda: set(
          'time',
          'flit'
        ),
        repr=False
    )
    required_properties: Set[str] = field(
        default_factory=lambda: set(
          'time',
          'flit'
        ),
        repr=False
    )

    def get_type_name(self):
        return self.type_name

    def get_required_ports(self):
        return self.required_ports

    def get_required_properties(self):
        return self.required_properties


class VertexesFactory:
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
            "Process": Process,
            "SporadicTask": SporadicTask,
            "TriggeredTask": TriggeredTask,
            "AbstractOrdering": AbstractOrdering,
            "AbstractGrouping": AbstractGrouping,
            "AbstractPhysicalComponent": AbstractPhysicalComponent,
            "AbstractProcessingComponent": AbstractProcessingComponent,
            "AbstractCommunicationComponent": AbstractCommunicationComponent,
            "TimeDivisionMultiplexer": TimeDivisionMultiplexer,
            "WCET": WCET,
            "AbstractStorageComponent": AbstractStorageComponent,
            "ComputationalTile": ComputationalTile,
            "AbsractInterfaceComponent": AbsractInterfaceComponent,
            "ConstructedProcess": ConstructedProcess,
            "Signal": Signal,
            "FIFOSignal": FIFOSignal,
            "WCCT": WCCT
        }
        if type_name in str_to_classes:
            return str_to_classes[type_name]()
        subpackage_type = MoCFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        if strict:
            raise NotImplementedError(
              f"The type '{type_name}' is not recognized."
            )
        else:
            return None
