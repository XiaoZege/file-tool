# file-tool

一个用 Python 写的文件批处理小工具，练习项目。

## 快速开始

```bash
uv sync
uv run file-tool --help
uv run file-tool stats .
```

## 命令

| 命令 | 作用 | 状态 |
|---|---|---|
| `stats <目录>` | 按扩展名统计文件数量 | 已完成 |
| `rename <目录> <旧> <新>` | 批量替换文件名中的字符串 | 待实现 |
| `dedupe <csv> <列名>` | 按某列给 CSV 去重 | 待实现 |

## 开发

```bash
uv run ruff check .     # 代码检查
uv run ruff format .    # 自动格式化
uv run pytest           # 跑测试
```
