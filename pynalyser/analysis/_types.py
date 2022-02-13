from typing import List, Tuple, Type, TypeVar, Union

import attr


# @attr.s(auto_attribs=True)
class PynalyserType:
    @property
    def as_str(self) -> str:
        raise NotImplementedError


@attr.s(auto_attribs=True)
class UnionType(PynalyserType):
    types: List[PynalyserType] = attr.ib()
    @types.validator
    def check(self, attribute: attr.ib, value: List[PynalyserType]):
        if len(value) <= 1:
            raise ValueError("there should be more than 2 different types")

    @property
    def as_str(self) -> str:
        return f"Union[{', '.join(tp.as_str for tp in self.types)}]"

    @classmethod
    def make(cls, *types: PynalyserType) -> PynalyserType:
        new_types: List[PynalyserType] = []

        for tp in types:
            if isinstance(tp, cls):
                new_types.extend(tp.types)
            else:
                new_types.append(tp)

        if len(new_types) == 0:
            raise ValueError("length of types should not be 0")
        elif len(new_types) == 1:
            return types[0]
        else:
            return cls(list(set(new_types)))


@attr.s(auto_attribs=True, hash=True)
class SingleType(PynalyserType):
    name: str = attr.ib(kw_only=True)
    is_builtin: bool = attr.ib(kw_only=True)

    @property
    def as_str(self) -> str:
        return self.name


objectType = SingleType(name="object", is_builtin=True)


@attr.s(auto_attribs=True, hash=True)
class IntType(SingleType):
    name: str = "int"
    is_builtin: bool = True


@attr.s(auto_attribs=True, hash=True)
class SequenceType(SingleType):
    # TODO: not finshed, see docs.python.org/3/library/collections.abc.html
    item_type: PynalyserType


    @property
    def as_str(self) -> str:
        return f"{super().as_str}[{self.item_type.as_str}]"


# @attr.s(auto_attribs=True)
# class ListType(SequenceType):
#     is_builtin: bool = True

    # def __mul__(self, other: PynalyserType):
    #     if isinstance(other, ListType):
    #         pass

# @attr.s(auto_attribs=True)
# class IterableType(PynalyserType):
#     name: str