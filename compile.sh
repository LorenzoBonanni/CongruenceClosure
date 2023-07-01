#!/bin/bash
source venv/bin/activate
pyinstaller --onefile main.py --hidden-import="PIL._tkinter_finder" --clean -n congruenceClosure
pyinstaller --onefile runner.py --hidden-import="PIL._tkinter_finder" --clean -n runner
