import tomllib
import os.path

def get_setting(file_path: str = "secret/setting.toml") -> dict:
    # Проверка существования файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл настроек не найден: {file_path}")

    # Попытка загрузить и разобрать TOML файл
    try:
        with open(file_path, "rb") as file:
            data = tomllib.load(file)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Ошибка синтаксиса в TOML файле: {e}")

    # Проверки на наличие обязательных секций и значений
    if not data.get("database"):
        raise TypeError("Отсутствует группа 'database'")

    if not isinstance(data["database"], dict):
        raise TypeError("Группа 'database' должна быть словарем")

    if not data["database"].get('url'):
        raise TypeError("Отсутствует значение 'url' в группе 'database'")

    if not data["database"].get('database'):
        raise TypeError("Отсутствует значение 'database' в группе 'database'")

    if not data.get("telegram"):
        raise TypeError("Отсутствует группа 'telegram'")

    if not isinstance(data["telegram"], dict):
        raise TypeError("Группа 'telegram' должна быть словарем")

    if not data["telegram"].get("token"):
        raise TypeError("Отсутствует значение 'token' в группе 'telegram'")

    return data
