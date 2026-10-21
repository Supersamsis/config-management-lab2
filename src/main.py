"""Точка входа программы."""
from src.config import parse_args


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


if __name__ == "__main__":
    main()