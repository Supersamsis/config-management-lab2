"""Модуль для визуализации графа (Graphviz)."""
from graphviz import Digraph


def to_dot(tree: dict) -> str:
    """Генерирует текстовое описание графа на языке DOT (Graphviz)."""
    lines = ["digraph G {"]
    
    def traverse(node):
        for pkg, children in node.items():
            if pkg.startswith("__"):  # Пропускаем циклы и фильтры
                continue
            lines.append(f'    "{pkg}";')
            if isinstance(children, dict):
                for child in children.keys():
                    if not child.startswith("__"):
                        lines.append(f'    "{pkg}" -> "{child}";')
                traverse(children)
                
    traverse(tree)
    lines.append("}")
    return "\n".join(lines)


def render_image(tree: dict, filename="graph") -> None:
    """Генерирует изображение графа в формате PNG и открывает его."""
    dot = Digraph(comment='Dependency Graph')
    
    def traverse(node):
        for pkg, children in node.items():
            if pkg.startswith("__"):
                continue
            dot.node(pkg)
            if isinstance(children, dict):
                for child in children.keys():
                    if not child.startswith("__"):
                        dot.edge(pkg, child)
                traverse(children)
                
    traverse(tree)
    # view=True автоматически откроет картинку после генерации
    dot.render(filename, format='png', view=True, cleanup=True)