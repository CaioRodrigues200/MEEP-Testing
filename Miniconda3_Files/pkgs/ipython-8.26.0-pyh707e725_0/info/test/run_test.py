#  tests for ipython-8.26.0-pyh707e725_0 (this is a generated file);
print('===== testing package: ipython-8.26.0-pyh707e725_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import subprocess
import platform
import os
import sys
from pathlib import Path
import IPython

WIN = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
PYPY = "__pypy__" in sys.builtin_module_names
PPC = "ppc" in platform.machine()

COV_THRESHOLD = os.environ.get("COV_THRESHOLD")

# Environment variable should be set in the meta.yaml
MIGRATING = eval(os.environ.get("MIGRATING", "None"))

PYTEST_SKIPS = ["decorator_skip", "pprint_heap_allocated"]
PYTEST_ARGS = [sys.executable, "-m", "pytest", "-vv"]

IGNORE_GLOBS = [
    "consoleapp.py",
    "external/*.py",
    "sphinxext/*.py",
    "terminal/console*.py",
    "terminal/pt_inputhooks/*.py",
    "utils/*.py",
]

PYTEST_ARGS += sum([[f"--ignore-glob", glob] for glob in IGNORE_GLOBS], [])

if WIN:
    pass
else:
    pass

if LINUX:
    PYTEST_SKIPS += ["system_interrupt"]

if PPC:
    PYTEST_SKIPS += ["ipython_dir_8", "audio_data"]

if COV_THRESHOLD is not None:
    PYTEST_ARGS += [
        "--cov", "IPython", "--no-cov-on-fail", "--cov-fail-under", COV_THRESHOLD,
        "--cov-report", "term-missing:skip-covered"
    ]

if len(PYTEST_SKIPS) == 1:
    PYTEST_ARGS += ["-k", f"not {PYTEST_SKIPS[0]}"]
elif PYTEST_SKIPS:
    PYTEST_ARGS += ["-k", f"""not ({" or ".join(PYTEST_SKIPS) })"""]

if __name__ == "__main__":
    print("Building on Windows?      ", WIN)
    print("Building on Linux?        ", LINUX)
    print("Building for PyPy?        ", PYPY)

    if MIGRATING:
        print("This is a migration, skipping test suite! Put it back later!", flush=True)
        sys.exit(0)
    else:
        print("Running pytest with args")
        print(PYTEST_ARGS, flush=True)
        sys.exit(subprocess.call(PYTEST_ARGS, cwd=str(Path(IPython.__file__).parent)))
#  --- run_test.py (end) ---

print('===== ipython-8.26.0-pyh707e725_0 OK =====');
print("import: 'IPython'")
import IPython

print("import: 'IPython.core'")
import IPython.core

print("import: 'IPython.core.magics'")
import IPython.core.magics

print("import: 'IPython.core.tests'")
import IPython.core.tests

print("import: 'IPython.extensions'")
import IPython.extensions

print("import: 'IPython.extensions.tests'")
import IPython.extensions.tests

print("import: 'IPython.external'")
import IPython.external

print("import: 'IPython.lib'")
import IPython.lib

print("import: 'IPython.lib.tests'")
import IPython.lib.tests

print("import: 'IPython.sphinxext'")
import IPython.sphinxext

print("import: 'IPython.terminal'")
import IPython.terminal

print("import: 'IPython.terminal.pt_inputhooks'")
import IPython.terminal.pt_inputhooks

print("import: 'IPython.terminal.tests'")
import IPython.terminal.tests

print("import: 'IPython.testing'")
import IPython.testing

print("import: 'IPython.testing.plugin'")
import IPython.testing.plugin

print("import: 'IPython.testing.tests'")
import IPython.testing.tests

print("import: 'IPython.utils'")
import IPython.utils

print("import: 'IPython.utils.tests'")
import IPython.utils.tests

