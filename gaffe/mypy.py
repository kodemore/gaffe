from typing import Any

from mypy.nodes import SymbolTableNode
from mypy.plugin import AttributeContext, Plugin, TypeInfo
from mypy.types import Type


def provide_exception_type(ctx: AttributeContext) -> Type:
    return ctx.type


class GaffePlugin(Plugin):

    def get_class_attribute_hook(self, fullname: str):
        class_name = fullname[:fullname.rfind(".")]
        sym = self.lookup_fully_qualified(class_name)
        if isinstance(sym, SymbolTableNode) and isinstance(sym.node, TypeInfo):
            for base in sym.node.bases:
                if str(base) == "gaffe.error.Error":
                    return provide_exception_type
        else:
            return None


def plugin(version: str) -> Any:
    # @todo: check the right version
    return GaffePlugin
