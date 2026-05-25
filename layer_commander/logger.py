from dataclasses import dataclass
from typing import Callable


@dataclass
class Logger:
    log: Callable
