from pathlib import Path
from loguru import logger
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QTextEdit, QDockWidget, QPushButton)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect

from settings.infrastructure import SettingsRepository
from overlay.ui import OverlayWidget
from timer.ui import TimerWidget
from timer.application import TimerUseCase
from hint_manager.ui import RoleSelectionWidget
from hint_manager.application import HintManagerUseCase

class LogHandler(QTextEdit):
    def write(self, message):
        self.moveCursor(self.textCursor().MoveOperation.End)
        self.insertPlainText(message)
        self.ensureCursorVisible()

class MainWindow(QMainWindow):
    def __init__(self, settings_repo: SettingsRepository, timer_uc: TimerUseCase, hint_uc: HintManagerUseCase):
        super().__init__()
        self.settings_repo = settings_repo
        self.timer_uc = timer_uc
        self.hint_uc = hint_uc

        self.setWindowTitle("Dota 2 Helper")
        self.overlay = OverlayWidget()

        self.sound_effect = QSoundEffect()
        sound_path = Path(__file__).parent / "notification.wav"
        if sound_path.exists():
            self.sound_effect.setSource(QUrl.fromLocalFile(str(sound_path)))
        else:
            logger.warning("Файл notification.wav не найден. Звуковые оповещения не будут работать.")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.timer_widget = TimerWidget()
        self.role_widget = RoleSelectionWidget()

        move_overlay_btn = QPushButton("Переместить оверлей (Вкл/Выкл)")
        move_overlay_btn.setCheckable(True)
        move_overlay_btn.toggled.connect(self.overlay.set_movable)

        main_layout.addWidget(self.role_widget)
        main_layout.addWidget(self.timer_widget)
        main_layout.addWidget(move_overlay_btn)
        main_layout.addStretch()

        self.setup_logging_dock()
        self.connect_signals()
        self.restore_settings()

    def setup_logging_dock(self):
        dock = QDockWidget("Логи", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        log_text_edit = LogHandler(self)
        log_text_edit.setReadOnly(True)
        dock.setWidget(log_text_edit)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        logger.add(log_text_edit.write, level="INFO", format="{message}")

    def connect_signals(self):
        self.timer_widget.start_pressed.connect(self.on_start_pressed)
        self.timer_widget.pause_pressed.connect(self.on_pause_pressed)
        self.timer_widget.reset_pressed.connect(self.on_reset_pressed)

        self.timer_uc.time_updated.connect(self.timer_widget.update_time)
        self.timer_uc.time_updated.connect(self.check_for_hint)

        self.role_widget.role_changed.connect(self.hint_uc.set_role)
        self.role_widget.hero_changed.connect(self.hint_uc.set_hero)

    def on_start_pressed(self):
        self.timer_uc.start()
        self.timer_widget.set_running_state(True)
        logger.info("Таймер запущен")

    def on_pause_pressed(self):
        self.timer_uc.pause()
        self.timer_widget.set_running_state(False)
        logger.info("Таймер на паузе")

    def on_reset_pressed(self):
        self.timer_uc.reset()
        self.timer_widget.set_running_state(False)
        self.overlay.hide() # <-- ИЗМЕНЕНИЕ ЗДЕСЬ
        logger.info("Таймер сброшен")

    def check_for_hint(self, current_time: str):
        hint_text = self.hint_uc.get_hint_for_time(current_time)
        if hint_text:
            self.overlay.set_text(hint_text)
            if self.sound_effect.isLoaded():
                self.sound_effect.play()
            logger.info(f"Подсказка в {current_time}: {hint_text}")
            QTimer.singleShot(4000, self.overlay.hide) # <-- ИЗМЕНЕНИЕ ЗДЕСЬ

    def closeEvent(self, event):
        self.settings_repo.save_main_window_state(self.saveGeometry(), self.saveState())
        self.overlay.close()
        super().closeEvent(event)

    def restore_settings(self):
        geometry, state = self.settings_repo.load_main_window_state()
        if geometry and state:
            self.restoreGeometry(geometry)
            self.restoreState(state)