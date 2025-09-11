import yaml
from pathlib import Path
from .domain import Hint_managerState, IHint_managerRepository

class YamlHint_managerRepository(IHint_managerRepository):
    def get_state(self) -> Hint_managerState:
        # This is a mock implementation
        return Hint_managerState(is_active=True)

def load_config(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)