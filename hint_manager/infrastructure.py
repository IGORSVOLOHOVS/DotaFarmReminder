import yaml
from pathlib import Path
from typing import List
from .domain import Hint

class YamlHintRepository:
    def __init__(self, config_dir: Path):
        self._config_dir = config_dir

    def get_hints_for_role(self, role: str) -> List[Hint]:
        path = self._config_dir / f"{role.lower()}.yaml"
        if not path.exists():
            return []
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return [Hint(**item) for item in data]