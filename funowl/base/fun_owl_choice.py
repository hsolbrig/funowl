import logging
from dataclasses import dataclass
from typing import Any, ClassVar, get_type_hints, List, Type

from rdflib import Graph

from funowl.base.fun_owl_base import FunOwlBase
from funowl.base.cast_function import cast
from funowl.terminals.TypingHelper import get_args, isinstance_, is_union
from funowl.writers.FunctionalWriter import FunctionalWriter


@dataclass
class FunOwlChoice(FunOwlBase):
    """
    Base class for different type choices.
    - v: The actual value.  Subclasses override the possible types of v
    - coercion_allowed: False means don't try to coerce incoming values to types -- must match exactly.
      True means try to make it fit
    """
    v: Any
    coercion_allowed: ClassVar[bool] = True       # True means you can't cast to the underlying type

    @classmethod
    def hints(cls) -> List[Type]:
        """
        Return the allowed types for value v
        """
        hints = get_type_hints(cls)['v']
        return get_args(hints) if is_union(hints) else [hints]

    def set_v(self, value: Any) -> bool:
        """ Default setter -- can be invoked from more elaborate coercion routines
        :param value: value to set
        :return: True if v was set
        """
        for choice_type in self.hints():
            if issubclass(type(value), choice_type) or (self.coercion_allowed and isinstance_(value, choice_type)):
                super().__setattr__('v', value)
                logging.debug(f"{type(self).__name__}: value = {str(self.v)} (type: {type(self.v).__name__})")
                return True
        return False

    def __setattr__(self, key, value):
        if key != 'v' or not self.set_v(value):
            hints = get_type_hints(type(self))
            super().__setattr__(key, cast(hints[key], value) if key in hints else value)

    def to_functional(self, w: FunctionalWriter) -> FunctionalWriter:
        """ Emit functional syntax for value

        :param w: FunctionalWriter instance
        :return: FunctionalWriter instance
        """
        return w + self.v

    def to_rdf(self, g: Graph) -> None:
        """
        Add value of self to graph g
        :param g: Target graph
        """
        self.v.to_rdf(g)

    def _is_valid(cls: Type["FunOwlChoice"], v: Any) -> bool:
        """
        Determine whether v is a valid instance of v
        :param v: value to test
        """
        for choice_type in cls.hints():
            if issubclass(type(v), choice_type):
                return True
            elif cls.coercion_allowed and isinstance(v, choice_type):
                return True
        return False

    def __str__(self) -> str:
        return str(self.v)