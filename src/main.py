"""Точка входа программы."""
from src.config import parse_args
from src.npm_client import NpmError, get_direct_dependencies


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

    print("\nСбор данных из npm...")
    try:
        deps = get_direct_dependencies(args.package, args.version)
    except NpmError as error:
        print(f"Ошибка: {error}")
        return

    if not deps:
        print(f"У пакета {args.package}@{args.version} нет зависимостей.")
        return

    print(f"\nПрямые зависимости {args.package}@{args.version}:")
    for name, ver in sorted(deps.items()):
        print(f"  - {name}: {ver}")


if __name__ == "__main__":
    main()