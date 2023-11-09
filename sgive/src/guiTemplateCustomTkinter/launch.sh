#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:/home/ryuseless/GitHub/senior-os/sgive/src/CaregiverApp"; # adding path to PYTHONPATH
source /home/ryuseless/GitHub/senior-os/venv/bin/activate; # starting venv
cd /home/ryuseless/GitHub/senior-os && python sgive/src/guiTemplateCustomTkinter/guiTempCTK.py; # running script