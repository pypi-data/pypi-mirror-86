import subprocess
import sys
import textwrap
import traceback

import pytest

from subprocess_check import output_in_errors
from subprocess_check._util import _format_error_outputs


@pytest.mark.parametrize(
    "stdout,stderr,expected",
    [
        (None, None, None),
        ("a", None, " stdout:\n  a\n stderr: Not captured"),
        (None, "b", " stdout: Not captured\n stderr:\n  b"),
        ("a", "b", " stdout:\n  a\n stderr:\n  b"),
        ("a\n a2", " b\nb2", " stdout:\n  a\n   a2\n stderr:\n   b\n  b2"),
        (b"a", b"b", " stdout:\n  a\n stderr:\n  b"),
        (b"\xada", b"b\xad", " stdout:\n  �a\n stderr:\n  b�"),
    ],
)
def test_output_formatting(stdout, stderr, expected):
    e = subprocess.CalledProcessError(0, [], stdout, stderr)
    result = _format_error_outputs(e)
    assert result == expected


def test_output_in_errors_traces_output_in_errors():
    command = [
        sys.executable,
        "-c",
        textwrap.dedent(
            """
            import os
            import sys


            sys.stdout.write('stdout')
            sys.stderr.write('stderr')
            if os.environ.get("EXIT_1"):
                sys.exit(1)
            """,
        ),
    ]

    with output_in_errors():
        result = subprocess.run(command, check=True, capture_output=True)

    assert result.stdout == b"stdout"
    assert result.stderr == b"stderr"

    with pytest.raises(subprocess.CalledProcessError) as e:
        with output_in_errors():
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                env={"EXIT_1": "yes"},
            )

    exc = e.value
    traceback_text = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    )
    # Only 1 frame from our library is in the traceback
    assert traceback_text.count("subprocess_check/_util.py") == 1
    # subprocess.run only appears once
    assert traceback_text.count("subprocess.run") == 1

    assert exc.stdout == b"stdout"
    assert exc.stderr == b"stderr"
    assert str(exc).endswith("\n stdout:\n  stdout\n stderr:\n  stderr")
