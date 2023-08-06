import inspect
import subprocess
import textwrap
from types import TracebackType
from typing import Optional


def _format_error_outputs(e: subprocess.CalledProcessError) -> Optional[str]:
    """
    If output or stderr is present on the provided error, returns a
    string with it formatted like

    ```
     stdout:
      stdout text, indented two columns, 1 column relative to the output
      labels
     stderr:
      stderr text, formatted similar to stdout text
    ```
    """
    chunks = []

    if e.output is None and e.stderr is None:
        return None

    if e.output is None:
        chunks.append(" stdout: Not captured")
    elif not len(e.output):
        chunks.append(" stdout: None")
    else:
        chunks.append(" stdout:")

        if isinstance(e.output, str):
            text = e.output
        else:
            text = e.output.decode("utf-8", errors="replace")

        chunks.append(textwrap.indent(text, "  "))

    if e.stderr is None:
        chunks.append(" stderr: Not captured")
    elif not len(e.stderr):
        chunks.append(" stderr: None")
    else:
        chunks.append(" stderr:")

        if isinstance(e.stderr, str):
            text = e.stderr
        else:
            text = e.stderr.decode("utf-8", errors="replace")

        chunks.append(textwrap.indent(text, "  "))

    return "\n".join(chunks)


class CalledProcessErrorWithOutput(subprocess.CalledProcessError):
    def __init__(self, exc: subprocess.CalledProcessError):
        super().__init__(exc.returncode, exc.cmd, exc.output, exc.stderr)

    def __str__(self) -> str:
        # The standard library representation already contains command and exit
        # code/signal.
        base_text = super().__str__()

        output_text = _format_error_outputs(self)

        if output_text is None:
            return f"{base_text} No output captured."

        return f"{base_text} Output captured:\n{output_text}"


def _strip_common_frames(traceback: TracebackType) -> Optional[TracebackType]:
    # When unwinding the stack, Python unconditionally prepends frames
    # to the active exception's traceback, including the frame in which it was
    # raised.
    #
    # When raising a new exception from a context manager's `__exit__` callback,
    # at least one frame ends up being common between the previously active
    # exception's traceback and the new exception's traceback, so a straightforward
    # `raise Exception().with_traceback(old_exc.__traceback__)`, leads to duplicate
    # frames.
    #
    # To prevent this and display a cleaner stack, we drop those common frame(s).
    current_frame = inspect.currentframe()
    # Implementation doesn't support stack frames.
    if current_frame is None:
        return traceback

    callers = {f.frame for f in inspect.getouterframes(current_frame)}

    traceback_item: Optional[TracebackType] = traceback
    while traceback_item is not None and traceback_item.tb_frame in callers:
        traceback_item = traceback_item.tb_next
    return traceback_item


# Slightly cleaner stack than using contextlib.contextmanager
class ReraisingContextWrapper:
    def __enter__(self):
        pass

    # Nicer name so stack is less confusing.
    def wrap_subprocess_exception(self, _exc_type, exc_value, exc_tb):
        if isinstance(exc_value, subprocess.CalledProcessError):
            tb = _strip_common_frames(exc_tb)
            raise CalledProcessErrorWithOutput(exc_value).with_traceback(tb) from None

    __exit__ = wrap_subprocess_exception


output_in_errors = ReraisingContextWrapper
