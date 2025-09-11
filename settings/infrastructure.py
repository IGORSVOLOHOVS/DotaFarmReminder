import yaml
from pathlib import Path
from .domain import SettingsState, ISettingsRepository

class YamlSettingsRepository(ISettingsRepository):
    def get_state(self) -> SettingsState:
        # This is a mock implementation
        return SettingsState(is_active=True)

def load_config(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)