from .domain import ISettingsRepository, SettingsState

class SettingsUseCase:
    def __init__(self, repo: ISettingsRepository):
        self._repo = repo

    def execute(self) -> SettingsState:
        # TODO: Implement use case logic
        return self._repo.get_state()