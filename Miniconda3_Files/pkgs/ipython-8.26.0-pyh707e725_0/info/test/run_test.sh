

set -ex



pip check
pygmentize -L | grep ipython
ipython -h
ipython3 -h
mypy -p IPython || exit 0
exit 0
