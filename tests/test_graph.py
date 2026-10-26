"""Тесты для графа зависимостей."""
from src.graph import find_reverse_dependencies


def test_reverse_dependencies():
    """Проверяет поиск обратных зависимостей."""
    tree = {"A": {"B": {"C": {}}}}
    result = find_reverse_dependencies(tree, "C")
    assert "A" in result
    assert "B" in result