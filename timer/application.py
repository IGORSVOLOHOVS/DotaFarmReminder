from .domain import ITimerRepository, TimerState

class TimerUseCase:
    def __init__(self, repo: ITimerRepository):
        self._repo = repo

    def execute(self) -> TimerState:
        # TODO: Implement use case logic
        return self._repo.get_state()