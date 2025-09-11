from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class TimerState:
    # TODO: Add fields
    is_active: bool = False

class ITimerRepository(ABC):
    @abstractmethod
    def get_state(self) -> TimerState:
        raise NotImplementedError