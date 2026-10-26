"""Модуль для построения графа зависимостей (DFS)."""
from typing import Dict, List, Optional, Set
from src.npm_client import get_direct_dependencies, NpmError


def parse_test_graph(path: str) -> Dict[str, List[str]]:
    """Парсит тестовый граф из файла (формат: A: B, C)."""
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            pkg, deps_str = line.split(":", 1)
            graph[pkg.strip()] = [d.strip() for d in deps_str.split(",") if d.strip()]
    return graph


def build_graph(
    package: str,
    test_graph: Optional[Dict[str, List[str]]] = None,
    filter_str: Optional[str] = None,
    visited: Optional[Set[str]] = None
) -> Dict:
    """Рекурсивно строит дерево зависимостей (DFS)."""
    if visited is None:
        visited = set()

    # 1. Фильтрация
    if filter_str and filter_str in package:
        return {"__filtered__": package}

    # 2. Обработка циклов
    if package in visited:
        return {"__cycle__": package}

    visited.add(package)

    # 3. Получение прямых зависимостей
    deps = []
    if test_graph is not None:
        deps = test_graph.get(package, [])
    else:
        try:
            deps_dict = get_direct_dependencies(package)
            deps = list(deps_dict.keys())
        except NpmError:
            deps = []

    # 4. Рекурсивный обход
    children = {}
    for dep in deps:
        children[dep] = build_graph(dep, test_graph, filter_str, visited)

    visited.remove(package)  # Возвращаем для других веток
    return children  # <--- ВАЖНО: возвращаем только детей, без самого пакета