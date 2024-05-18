import sys
from enum import Enum, auto, unique
from textwrap import dedent
from typing import Final, List, Sequence

import click
import msgfy
import pytablewriter as ptw
from click.core import Context
from pathvalidate import (
    AbstractSanitizer,
    AbstractValidator,
    FileNameSanitizer,
    FileNameValidator,
    FilePathSanitizer,
    FilePathValidator,
    normalize_platform,
)
from pathvalidate.error import ErrorReason, ValidationError

from .__version__ import __version__
from ._const import MODULE_NAME
from ._logger import LogLevel, initialize_logger, logger


COMMAND_EPILOG: Final = dedent(
    f"""\
    Issue tracker: https://github.com/thombashi/{MODULE_NAME}/issues
    """
)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], obj={})


@unique
class ContextKey(Enum):
    CHECK_RESERVED = auto()
    LOG_LEVEL = auto()
    IS_FILENAME = auto()
    NORMALIZE = auto()
    MAX_LEN = auto()
    MIN_LEN = auto()
    PLATFORM = auto()
    VERBOSITY_LEVEL = auto()
    VALIDATE_AFTER_SANITIZE = auto()


def use_stdin(args: Sequence) -> bool:
    if sys.stdin.isatty():
        return False

    return len(args) == 1 and "-" in args


def print_err(e: ValidationError, fmt: str) -> None:
    if fmt == "jsonl":
        print(e.as_slog())
        return

    print(e)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, message="%(prog)s %(version)s")
@click.option("--debug", "log_level", flag_value=LogLevel.DEBUG, help="For debug print.")
@click.option(
    "-q",
    "--quiet",
    "log_level",
    flag_value=LogLevel.QUIET,
    help="Suppress execution log messages.",
)
@click.option("--filename", "is_filename", is_flag=True, help="Consider inputs as filenames.")
@click.option(
    "--max-len",
    "--max-bytes",
    metavar="BYTES",
    type=int,
    show_default=True,
    default=-1,
    help="Maximum byte counts of file paths. -1: same value as the platform limitation.",
)
@click.option(
    "--platform",
    metavar="PLATFORM",
    default="universal",
    show_default=True,
    help=" ".join(
        [
            "Target platform name (case-insensitive).",
            "Valid platform specifiers are Linux/Windows/macOS.",
            "Valid special values are: auto, universal, POSIX\n",
        ]
    )
    + """\
    (a) auto: automatically detects the execution platform.
    (b) universal: platform independent.
    (c) POSIX: POSIX-compliant platform.
""",
)
@click.option(
    "-v", "--verbose", "verbosity_level", help="Verbosity level", show_default=True, count=True
)
@click.pass_context
def cmd(
    ctx: Context,
    log_level: LogLevel,
    is_filename: bool,
    max_len: int,
    platform: str,
    verbosity_level: int,
) -> None:
    ctx.obj[ContextKey.LOG_LEVEL] = LogLevel.INFO if log_level is None else log_level
    ctx.obj[ContextKey.IS_FILENAME] = is_filename
    ctx.obj[ContextKey.MAX_LEN] = max_len
    ctx.obj[ContextKey.PLATFORM] = normalize_platform(platform)
    ctx.obj[ContextKey.VERBOSITY_LEVEL] = verbosity_level

    initialize_logger(name=f"{MODULE_NAME:s}", log_level=ctx.obj[ContextKey.LOG_LEVEL])

    for key, value in ctx.obj.items():
        logger.debug(f"{key}={value}")


def create_sanitizer(ctx: Context) -> AbstractSanitizer:
    kwargs = {
        "max_len": ctx.obj[ContextKey.MAX_LEN],
        "platform": ctx.obj[ContextKey.PLATFORM],
        "validate_after_sanitize": ctx.obj[ContextKey.VALIDATE_AFTER_SANITIZE],
    }

    if not ctx.obj[ContextKey.IS_FILENAME]:
        kwargs["normalize"] = ctx.obj[ContextKey.NORMALIZE]

    logger.debug(str(kwargs))

    if ctx.obj[ContextKey.IS_FILENAME]:
        return FileNameSanitizer(**kwargs)

    return FilePathSanitizer(**kwargs)


def create_validator(ctx: Context) -> AbstractValidator:
    kwargs = {
        "max_len": ctx.obj[ContextKey.MAX_LEN],
        "min_len": ctx.obj[ContextKey.MIN_LEN],
        "platform": ctx.obj[ContextKey.PLATFORM],
        "check_reserved": ctx.obj[ContextKey.CHECK_RESERVED],
    }

    if ctx.obj[ContextKey.IS_FILENAME]:
        return FileNameValidator(**kwargs)

    return FilePathValidator(**kwargs)


def to_error_reason_row(code: str) -> List[str]:
    for reason in ErrorReason:
        if reason.code != code:
            continue

        return [reason.code, reason.name, reason.description]

    raise ValueError(f"Error code {code} is not found.")


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
@click.argument("filepaths", type=str, nargs=-1)
@click.option(
    "--replacement-text",
    show_default=True,
    default="",
    help="""
    Replacement text for invalid characters.
    Defaults to an empty string (remove invalid strings).
    """,
)
@click.option(
    "--normalize",
    is_flag=True,
    help="Normalize the path.",
)
@click.option(
    "--validate-after-sanitize",
    is_flag=True,
    help="Execute validation after sanitization.",
)
def sanitize(
    ctx: Context,
    filepaths: List[str],
    replacement_text: str,
    normalize: bool,
    validate_after_sanitize: bool,
) -> None:
    """Sanitize file paths."""

    ctx.obj[ContextKey.VALIDATE_AFTER_SANITIZE] = validate_after_sanitize
    ctx.obj[ContextKey.NORMALIZE] = normalize

    if use_stdin(filepaths):
        filepaths = sys.stdin.read().splitlines()

    sanitizer = create_sanitizer(ctx)

    for filepath in filepaths:
        logger.debug(f"{sanitizer.__class__.__name__}: {filepath}")

        try:
            print(sanitizer.sanitize(filepath, replacement_text))
        except ValidationError as e:
            logger.error(msgfy.to_error_message(e))


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
@click.argument("filepaths", type=str, nargs=-1)
@click.option(
    "--min-len",
    "--min-bytes",
    metavar="BYTES",
    type=int,
    show_default=True,
    default=1,
    help="Minimum byte counts of file paths.",
)
@click.option("--no-check-reserved", is_flag=True, help="Check reserved names.")
def validate(ctx: Context, filepaths: List[str], min_len: int, no_check_reserved: bool) -> None:
    """Validate file paths."""

    if use_stdin(filepaths):
        filepaths = sys.stdin.read().splitlines()

    ctx.obj[ContextKey.CHECK_RESERVED] = not no_check_reserved
    ctx.obj[ContextKey.MIN_LEN] = min_len
    validator = create_validator(ctx)
    found_invalid = False

    for filepath in filepaths:
        logger.debug(f"{validator.__class__.__name__}: {filepath}")

        try:
            validator.validate(filepath)
        except ValidationError as e:
            print_err(e, fmt="text")
            found_invalid = True
            continue

        if ctx.obj[ContextKey.VERBOSITY_LEVEL] >= 1:
            logger.info(f"{filepath} is a valid path for {ctx.obj[ContextKey.PLATFORM].value}")

    if found_invalid:
        sys.exit(1)


@cmd.command(epilog=COMMAND_EPILOG)
@click.pass_context
@click.argument("codes", type=str, nargs=-1)
@click.option("--list", "list_errors", is_flag=True, help="List error reasons.")
def error(ctx: Context, codes: List[str], list_errors: bool) -> None:
    """Print error reasons."""

    if len(codes) == 0 and not list_errors:
        click.echo(ctx.get_help())
        ctx.exit()

    errors: List[List[str]] = []
    exit_code = 0

    if list_errors:
        errors = [[reason.code, reason.name, reason.description] for reason in ErrorReason]
    else:
        for code in codes:
            try:
                errors.append(to_error_reason_row(code))
            except ValueError as e:
                exit_code = 1
                click.echo(e)

    writer = ptw.MarkdownTableWriter(
        table_name="Error Reason",
        headers=["Code", "Name", "Description"],
        value_matrix=errors,
        margin=1,
    )
    writer.write_table()
    ctx.exit(exit_code)
