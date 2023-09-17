import pytest
from click.testing import CliRunner

from pathvalidate_cli.main import cmd


class Test_validate_subcommand:
    @pytest.mark.parametrize(
        ["value", "options", "expected"],
        [
            [
                ["file/path.txt"],
                [],
                0,
            ],
            [
                ["file/path.txt", "abc.txt"],
                [],
                0,
            ],
            [
                [r'fi:l*e/p"a?t>h|.t<xt'],
                [],
                1,
            ],
        ],
    )
    def test_normal_filepath(self, value, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, ["validate"] + value + options)

        assert result.exit_code == expected

    @pytest.mark.parametrize(
        ["value", "options", "expected"],
        [
            [["filepath.txt"], [], 0],
            [[r'fi:l*e/p"a?t>h|.t<xt'], [], 1],
        ],
    )
    def test_normal_filename(self, value, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, ["--filename", "validate"] + value + options)

        assert result.exit_code == expected
