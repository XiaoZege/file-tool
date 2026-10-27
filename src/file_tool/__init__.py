import csv
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
    # rglob("*") 递归列出目录下的所有东西（文件 + 子目录）
    for item in root.rglob("*"):
        if not item.is_file():  # 只要文件，不要目录
            continue
        # 路径拆成一段一段，只要有任何一段是 .venv 这类目录就跳过
        if any(part in SKIP_DIRS for part in item.relative_to(root).parts):
            continue
        suffix = item.suffix.lower() or "(无扩展名)"
        counter[suffix] += 1
        total += 1

    typer.echo(f"目录：{root.resolve()}")
    typer.echo(f"共 {total} 个文件")
    typer.echo("")
    # most_common() 按数量从多到少排序
    for suffix, count in counter.most_common():
        typer.echo(f"{suffix:<14}{count}")


@app.command()
def rename(directory: str, old: str, new: str):
    """批量把文件名里的 old 替换成 new。"""
    root = Path(directory)
    if not root.is_dir():
        typer.echo(f"不是目录：{root}")
        raise typer.Exit(code=1)

    changed = 0
    # iterdir() 只列这一层，不往子目录钻（想递归就用 stats 里的 rglob）
    for item in root.iterdir():
        if not item.is_file():
            continue
        new_name = item.name.replace(old, new)  # 纯字符串替换，得到新名字
        if new_name == item.name:  # 名字没变，不用动它
            continue
        if (root / new_name).exists():  # 目标已存在，不覆盖别人的文件
            typer.echo(f"跳过（已有同名文件）：{new_name}")
            continue
        item.rename(root / new_name)  # 真正改名
        typer.echo(f"{item.name} -> {new_name}")
        changed += 1

    typer.echo(f"共改名 {changed} 个文件")


@app.command()
def dedupe(csv_path: str, column: str):
    """按指定列给 CSV 去重，结果写回原文件。"""
    path = Path(csv_path)
    if not path.is_file():
        typer.echo(f"不是文件：{path}")
        raise typer.Exit(code=1)

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)  # 每一行变成一个 dict
        if reader.fieldnames is None or column not in reader.fieldnames:
            typer.echo(f"找不到列：{column}")
            raise typer.Exit(code=1)
        fieldnames = reader.fieldnames

        seen: set[str] = set()  # 记录已经出现过的值
        rows = []
        removed = 0
        for row in reader:
            key = (row.get(column) or "").strip()
            if key in seen:  # 这个值见过了，丢掉这一行
                removed += 1
                continue
            seen.add(key)
            rows.append(row)

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    typer.echo(f"去重后 {len(rows)} 行，删除重复 {removed} 行")


def main() -> None:
    app()
