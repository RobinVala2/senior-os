#!/bin/bash
################################################################################
# Shell launcher for Caregiver Application				       #
################################################################################
# current dir, up to /sgive /user/home.../senior-os/sgive
CURRENT_DIR="$PWD"

# application working dirrectory:
WORKING_DIR="$CURRENT_DIR/src/CaregiverApp"

BASE_DIR=$(dirname "$CURRENT_DIR")

# Nastavení PYTHONPATH
export PYTHONPATH="$WORKING_DIR:$PYTHONPATH" # working dir
export PYTHONPATH="$PYTHONPATH:$BASE_DIR" # python dir

# venv and requirements paths
VENV_DIR="$BASE_DIR/venv"
REQUIREMENTS_PATH="$CURRENT_DIR/requirements.txt"

# create new venv, if there is not one already
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -r "$REQUIREMENTS_PATH"
else
    source "$VENV_DIR/bin/activate"
fi

# 
cd "$WORKING_DIR"

# start the application
python -m main

# deactivate venv
deactivate

