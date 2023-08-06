# subprocess-check

Provides a wrapper that traces sub-process output, if captured.

## Uses

### Easier debugging when capturing output in a sub-process call

**Before**:

```python
import subprocess

result = subprocess.run(
    "echo error message >&2 && exit 1", shell=True, capture_output=True, check=True
)
```

Since the stderr output of the sub-process has been captured, we only see the command
and exit code:

```
$ python t.py
Traceback (most recent call last):
  File "t.py", line 3, in <module>
    result = subprocess.run(
  File "lib/python3.8/subprocess.py", line 512, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command 'echo error message >&2 && exit 1' returned non-zero exit status 1.
```

**After**:

```python
import subprocess

from subprocess_check import output_in_errors

with output_in_errors():
    result = subprocess.run(
        "echo error message >&2 && exit 1", shell=True, capture_output=True, check=True
    )
```

The stdout/stderr is traced right next to the exit code and command:

```
$ python t.py
Traceback (most recent call last):
  File "t.py", line 6, in <module>
    result = subprocess.run(
  File "lib/python3.8/site-packages/subprocess_check/_util.py", line 108, in wrap_subprocess_exception
    raise CalledProcessErrorWithOutput(exc_value).with_traceback(tb) from None
  File "lib/python3.8/subprocess.py", line 512, in run
    raise CalledProcessError(retcode, process.args,
subprocess_check._util.CalledProcessErrorWithOutput: Command 'echo error message >&2 && exit 1' returned non-zero exit status 1. Output captured:
 stdout: None
 stderr:
  error message
```

## Alternatives

1. Manual error handling/formatting:
   - :heavy_plus_sign: customizable formatting
   - :heavy_plus_sign: no dependencies
   - :heavy_minus_sign: ad-hoc code may not be tested as thoroughly
2. Don't capture stderr: 
   - :heavy_plus_sign: no dependencies
   - :heavy_minus_sign: output to terminal in non-error case may be verbose, if
     sub-process stderr outputs regardless
   - :heavy_minus_sign: if the error is re-raised after other operations, which
     output corresponds to the failed sub-process may not be nearby, or obvious
3. Wrap subprocess.run instead of using a context manager
   - :heavy_plus_sign: no need to pass `capture_output=True, check=True`
   - :heavy_minus_sign: IDEs do not understand "transparent function wrappers" well,
     so autocomplete and type hints are compromised
