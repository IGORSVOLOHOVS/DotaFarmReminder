from dependency_injector import containers, providers
from pathlib import Path

from settings.infrastructure import SettingsRepository
from timer.application import TimerUseCase
from hint_manager.infrastructure import YamlHintRepository
from hint_manager.application import HintManagerUseCase
from ui import MainWindow  # <-- ИЗМЕНЕНИЕ ЗДЕСЬ

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    settings_repo = providers.Singleton(SettingsRepository)
    timer_use_case = providers.Singleton(TimerUseCase)

    hint_repo = providers.Singleton(
        YamlHintRepository, 
        config_dir=config.hint_repo_path
    )
    hint_use_case = providers.Singleton(
        HintManagerUseCase, 
        repo=hint_repo
    )
    
    main_window = providers.Singleton(
        MainWindow,
        settings_repo=settings_repo,
        timer_uc=timer_use_case,
        hint_uc=hint_use_case,
    )