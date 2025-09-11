# Dota 2 Helper

Игровой помощник-напоминалка для Dota 2, отображающий подсказки поверх окна с игрой.

## Установка зависимостей

Рекомендуется использовать виртуальное окружение. Для установки и управления им можно использовать `uv`.

1.  **Создание виртуального окружения:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
    ```

2.  **Установка зависимостей с помощью uv:**
    ```bash
    pip install uv
    uv pip install -r requirements.txt
    ```

## Запуск приложения
```bash
python main.py