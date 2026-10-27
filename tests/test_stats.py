from typer.testing import CliRunner

from file_tool import app

runner = CliRunner()


def test_stats_counts_by_suffix(tmp_path):
    (tmp_path / "a.py").write_text("")
    (tmp_path / "b.py").write_text("")
    (tmp_path / "c.md").write_text("")

    result = runner.invoke(app, ["stats", str(tmp_path)])

    assert result.exit_code == 0
    assert "共 3 个文件" in result.stdout
    assert ".py" in result.stdout
    assert ".md" in result.stdout


def test_stats_skips_venv(tmp_path):
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "inside.py").write_text("")
    (tmp_path / "a.py").write_text("")

    result = runner.invoke(app, ["stats", str(tmp_path)])

    assert result.exit_code == 0
    assert "共 1 个文件" in result.stdout


def test_stats_rejects_missing_dir(tmp_path):
    result = runner.invoke(app, ["stats", str(tmp_path / "not-exist")])

    assert result.exit_code == 1
    assert "不是目录" in result.stdout
