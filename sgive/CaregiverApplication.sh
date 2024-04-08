#!/bin/bash
################################################################################
# Shell launcher for Caregiver Application				       #
################################################################################

# Zjistí cestu ke skriptu
# CURRENT_DIR=$(find / -type d -not \( -path '*/.cache/*' -o -path '*/cache/*' \) -type d -name "sgive" -print 2>/dev/null)
CURRENT_DIR=$(dirname "$(realpath "$0")")
 echo "pokus s direm:", $(dirname "$(realpath "$0")")

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
    python -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
else
    source "$VENV_DIR/bin/activate"
fi

RED='\033[0;31m'
NC='\033[0m' # No Color
echo -e "${RED}Checking for dependencies ---------------------------------------------------------------------------------------------------${NC}"

# install or check for requirements:
pip install -r "$REQUIREMENTS_PATH"

echo -e "${RED}Done  ------------------------------------------------------------------------------------------------------------------------${NC}"

# 
cd "$WORKING_DIR"

# start the application
python -m main

# deactivate venv
deactivate
