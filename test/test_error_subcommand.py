import pytest
from click.testing import CliRunner

from pathvalidate_cli.main import cmd


class Test_error_subcommand:
    @pytest.mark.parametrize(
        ["value", "options", "expected"],
        [
            [
                ["PV1001"],
                [],
                0,
            ],
            [
                ["PV1001", "PV1002"],
                [],
                0,
            ],
            [
                [],
                ["--list"],
                0,
            ],
        ],
    )
    def test_normal(self, value, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, ["error"] + value + options)

        assert result.exit_code == expected
        assert result.output

    @pytest.mark.parametrize(
        ["value", "options", "expected"],
        [
            [["INVALID"], [], 1],
        ],
    )
    def test_normal_filename(self, value, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, ["error"] + value + options)

        assert result.exit_code == expected
