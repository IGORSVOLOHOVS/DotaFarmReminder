from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Hint_managerState:
    # TODO: Add fields
    is_active: bool = False

class IHint_managerRepository(ABC):
    @abstractmethod
    def get_state(self) -> Hint_managerState:
        raise NotImplementedError