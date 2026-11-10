"""Точка входа программы."""
from src.config import parse_args
from src.graph import (
    build_graph,
    parse_test_graph,
    find_reverse_dependencies,
)
from src.visualizer import to_dot, render_image


def print_tree(tree: dict, indent: int = 0) -> None:
    """Печатает дерево зависимостей в консоль."""
    for pkg, children in tree.items():
        if pkg == "__cycle__":
            print("  " * indent + f"[Цикл: {children}]")
        elif pkg == "__filtered__":
            print("  " * indent + f"[Отфильтровано: {children}]")
        else:
            print("  " * indent + f"- {pkg}")
            if children:
                print_tree(children, indent + 1)


def main() -> None:
    """Запускает программу."""
    args = parse_args()

    print("Параметры запуска:")
    print(f"  Пакет:      {args.package}")
    print(f"  Репозиторий:{args.repo}")
    print(f"  Test-mode:  {args.test_mode}")
    print(f"  Версия:     {args.version}")
    print(f"  ASCII-tree: {args.ascii_tree}")
    print(f"  Фильтр:     {args.filter}")

    test_graph = None
    if args.test_mode:
        if not args.repo:
            print("Ошибка: В тестовом режиме нужен путь к файлу.")
            return
        try:
            test_graph = parse_test_graph(args.repo)
            print(f"\nТестовый граф загружен из {args.repo}")
        except FileNotFoundError:
            print(f"Ошибка: Файл {args.repo} не найден.")
            return
    else:
        print(f"\nСбор данных из npm для {args.package}...")

    tree = {
        args.package: build_graph(
            args.package, test_graph, args.filter
        )
    }

    print("\nГраф зависимостей:")
    print_tree(tree)

    if args.reverse:
        print(f"\nОбратные зависимости для {args.reverse}:")
        rev_deps = find_reverse_dependencies(tree, args.reverse)
        if not rev_deps:
            print("  Не найдено.")
        else:
            for dep in rev_deps:
                print(f"  - {dep}")

    if args.ascii_tree:
        print("\nГраф зависимостей (ASCII):")
        print_tree(tree)

    dot_code = to_dot(tree)
    print("\nТекстовое представление графа (Graphviz DOT):")
    print(dot_code)

    print("\nГенерация изображения графа...")
    try:
        render_image(tree, filename="dependency_graph")
        print("Изображение сохранено и открыто.")
    except Exception as e:
        print(f"Ошибка при создании изображения: {e}")


if __name__ == "__main__":
    main()