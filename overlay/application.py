from .domain import IOverlayRepository, OverlayState

class OverlayUseCase:
    def __init__(self, repo: IOverlayRepository):
        self._repo = repo

    def execute(self) -> OverlayState:
        # TODO: Implement use case logic
        return self._repo.get_state()