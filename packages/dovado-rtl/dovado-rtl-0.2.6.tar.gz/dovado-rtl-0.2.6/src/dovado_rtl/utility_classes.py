from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Tuple, List


class RTL(Enum):
    VHDL = auto()
    VERILOG = auto()
    SYSTEM_VERILOG = auto()


class StopStep(Enum):
    SYNTHESIS = auto()
    IMPLEMENTATION = auto()


class ImplementationStep(Enum):
    PLACE = auto()
    ROUTE = auto()


@dataclass
class IsIncremental:
    synthesis: bool = True
    implementation: bool = True
