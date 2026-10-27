from collections import Counter
from pathlib import Path

import typer

app = typer.Typer(help="文件批处理小工具", no_args_is_help=True)

# 这些目录里的文件不是项目内容，统计时跳过
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".idea"}


@app.command()
def stats(path: str = typer.Argument(".", help="要统计的目录")):
    """按扩展名统计文件数量。"""
    root = Path(path)
    if not root.is_dir():
        typer.echo(f"不是目录：{root}")
        raise typer.Exit(code=1)

    counter: Counter[str] = Counter()
    total = 0
    for item in root.rglob("*"):
        if not item.is_file():
            continue
        if any(part in SKIP_DIRS for part in item.relative_to(root).parts):
            continue
        suffix = item.suffix.lower() or "(无扩展名)"
        counter[suffix] += 1
        total += 1

    typer.echo(f"目录：{root.resolve()}")
    typer.echo(f"共 {total} 个文件")
    typer.echo("")
    for suffix, count in counter.most_common():
        typer.echo(f"{suffix:<14}{count}")


@app.command()
def rename(directory: str, old: str, new: str):
    """批量替换文件名中的字符串（待实现）。"""
    typer.echo("还没实现：照着 stats 的写法，遍历 directory，用 name.replace(old, new) 改名")


@app.command()
def dedupe(csv_path: str, column: str):
    """按指定列给 CSV 去重（待实现）。"""
    typer.echo("还没实现：用 csv.DictReader 读入，按 column 的值去重后写回")


def main() -> None:
    app()
