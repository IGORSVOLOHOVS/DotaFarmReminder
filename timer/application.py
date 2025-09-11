from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from .domain import TimerState

class TimerUseCase(QObject):
    time_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._state = TimerState()
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)

    def _tick(self):
        self._state.seconds += 1
        self.time_updated.emit(self._state.formatted_time())

    def start(self):
        if not self._state.is_running:
            self._state.is_running = True
            self._timer.start(1000)
    
    def pause(self):
        if self._state.is_running:
            self._state.is_running = False
            self._timer.stop()

    def reset(self):
        self._state.is_running = False
        self._state.seconds = 0
        self._timer.stop()
        self.time_updated.emit(self._state.formatted_time())