# file-tool

[![CI](https://github.com/XiaoZege/file-tool/actions/workflows/ci.yaml/badge.svg)](https://github.com/XiaoZege/file-tool/actions/workflows/ci.yaml)

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
| `stats <目录>` | 按扩展名统计文件数量（递归，跳过 `.venv` 等目录） | 已完成 |
| `rename <目录> <旧> <新>` | 批量替换同层文件名中的字符串 | 已完成 |
| `dedupe <csv> <列名>` | 按某列给 CSV 去重，结果写回原文件 | 已完成 |

### 例子

```bash
# 统计当前目录各类文件数量
uv run file-tool stats .

# 把 photos/ 下的 "IMG_" 全换成 "photo_"
uv run file-tool rename ./photos "IMG_" "photo_"

# people.csv 里 name 列重复的只保留第一行
uv run file-tool dedupe people.csv name
```

## 测试

9 个测试，覆盖正常路径和出错路径（目录不存在、列名不存在、改名目标已存在）。

## 开发

```bash
uv run ruff check .     # 代码检查
uv run ruff format .    # 自动格式化
uv run pytest           # 跑测试
```
