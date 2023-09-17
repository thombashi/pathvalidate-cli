import pytest
from click.testing import CliRunner

from pathvalidate_cli.main import cmd


class Test_sanitize_subcommand:
    @pytest.mark.parametrize(
        ["value", "options", "expected"],
        [
            [
                [r'fi:l*e/p"a?t>h|.t<xt'],
                [],
                "file/path.txt\n",
            ],
        ],
    )
    def test_normal_filepath(self, value, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, ["sanitize"] + value + options)

        assert result.exit_code == 0
        assert result.output == expected

    @pytest.mark.parametrize(
        ["value", "options", "expected"],
        [
            [
                [r'fi:l*e/p"a?t>h|.t<xt'],
                [],
                "filepath.txt\n",
            ],
        ],
    )
    def test_normal_filename(self, value, options, expected):
        runner = CliRunner()
        result = runner.invoke(cmd, ["--filename", "sanitize"] + value + options)

        assert result.exit_code == 0
        assert result.output == expected
