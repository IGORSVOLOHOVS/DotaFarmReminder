import sys
import os
from pathlib import Path
from loguru import logger
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QTextEdit, QDockWidget)
from PyQt6.QtCore import Qt, QTimer

from settings.infrastructure import SettingsRepository
from overlay.ui import OverlayWidget
from timer.ui import TimerWidget
from timer.application import TimerUseCase
from hint_manager.ui import RoleSelectionWidget
from hint_manager.infrastructure import YamlHintRepository
from hint_manager.application import HintManagerUseCase

class LogHandler(QTextEdit):
    def write(self, message):
        self.moveCursor(self.textCursor().MoveOperation.End)
        self.insertPlainText(message)
        self.ensureCursorVisible()

class MainWindow(QMainWindow):
    def __init__(self, settings_repo, timer_uc, hint_uc):
        super().__init__()
        self.settings_repo = settings_repo
        self.timer_uc = timer_uc
        self.hint_uc = hint_uc
        
        self.setWindowTitle("Dota 2 Helper")
        self.overlay = OverlayWidget()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        timer_widget = TimerWidget()
        role_widget = RoleSelectionWidget()
        main_layout.addWidget(role_widget)
        main_layout.addWidget(timer_widget)
        main_layout.addStretch()

        self.setup_logging_dock()
        self.connect_signals(timer_widget, role_widget)
        self.restore_settings()

    def setup_logging_dock(self):
        dock = QDockWidget("Логи", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        log_text_edit = LogHandler(self)
        log_text_edit.setReadOnly(True)
        dock.setWidget(log_text_edit)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        logger.add(log_text_edit.write, level="INFO", format="{message}")

    def connect_signals(self, timer_widget, role_widget):
        timer_widget.start_pressed.connect(self.timer_uc.start)
        timer_widget.start_pressed.connect(lambda: timer_widget.set_running_state(True))
        timer_widget.pause_pressed.connect(self.timer_uc.pause)
        timer_widget.pause_pressed.connect(lambda: timer_widget.set_running_state(False))
        timer_widget.reset_pressed.connect(self.timer_uc.reset)
        timer_widget.reset_pressed.connect(lambda: timer_widget.set_running_state(False))
        timer_widget.reset_pressed.connect(self.overlay.hide_text)
        
        self.timer_uc.time_updated.connect(timer_widget.update_time)
        self.timer_uc.time_updated.connect(self.check_for_hint)

        role_widget.role_changed.connect(self.hint_uc.set_role)

    def check_for_hint(self, current_time: str):
        hint_text = self.hint_uc.get_hint_for_time(current_time)
        if hint_text:
            self.overlay.set_text(hint_text)
            logger.info(f"Подсказка в {current_time}: {hint_text}")
            QTimer.singleShot(4000, self.overlay.hide_text)

    def closeEvent(self, event):
        self.settings_repo.save_main_window_state(self.saveGeometry(), self.saveState())
        self.overlay.close()
        super().closeEvent(event)

    def restore_settings(self):
        geometry, state = self.settings_repo.load_main_window_state()
        if geometry and state:
            self.restoreGeometry(geometry)
            self.restoreState(state)

def setup_logger():
    log_dir = Path("logs/dota2helper")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "{time:YYYY-MM-DD}.log"
    
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(
        log_file,
        level="INFO",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        serialize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True
    )

def main():
    try:
        setup_logger()
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        
        dark_stylesheet = """
        QWidget { color: #E0E0E0; background-color: #2E2E2E; }
        QMainWindow, QDockWidget { background-color: #252525; }
        QPushButton { background-color: #4A4A4A; border: 1px solid #5A5A5A; padding: 5px; border-radius: 3px; }
        QPushButton:hover { background-color: #5A5A5A; }
        QPushButton:pressed { background-color: #6A6A6A; }
        QPushButton:disabled { color: #888888; background-color: #3A3A3A; }
        QGroupBox { border: 1px solid #4A4A4A; margin-top: 10px; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        QTextEdit { background-color: #1E1E1E; border: 1px solid #4A4A4A; }
        """
        app.setStyleSheet(dark_stylesheet)
        
        settings_repo = SettingsRepository()
        timer_use_case = TimerUseCase()
        
        hint_repo_path = Path(__file__).parent / "hint_manager" / "config"
        hint_repo = YamlHintRepository(hint_repo_path)
        hint_use_case = HintManagerUseCase(hint_repo)

        window = MainWindow(settings_repo, timer_use_case, hint_use_case)
        window.showNormal()
        
        sys.exit(app.exec())
    except Exception as e:
        logger.exception(f"Критическая ошибка в приложении: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()