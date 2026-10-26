"""Точка входа программы."""
import json
from src.config import parse_args
from src.graph import build_graph, parse_test_graph


def print_tree(tree: dict, indent: int = 0) -> None:
    """Печатает дерево зависимостей."""
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
            print("Ошибка: В тестовом режиме нужно указать --repo с путем к файлу.")
            return
        try:
            test_graph = parse_test_graph(args.repo)
            print(f"\nТестовый граф загружен из {args.repo}")
        except FileNotFoundError:
            print(f"Ошибка: Файл {args.repo} не найден.")
            return
    else:
        print(f"\nСбор данных из npm для {args.package}...")

        # Строим граф (оборачиваем в словарь с корневым пакетом)
    tree = {args.package: build_graph(args.package, test_graph, args.filter)}

    print("\nГраф зависимостей:")
    print_tree(tree)
    
    # Вывод в формате JSON (для проверки структуры)
    # print(json.dumps(tree, indent=2))


if __name__ == "__main__":
    main()