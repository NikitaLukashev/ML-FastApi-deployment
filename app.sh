#!/usr/bin/env bash

# Set current directory to the directory of the file
cd $(dirname $0)

# Use the pip virtualenv
/bin/bash -c "allisone/bin/activate; exec /bin/bash -i"

#add PYTHONPATH
PYTHONPATH=$PYTHONPATH:$(dirname $0)/src
export PYTHONPATH

# Run migration
alembic upgrade head

# Start app
exec python ./src/main.py
