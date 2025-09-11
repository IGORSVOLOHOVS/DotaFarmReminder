import os
import sys
from pathlib import Path

def create_file(path: Path, content: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip(), encoding='utf-8')

def generate_component(name: str):
    base_path = Path(name)
    if base_path.exists():
        print(f"Error: Component '{name}' already exists.")
        return

    print(f"Generating component '{name}'...")

    # --- domain.py ---
    domain_content = f"""
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class {name.capitalize()}State:
    # TODO: Add fields
    is_active: bool = False

class I{name.capitalize()}Repository(ABC):
    @abstractmethod
    def get_state(self) -> {name.capitalize()}State:
        raise NotImplementedError
"""
    create_file(base_path / "domain.py", domain_content)

    # --- application.py ---
    application_content = f"""
from .domain import I{name.capitalize()}Repository, {name.capitalize()}State

class {name.capitalize()}UseCase:
    def __init__(self, repo: I{name.capitalize()}Repository):
        self._repo = repo

    def execute(self) -> {name.capitalize()}State:
        # TODO: Implement use case logic
        return self._repo.get_state()
"""
    create_file(base_path / "application.py", application_content)

    # --- infrastructure.py ---
    infra_content = f"""
import yaml
from pathlib import Path
from .domain import {name.capitalize()}State, I{name.capitalize()}Repository

class Yaml{name.capitalize()}Repository(I{name.capitalize()}Repository):
    def get_state(self) -> {name.capitalize()}State:
        # This is a mock implementation
        return {name.capitalize()}State(is_active=True)

def load_config(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
"""
    create_file(base_path / "infrastructure.py", infra_content)

    # --- ui.py ---
    ui_content = f"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class {name.capitalize()}Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("UI for {name.capitalize()} Component"))
        self.setLayout(self.layout)
"""
    create_file(base_path / "ui.py", ui_content)

    # --- config/{name}.yaml ---
    config_content = f"""
# Configuration for the {name} component
default_settings:
  param1: value1
  param2: value2
"""
    create_file(base_path / "config" / f"{name}.yaml", config_content)
    
    # --- tests.py ---
    tests_content = f"""
import pytest
# from .application import {name.capitalize()}UseCase
# from .infrastructure import Yaml{name.capitalize()}Repository

def test_{name}_initialization():
    # repo = Yaml{name.capitalize()}Repository()
    # use_case = {name.capitalize()}UseCase(repo)
    # assert use_case is not None
    assert True
"""
    create_file(base_path / "tests.py", tests_content)

    print(f"Component '{name}' generated successfully in folder '{base_path}/'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gen.py <ComponentName>")
    else:
        component_name = sys.argv[1].lower()
        generate_component(component_name)