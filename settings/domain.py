from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class SettingsState:
    # TODO: Add fields
    is_active: bool = False

class ISettingsRepository(ABC):
    @abstractmethod
    def get_state(self) -> SettingsState:
        raise NotImplementedError