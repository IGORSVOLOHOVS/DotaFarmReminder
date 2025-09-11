from dataclasses import dataclass

@dataclass
class TimerState:
    seconds: int = 0
    is_running: bool = False

    def formatted_time(self) -> str:
        mins, secs = divmod(self.seconds, 60)
        return f"{mins:02}:{secs:02}"