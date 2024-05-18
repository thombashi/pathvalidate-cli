.. contents:: **pathvalidate-cli**
   :backlinks: top
   :depth: 2


Summary
============================================

``pathvalidate-cli`` is a command line interface for `pathvalidate <https://github.com/thombashi/pathvalidate>`__ library.
The tool can sanitize/validate strings such as file-names/file-paths.

|PyPI pkg ver| |Supported Python ver| |CI status| |CodeQL|

.. |PyPI pkg ver| image:: https://badge.fury.io/py/pathvalidate-cli.svg
    :target: https://badge.fury.io/py/pathvalidate-cli
    :alt: PyPI package version

.. |Supported Python ver| image:: https://img.shields.io/pypi/pyversions/pathvalidate-cli.svg
    :target: https://pypi.org/project/pathvalidate-cli
    :alt: Supported Python versions

.. |CI status| image:: https://github.com/thombashi/pathvalidate-cli/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/thombashi/pathvalidate-cli/actions/workflows/ci.yml
    :alt: CI status of Linux/macOS/Windows

.. |CodeQL| image:: https://github.com/thombashi/pathvalidate-cli/actions/workflows/github-code-scanning/codeql/badge.svg
    :target: https://github.com/thombashi/pathvalidate-cli/actions/workflows/github-code-scanning/codeql
    :alt: CodeQL


Installation
============================================
::

    pip install pathvalidate-cli


Usage
============================================

Sanitize file paths
--------------------------------------------

::

    $ pathvalidate sanitize 'fi:l*e/p"a?t>h|.t<xt'
    file/path.txt
    $ pathvalidate --filename sanitize 'fi:l*e/p"a?t>h|.t<xt'
    filepath.txt

Validate file paths
--------------------------------------------

::

    $ pathvalidate validate file/path.txt
    $ 
    $ pathvalidate validate 'fi:l*e/p"a?t>h|.t<xt'
    [PV1100] invalid characters found: invalids=(':', '*', '"', '?', '>', '|', '<'), value='fi:l*e/p"a?t>h|.t<xt', platform=Windows

Command Help
--------------------------------------------

::

    Usage: pathvalidate [OPTIONS] COMMAND [ARGS]...

    Options:
      --version                     Show the version and exit.
      --debug                       For debug print.
      -q, --quiet                   Suppress execution log messages.
      --filename                    Consider inputs as filenames.
      --max-len, --max-bytes BYTES  Maximum byte counts of file paths. -1: same
                                    value as the platform limitation.  [default:
                                    -1]
      --platform PLATFORM           Target platform name (case-insensitive). Valid
                                    platform specifiers are Linux/Windows/macOS.
                                    Valid special values are: auto, universal,
                                    POSIX (a) auto: automatically detects the
                                    execution platform. (b) universal: platform
                                    independent. (c) POSIX: POSIX-compliant
                                    platform.  [default: universal]
      --security-check              Enable security checks.
      -v, --verbose                 Verbosity level  [default: 0]
      -h, --help                    Show this message and exit.

    Commands:
      error     Print error reasons.
      sanitize  Sanitize file paths.
      validate  Validate file paths.


Dependencies
============================================
Python 3.8+


Related Project
============================================

- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
