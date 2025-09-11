from .domain import HintState
from .infrastructure import YamlHintRepository

class HintManagerUseCase:
    def __init__(self, repo: YamlHintRepository):
        self._repo = repo
        self._state = HintState()
        self.load_hints_for_current_role()

    def set_role(self, role: str):
        if self._state.current_role != role:
            self._state.current_role = role
            self.load_hints_for_current_role()
    
    def load_hints_for_current_role(self):
        self._state.hints = self._repo.get_hints_for_role(self._state.current_role)
    
    def get_hint_for_time(self, formatted_time: str) -> str | None:
        if not self._state.hints:
            return None
        for hint in self._state.hints:
            if hint.time == formatted_time:
                return hint.text
        return None