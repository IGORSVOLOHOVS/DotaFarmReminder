# Спецификация требований: DotaFarmReminder

Восстановлена по коду коммита `bd893bd` 2026-11-18. Описывает поведение, которое реализовано;
заявленное, но не сделанное вынесено в п. 3.7, неясное — в п. 9. Обзор проекта и команды —
[docs/README.md](docs/README.md).

## 1. Назначение и область

Приложение показывает игроку Dota 2 подсказки по фарму для выбранной роли в заданные моменты
матча, отсчитывая время собственным таймером.

В области:

- таймер матча с кнопками и глобальными клавишами F8/F9;
- выбор одной из трёх ролей и загрузка её подсказок из YAML;
- показ подсказки в окне поверх остальных, звук, скрытие через 5 с;
- перемещение оверлея, сохранение позиции оверлея и геометрии главного окна;
- журнал в stderr, файл и панель окна;
- генератор каркаса компонента `gen.py` и сборка PyInstaller по `dotafarmreminder.spec`.

Вне области (в коде этого нет):

- чтение состояния Dota 2 (игровое время, герой, золото): сетевых вызовов и интеграции с игрой нет;
- синхронизация таймера с игровыми часами;
- выбор героя: в коде есть только роль (коммит `4b3c291` «remove hero-specific logic»);
- роли, кроме Carry, Support и Offlane;
- редактирование подсказок из интерфейса — только правкой YAML и перезапуском.

## 2. Контекст

| Участник / система | Роль | Источник |
|---|---|---|
| Игрок | выбирает роль, управляет таймером кнопками и F8/F9, двигает оверлей | `ui.py`, `main.py:36-44` |
| Автор подсказок | правит `hint_manager/config/*.yaml` | `README.md:88-99` |
| Разработчик | создаёт компоненты `gen.py`, собирает exe | `gen.py`, `dotafarmreminder.spec` |
| Клавиатура ОС | глобальный перехват нажатий через pynput | `main.py:48-49` |
| Хранилище `QSettings` | позиция оверлея, геометрия окна | `settings/infrastructure.py` |
| Звуковой вывод | `QSoundEffect` из QtMultimedia | `ui.py:31-34` |
| Файловая система | YAML подсказок, `notification.wav`, журнал | `hint_manager/infrastructure.py`, `ui.py:32`, `main.py:13` |
| Окно Dota 2 | только фон, поверх которого стоит оверлей; приложение с ним не взаимодействует | `overlay/ui.py:7-11` |

Среда выполнения: Python 3.10+ (`README.md:23`), PyQt6. ОС — Windows; это вывод из
скрытых импортов `pynput.*._win32` (`dotafarmreminder.spec:13-14`), команд PowerShell в
`README.md:38-39` и упоминания pywin32 в коммите `f2519ba`. Другие ОС не описаны.

## 3. Функциональные требования

### 3.1 Таймер

- **FR-1.** Система должна после запуска таймера прибавлять одну секунду каждые 1000 мс и при каждом
  шаге выдавать текущее время строкой `MM:SS`.
  Source: `timer/application.py:13-20`, `timer/domain.py:8-10`. Verification: no test.
- **FR-2.** Система должна писать минуты без ограничения 59 (3600 с — `60:00`).
  Source: `timer/domain.py:9-10`. Verification: no test (проверено вызовом `formatted_time`).
- **FR-3.** Система должна игнорировать запуск уже идущего таймера и паузу остановленного.
  Source: `timer/application.py:17-25`. Verification: no test.
- **FR-4.** Система должна при сбросе останавливать таймер, обнулять счёт, выдавать `00:00` и
  скрывать оверлей. Source: `timer/application.py:27-31`, `ui.py:87-91`. Verification: no test.
- **FR-5.** Система должна делать кнопку «Старт» недоступной, пока таймер идёт, а «Пауза» — пока
  он стоит. Source: `timer/ui.py:29`, `timer/ui.py:34-36`, `ui.py:77-91`. Verification: no test.
- **FR-6.** Система должна по F8, нажатой в любом приложении, ставить идущий таймер на паузу или
  запускать остановленный, а по F9 — сбрасывать таймер.
  Source: `main.py:31-50`. Verification: no test (см. вопрос 2 в п. 9).

### 3.2 Роли и подсказки

- **FR-7.** Система должна предлагать три роли — «Керри» (Carry), «Саппорт» (Support),
  «Танк (Оффлейн)» (Offlane) — и при запуске выбирать Support.
  Source: `hint_manager/ui.py:16-26`, `hint_manager/domain.py:11`. Verification: no test.
- **FR-8.** Система должна при создании и при смене роли загружать подсказки из файла
  `<роль в нижнем регистре>.yaml` в каталоге `hint_manager/config` рядом с `main.py`.
  Source: `main.py:55-57`, `hint_manager/ui.py:28-30`, `hint_manager/application.py:8-16`,
  `hint_manager/infrastructure.py:10-16`. Verification: no test (проверено скриптом, см. docs/README.md).
- **FR-9.** Система должна считать, что подсказок у роли нет, если файла роли нет.
  Source: `hint_manager/infrastructure.py:12-13`. Verification: no test.
- **FR-10.** Система должна на каждом шаге таймера выбирать первую по порядку файла подсказку,
  у которой `time` посимвольно равно текущей строке `MM:SS`.
  Source: `ui.py:73`, `ui.py:93-94`, `hint_manager/application.py:18-24`. Verification: no test.
- **FR-11.** Система должна показывать текст найденной подсказки в оверлее, проигрывать
  `notification.wav`, если звук загружен, писать в журнал «Подсказка в MM:SS: текст» и скрывать
  оверлей через 5000 мс. Source: `ui.py:96-100`. Verification: no test.
- **FR-12.** Система должна при отсутствии `notification.wav` писать предупреждение в журнал и
  работать без звука. Source: `ui.py:31-36`. Verification: no test.

### 3.3 Оверлей

- **FR-13.** Система должна показывать оверлей окном без рамки, поверх остальных окон, с флагом
  `Tool`, прозрачным фоном и подложкой текста `rgba(0, 0, 0, 180)`.
  Source: `overlay/ui.py:7-25`. Verification: no test.
- **FR-14.** Система должна делать оверлей прозрачным для событий мыши Qt, пока режим перемещения
  выключен. Source: `overlay/ui.py:29`, `overlay/ui.py:36-37`. Verification: no test.
- **FR-15.** Система должна по кнопке-переключателю «Переместить оверлей (Вкл/Выкл)» включать режим,
  в котором у текста пунктирная рамка `#FFA500`, а оверлей перетаскивается левой кнопкой мыши;
  повторное нажатие выключает режим. Source: `ui.py:45-47`, `overlay/ui.py:39-60`. Verification: no test.

### 3.4 Сохранение состояния

- **FR-16.** Система должна при закрытии главного окна сохранять позицию оверлея, геометрию и
  состояние главного окна в `QSettings("MyCompany", "Dota2Helper")` и закрывать оверлей.
  Source: `ui.py:102-107`, `settings/infrastructure.py:4-18`. Verification: no test.
- **FR-17.** Система должна при запуске восстанавливать геометрию и состояние окна, если сохранены
  оба значения, и позицию оверлея, если она сохранена.
  Source: `ui.py:109-118`, `settings/infrastructure.py:11-23`. Verification: no test.

### 3.5 Главное окно, журнал, завершение

- **FR-18.** Система должна показывать окно «Dota 2 Helper» с блоком «Выберите роль», временем и
  кнопками «Старт», «Пауза», «Сброс», кнопкой перемещения оверлея и док-панелью «Логи», в стиле
  Fusion с тёмной таблицей стилей.
  Source: `ui.py:28`, `ui.py:42-52`, `ui.py:58-65`, `main.py:61-78`. Verification: no test.
- **FR-19.** Система должна писать журнал уровня INFO в stderr, в панель «Логи» (только текст
  сообщения) и в файл `logs/dota2helper/<ГГГГ-ММ-ДД>.log` относительно текущего каталога в виде
  JSON-строк с ротацией по 10 MB, хранением 10 дней и сжатием zip.
  Source: `main.py:12-29`, `ui.py:65`. Verification: no test.
- **FR-20.** Система должна при исключении во время запуска записывать его в журнал и завершаться
  с кодом 1. Source: `main.py:88-90`. Verification: no test.
- **FR-21.** Система должна после выхода из цикла событий Qt останавливать слушатель клавиатуры и
  завершаться с кодом цикла. Source: `main.py:85-87`. Verification: no test.

### 3.6 Содержимое и инструменты разработчика

- **FR-22.** Поставляемые файлы подсказок должны содержать: `carry.yaml` — 20 записей с `00:45` по
  `60:00`, `support.yaml` — 17 с `01:00` по `56:00`, `offlane.yaml` — 17 с `01:15` по `60:00`;
  времена уникальны, в кавычках, в формате `MM:SS`, тексты начинаются с «<Роль> (Турбо):».
  Source: `hint_manager/config/*.yaml`. Verification: no test (проверено `yaml.safe_load` и grep).
- **FR-23.** Система должна по `python gen.py <ComponentName>` создавать каталог с именем
  компонента в нижнем регистре и файлами `domain.py`, `application.py`, `infrastructure.py`,
  `ui.py`, `config/<имя>.yaml`, `tests.py`. Source: `gen.py:9-99`, `gen.py:103-108`. Verification: no test.
- **FR-24.** Система должна отказываться генерировать компонент, если каталог уже существует, и
  печатать строку использования, если аргументов не один.
  Source: `gen.py:11-13`, `gen.py:104-105`. Verification: no test.
- **FR-25.** Сборка по `dotafarmreminder.spec` должна включать `hint_manager/config` и
  `notification.wav`, скрытые импорты `pynput.keyboard._win32`, `pynput.mouse._win32`,
  `configparser`, `dependency_injector.errors` и давать каталог `DotaFarmReminder` с консольным
  exe. Source: `dotafarmreminder.spec:3-53`. Verification: no test (сборка не запускалась).

### 3.7 Заявлено, но не реализовано

| Что | Где заявлено | Что в коде |
|---|---|---|
| Сборка в один исполняемый файл в `dist` | `README.md:105`, `README.md:113` | `exclude_binaries=True` + `COLLECT` — сборка в каталог (`dotafarmreminder.spec:26-53`) |
| Иконка `image.ico` | `README.md:108` | spec берёт `image.png` (`dotafarmreminder.spec:42`) |
| Формат времени «ЧЧ:ММ» | `README.md:96` | сравнение с `MM:SS` от запуска таймера (`timer/domain.py:8-10`) |
| Use case'ы и репозитории оверлея и настроек | `overlay/application.py:8`, `settings/application.py:8` (`# TODO`) | заглушки, не подключены в `containers.py` |
| Поля состояния оверлея и настроек | `overlay/domain.py:6`, `settings/domain.py:6` (`# TODO`) | только `is_active` |
| `YamlTimerRepository` | `timer/infrastructure.py:5-8` | не импортируется: нет `ITimerRepository` в `timer/domain.py` |
| Настройки компонентов | `timer/config/timer.yaml`, `overlay/config/overlay.yaml`, `settings/config/settings.yaml` | шаблон `param1: value1`, не читается |
| Тесты компонентов | `*/tests.py` | `assert True`, настоящие проверки закомментированы |
| Замеры производительности | `pytest-benchmark` в `requirements.txt:3` | бенчмарков нет |

## 4. Интерфейсы

Командная строка (команды из файлов проекта):

| Команда | Источник | Действие |
|---|---|---|
| `python main.py` | `README.md:58` | запуск приложения |
| `python gen.py <ComponentName>` | `gen.py:103-108` | каркас компонента |
| `pyinstaller dotafarmreminder.spec` | `README.md:111` | сборка |

Клавиши и элементы окна:

| Элемент | Действие | Источник |
|---|---|---|
| F8 (глобально) | пауза, если таймер идёт, иначе старт | `main.py:38-42` |
| F9 (глобально) | сброс | `main.py:43-44` |
| Радиокнопки «Керри», «Саппорт», «Танк (Оффлейн)» | сигнал `role_changed` с `carry` / `support` / `offlane` | `hint_manager/ui.py:16-30` |
| «Старт», «Пауза», «Сброс» | сигналы `start_pressed`, `pause_pressed`, `reset_pressed` | `timer/ui.py:5-22` |
| «Переместить оверлей (Вкл/Выкл)» | `OverlayWidget.set_movable(bool)` | `ui.py:45-47` |
| Панель «Логи» | вывод журнала, только чтение | `ui.py:58-65` |

Внутренние сигналы Qt: `TimerUseCase.time_updated(str)` (`timer/application.py:5`),
`RoleSelectionWidget.role_changed(str)` (`hint_manager/ui.py:5`).

Файл подсказок `hint_manager/config/<роль>.yaml` (UTF-8, `hint_manager/infrastructure.py:14`):

| Поле | Тип | Обязательно | Смысл |
|---|---|---|---|
| (корень) | список | да | пустой файл — `TypeError` |
| `time` | строка `MM:SS` в кавычках | да | момент от запуска таймера; без кавычек `10:00` читается как число 600 |
| `text` | строка | да | текст оверлея |
| другие ключи | — | нельзя | `TypeError` в `Hint(**item)` (`hint_manager/infrastructure.py:16`) |

Ключи `QSettings` (`settings/infrastructure.py:7-23`):

| Ключ | Тип | Запись | Чтение |
|---|---|---|---|
| `mainWindow/geometry` | `QByteArray` | `ui.py:105` | `ui.py:111` |
| `mainWindow/state` | `QByteArray` | `ui.py:105` | `ui.py:111` |
| `overlay/position` | `QPoint` | `ui.py:104` | `ui.py:116` |

## 5. Данные

| Сущность | Поля | Источник |
|---|---|---|
| `Hint` | `time: str`, `text: str` | `hint_manager/domain.py:4-7` |
| `HintState` | `current_role: str = "support"`, `hints: List[Hint]` | `hint_manager/domain.py:9-12` |
| `TimerState` | `seconds: int = 0`, `is_running: bool = False` | `timer/domain.py:3-6` |

Хранение: подсказки — YAML в репозитории; состояние окон — `QSettings`; журнал — JSON-строки
loguru в `logs/dota2helper/` (каталог в `.gitignore:15`). Базы данных нет. Подсказки держатся в
памяти списком для текущей роли (`hint_manager/application.py:15-16`).

## 6. Нефункциональные требования

- **NFR-1.** Разрешение по времени — 1 с: шаг `QTimer` 1000 мс, сравнение по строке `MM:SS`.
  Source: `timer/application.py:20`, `hint_manager/application.py:22`.
- **NFR-2.** Файлы подсказок читаются в UTF-8. Source: `hint_manager/infrastructure.py:14`.
- **NFR-3.** Файл журнала ограничен: ротация 10 MB, хранение 10 дней, сжатие zip; запись через
  очередь (`enqueue=True`), с `backtrace` и `diagnose`. Source: `main.py:19-29`.
- **NFR-4.** Файл роли читается только при создании use case'а и при смене роли, не на каждом шаге.
  Source: `hint_manager/application.py:8-16`.
- **NFR-5.** Подписи интерфейса и сообщения журнала — на русском; исключение — заголовок окна
  «Dota 2 Helper» (`ui.py:28`).
  Source: `hint_manager/ui.py:10-19`, `timer/ui.py:16-18`, `ui.py:45`, `ui.py:59`, `main.py:46`.
- **NFR-6.** Совместимость с Python 3.10+: аннотации `str | None`, `tuple[...]`.
  Source: `README.md:23`, `hint_manager/application.py:18`, `settings/infrastructure.py:11`.

## 7. Ограничения и зависимости

Версии не закреплены (`requirements.txt:1-8`), lock-файла нет.

| Пакет | Где используется |
|---|---|
| PyQt6 (QtWidgets, QtCore, QtMultimedia) | интерфейс, `QTimer`, `QSettings`, `QSoundEffect` |
| pynput | глобальные клавиши (`main.py:5`, `main.py:48`) |
| loguru | журнал (`main.py:3`, `ui.py:2`) |
| PyYAML | файлы подсказок (`hint_manager/infrastructure.py:1`) |
| dependency-injector | контейнер и `@inject` (`containers.py:1`, `main.py:6`) |
| pytest | тесты-заготовки (`*/tests.py`) |
| pytest-benchmark | не используется |
| pyinstaller | сборка (`dotafarmreminder.spec`) |

Ограничение: `timer/__init__.py` должен существовать — иначе `import timer` находит модуль
pywin32 с тем же именем (коммит `f2519ba`). У `hint_manager/`, `overlay/`, `settings/`
`__init__.py` нет. Лицензия — MIT (`LICENSE`).

## 8. Приёмка

Автотестов поведения нет, поэтому приёмка ручная:

1. `pip install -r requirements.txt`, `python main.py`: открывается «Dota 2 Helper», выбрана роль
   «Саппорт», время `00:00`, «Пауза» недоступна (FR-5, FR-7, FR-18).
2. «Старт»: время растёт на 1 в секунду, «Старт» недоступна (FR-1, FR-5).
3. На `01:00` у роли Support появляется оверлей с текстом из `support.yaml`, звучит сигнал, в
   «Логи» строка «Подсказка в 01:00: …»; через 5 с оверлей исчезает (FR-10, FR-11).
4. При фокусе в другом окне F8 ставит на паузу и запускает, F9 сбрасывает в `00:00` и скрывает
   оверлей (FR-4, FR-6).
5. Роль «Керри»: подсказка на `00:45` из `carry.yaml` (FR-8).
6. Режим перемещения: оранжевая пунктирная рамка, перетаскивание; после закрытия и повторного
   запуска позиция оверлея и окна восстановлены (FR-15–FR-17).
7. В текущем каталоге появляется `logs/dota2helper/<дата>.log` с JSON-строками (FR-19).
8. Файлы подсказок проходят проверку `yaml.safe_load`: список, ключи только `time` и `text`,
   времена — строки `MM:SS` (FR-22).
9. `pyinstaller dotafarmreminder.spec`: собранный exe запускается и находит подсказки и звук (FR-25).

## 9. Открытые вопросы

1. Кто пользователи и какого уровня игры — в файлах только обращение README к игрокам.
2. Работают ли F8/F9: обработчик pynput вызывается в своём потоке и запускает `QTimer` и меняет
   виджеты напрямую (`main.py:36-44`); по правилам Qt таймер запускают из его потока. Не проверено.
3. Проходят ли клики сквозь оверлей в окно игры: стоит только `WA_TransparentForMouseEvents`
   (`overlay/ui.py:37`), флага `WindowTransparentForInput` нет. Не проверено.
4. Виден ли оверлей поверх Dota 2 в полноэкранном режиме — в файлах ничего.
5. Находит ли собранный exe `hint_manager/config` и `notification.wav`, если пути строятся от
   `__file__` (`main.py:56`, `ui.py:32`). Частичный ответ: снимок `image-1.png` (коммит `15375c0`,
   2025-09-11) показывает консоль `DotaFarmReminder.exe` и подсказку Carry на `00:45` — та сборка
   подсказки находила. Звук по снимку не определить; сборка текущего кода не проверялась.
6. Проходит ли сборка с `icon='image.png'`: по документации PyInstaller (не по файлам проекта)
   иконку не в формате `.ico` на Windows он переводит через Pillow, а Pillow в `requirements.txt` нет.
   Частичный ответ: `icon='image.png'` стоит с `eb8e2b3`, а на снимке `image-1.png` (журнал
   2025-09-11 12:57–12:58, коммит снимка `15375c0` — 12:59) работает `DotaFarmReminder.exe` с консолью,
   то есть сборка в тот день, по-видимому, проходила; в каком окружении — неизвестно.
7. Почему в v1.0.0 включена консоль (`55ffd31`: `console=False` → `True`).
8. Что происходит при ошибке в YAML роли, выбранной уже после запуска (исключение в слоте Qt).
9. Какие версии зависимостей использовались — ничего не закреплено.
10. Нужны ли заглушки `overlay`, `settings`, `timer/infrastructure.py` и шаблонные `config/*.yaml`;
    зачем в репозитории `image.ico` и `mixkit-long-pop-2358.wav`. Что известно: заглушки и шаблонные
    `config/*.yaml` совпадают побайтно с выводом нынешнего `gen.py` (проверено генерацией во
    временный каталог), то есть это его нетронутый результат; `image.ico` добавлен в `55ffd31`, а
    `mixkit-long-pop-2358.wav` — в `4b3c291` вместе с `notification.wav`; ни код, ни spec-файл на них
    не ссылаются. Нужны ли они владельцу — неизвестно.
11. Откуда взяты тексты подсказок и под какой патч Dota 2 они писались.
