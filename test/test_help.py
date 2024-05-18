import pytest
from click.testing import CliRunner

from pathvalidate_cli.main import cmd


class Test_main:
    @pytest.mark.parametrize(
        ["options", "expected"],
        [
            [["-h"], 0],
            [["sanitize", "-h"], 0],
            [["validate", "-h"], 0],
            [["error", "-h"], 0],
        ],
    )
    def test_help(self, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, options)

        assert result.exit_code == expected
