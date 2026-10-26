"""Парсинг аргументов командной строки для ПР2."""
import argparse


def parse_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки.

    Returns:
        argparse.Namespace: объект с параметрами.
    """
    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей npm"
    )
    parser.add_argument(
        "--package", type=str, required=True,
        help="Имя анализируемого пакета",
    )
    parser.add_argument(
        "--repo", type=str, default=None,
        help="URL репозитория или путь к файлу тестового репозитория",
    )
    parser.add_argument(
        "--test-mode", action="store_true",
        help="Режим работы с тестовым репозиторием (файл)",
    )
    parser.add_argument(
        "--version", type=str, default="latest",
        help="Версия пакета",
    )
    parser.add_argument(
        "--ascii-tree", action="store_true",
        help="Вывод в формате ASCII-дерева",
    )
    parser.add_argument(
        "--filter", type=str, default=None,
        help="Подстрока для фильтрации пакетов",
    )
    parser.add_argument(
        "--reverse", type=str, default=None,
        help="Найти обратные зависимости для указанного пакета",
    )
    return parser.parse_args()