"""Клиент для работы с реестром npm."""
import json
import urllib.request
import urllib.error
from typing import Dict


class NpmError(Exception):
    """Ошибка при работе с npm."""


def get_direct_dependencies(
    package_name: str, version: str = "latest"
) -> Dict[str, str]:
    """Получает прямые зависимости пакета из реестра npm.

    Args:
        package_name: имя пакета (например, "express").
        version: версия пакета (например, "4.18.2" или "latest").

    Returns:
        Словарь {имя_зависимости: версия}.

    Raises:
        NpmError: если пакет не найден или произошла ошибка сети.
    """
    url = f"https://registry.npmjs.org/{package_name}/{version}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise NpmError(
            f"Пакет {package_name}@{version} не найден (HTTP {error.code})"
        )
    except urllib.error.URLError as error:
        raise NpmError(f"Ошибка сети: {error.reason}")
    except json.JSONDecodeError:
        raise NpmError("Некорректный ответ от реестра npm")

    dependencies = data.get("dependencies", {})
    return dict(dependencies)