from .domain import IHint_managerRepository, Hint_managerState

class Hint_managerUseCase:
    def __init__(self, repo: IHint_managerRepository):
        self._repo = repo

    def execute(self) -> Hint_managerState:
        # TODO: Implement use case logic
        return self._repo.get_state()