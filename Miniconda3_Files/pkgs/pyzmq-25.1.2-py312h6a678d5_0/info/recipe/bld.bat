set DISTUTILS_USE_SDK=1

set ZMQ_PREFIX=%LIBRARY_PREFIX%

"%PYTHON%" -m pip install --no-deps --no-build-isolation .
if errorlevel 1 exit 1
