from dataclasses import dataclass
from krita import Node


@dataclass
class CommandReturn:
    new_node: None | Node = None
    err_msg: str | None = None


@dataclass
class Result[T]:
    result: T | None = None
    err_msg: str | None = None

    def unwrap(self) -> T:
        return self.result
