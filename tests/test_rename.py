from typer.testing import CliRunner

from file_tool import app

runner = CliRunner()


def test_rename_replaces_in_file_names(tmp_path):
    (tmp_path / "draft_report.md").write_text("")
    (tmp_path / "draft_notes.md").write_text("")
    (tmp_path / "other.txt").write_text("")

    result = runner.invoke(app, ["rename", str(tmp_path), "draft_", ""])

    assert result.exit_code == 0
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "notes.md").exists()
    assert (tmp_path / "other.txt").exists()
    assert "共处理 2 个文件" in result.stdout


def test_rename_skips_when_target_exists(tmp_path):
    (tmp_path / "a_old.txt").write_text("")
    (tmp_path / "a_new.txt").write_text("")

    result = runner.invoke(app, ["rename", str(tmp_path), "old", "new"])

    assert result.exit_code == 0
    assert (tmp_path / "a_old.txt").exists()
    assert (tmp_path / "a_new.txt").exists()
    assert "跳过" in result.stdout


def test_rename_rejects_missing_dir(tmp_path):
    result = runner.invoke(app, ["rename", str(tmp_path / "not-exist"), "a", "b"])

    assert result.exit_code == 1
    assert "不是目录" in result.stdout


def test_rename_dry_run_does_not_touch_files(tmp_path):
    (tmp_path / "old1.txt").write_text("")
    (tmp_path / "old2.txt").write_text("")

    result = runner.invoke(app, ["rename", str(tmp_path), "old", "new", "--dry-run"])

    assert result.exit_code == 0
    assert (tmp_path / "old1.txt").exists()
    assert (tmp_path / "old2.txt").exists()
    assert not (tmp_path / "new1.txt").exists()
    assert "预览" in result.stdout
