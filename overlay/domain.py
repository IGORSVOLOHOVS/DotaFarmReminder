from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class OverlayState:
    # TODO: Add fields
    is_active: bool = False

class IOverlayRepository(ABC):
    @abstractmethod
    def get_state(self) -> OverlayState:
        raise NotImplementedError