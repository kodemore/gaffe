from typing import Any

from mypy.nodes import AssignmentStmt, ClassDef, SymbolTableNode
from mypy.plugin import AttributeContext, ClassDefContext, Plugin, SemanticAnalyzerPluginInterface, TypeInfo
from mypy.types import AnyType, Type, TypeOfAny


class GaffePlugin(Plugin):
    def get_class_attribute_hook(self, fullname: str):
        if fullname.startswith("builtins.") or fullname.startswith("typing."):
            return
        class_name = fullname[: fullname.rfind(".")]
        sym = self.lookup_fully_qualified(class_name)
        if isinstance(sym, SymbolTableNode) and isinstance(sym.node, TypeInfo):
            for mro in sym.node.mro:
                full_name = str(mro.defn.fullname)
                if full_name == "gaffe.error.Error":
                    return self._override_attribute_type

    @staticmethod
    def _override_attribute_type(ctx: AttributeContext) -> Type:
        return AnyType(TypeOfAny.special_form)

    def get_base_class_hook(self, fullname: str):
        if fullname.startswith("builtins.") or fullname.startswith("typing."):
            return

        class_name = fullname[: fullname.rfind(".")]
        sym = self.lookup_fully_qualified(class_name)
        if isinstance(sym, SymbolTableNode) and isinstance(sym.node, TypeInfo):
            for mro in sym.node.mro:
                full_name = str(mro.defn.fullname)
                if full_name == "gaffe.error.Error":
                    return self._override_class_body

    @staticmethod
    def _override_class_body(ctx: ClassDefContext) -> None:
        cls: ClassDef = ctx.cls
        api: SemanticAnalyzerPluginInterface = ctx.api

        # remove assignments so mypy doesn't complain
        for stmt in cls.defs.body:
            if not isinstance(stmt, AssignmentStmt):
                continue
            stmt.type = AnyType(TypeOfAny.special_form)


def plugin(version: str) -> Any:
    # @todo: check the right version
    return GaffePlugin
