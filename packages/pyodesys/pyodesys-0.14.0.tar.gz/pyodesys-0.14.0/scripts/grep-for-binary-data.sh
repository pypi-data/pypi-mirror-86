#!/bin/bash
if grep '"image/png":' -R . --include "*.ipynb" --exclude-dir=venv --exclude-dir=deploy; then
    >&2 echo "You may not check in binary data into the repository."
    >&2 echo "See e.g. .jupyter/jupyter_notebook_config.py for how to exclude output."
    exit 1
fi
