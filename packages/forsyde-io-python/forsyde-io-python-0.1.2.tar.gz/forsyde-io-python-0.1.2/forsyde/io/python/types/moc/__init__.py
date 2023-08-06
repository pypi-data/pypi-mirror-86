from dataclasses import dataclass, field
from typing import Set

import forsyde.io.python.core as core
from forsyde.io.python.types.moc.sy import SYFactory
from forsyde.io.python.types.moc.sdf import SDFFactory
from forsyde.io.python.types.moc.de import DEFactory


class MoCFactory:
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
            return str_to_classes[type_name]
        subpackage_type = SYFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        subpackage_type = SDFFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        subpackage_type = DEFactory.build_type(type_name, False)
        if subpackage_type is not None:
            return subpackage_type
        if strict:
            raise NotImplementedError(
              f"The type '{type_name}' is not recognized."
            )
        else:
            return None
