.. contents:: **pathvalidate-cli**
   :backlinks: top
   :depth: 2


Summary
============================================

pathvalidate-cli is a command line interface for `pathvalidate <https://github.com/thombashi/pathvalidate>`__ library.


Installation
============================================
::

    pip install pathvalidate-cli


Usage
============================================

::

    $ pathvalidate sanitize 'fi:l*e/p"a?t>h|.t<xt'
    file/path.txt
    $ pathvalidate --filename sanitize 'fi:l*e/p"a?t>h|.t<xt'
    filepath.txt

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
                                    value with the platform limitation.  [default:
                                    -1]
      --platform PLATFORM           Execution platform name (case-insensitive).
                                    Valid platform specifiers are
                                    Linux/Windows/macOS. Valid special values are:
                                    POSIX, universal (a) auto: automatically
                                    detects the execution platform. (b) universal:
                                    platform independent.  [default: universal]
      -v, --verbose                 Verbosity level  [default: 0]
      -h, --help                    Show this message and exit.

    Commands:
      error     Print error reasons.
      sanitize  Sanitize file paths.
      validate  Validate file paths.


Dependencies
============================================
Python 3.8+
