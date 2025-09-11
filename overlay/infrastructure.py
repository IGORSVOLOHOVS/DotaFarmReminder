import yaml
from pathlib import Path
from .domain import OverlayState, IOverlayRepository

class YamlOverlayRepository(IOverlayRepository):
    def get_state(self) -> OverlayState:
        # This is a mock implementation
        return OverlayState(is_active=True)

def load_config(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)