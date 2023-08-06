from dataclasses import dataclass, field
from typing import Set

import forsyde.io.python.core as core
from forsyde.io.python.types.application import ApplicationFactory
from forsyde.io.python.types.extra import ExtraFactory
from forsyde.io.python.types.refinement import RefinementFactory
from forsyde.io.python.types.vertexes import VertexesFactory
from forsyde.io.python.types.edges import EdgesFactory
from forsyde.io.python.types.ports import PortsFactory


class TypesFactory:
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
        }
        if type_name in str_to_classes:
            return str_to_classes[type_name]()
        subpackage_type = ApplicationFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        subpackage_type = ExtraFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        subpackage_type = RefinementFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        subpackage_type = VertexesFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        subpackage_type = EdgesFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        subpackage_type = PortsFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        if strict:
            raise NotImplementedError(
              f"The type '{type_name}' is not recognized."
            )
        else:
            return None
