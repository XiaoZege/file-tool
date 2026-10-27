from typer.testing import CliRunner

from file_tool import app

runner = CliRunner()


def test_dedupe_keeps_first_row_per_key(tmp_path):
    csv_file = tmp_path / "people.csv"
    csv_file.write_text(
        "name,city\n小明,福州\n小红,厦门\n小明,泉州\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["dedupe", str(csv_file), "name"])

    assert result.exit_code == 0
    lines = csv_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3  # 表头 + 2 行数据
    assert "小明,福州" in lines
    assert "小明,泉州" not in lines


def test_dedupe_rejects_unknown_column(tmp_path):
    csv_file = tmp_path / "people.csv"
    csv_file.write_text("name,city\n小明,福州\n", encoding="utf-8")

    result = runner.invoke(app, ["dedupe", str(csv_file), "age"])

    assert result.exit_code == 1
    assert "找不到列" in result.stdout


def test_dedupe_rejects_missing_file(tmp_path):
    result = runner.invoke(app, ["dedupe", str(tmp_path / "nope.csv"), "name"])

    assert result.exit_code == 1
    assert "不是文件" in result.stdout
