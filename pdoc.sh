#!/bin/bash

echo "Generating documentation.  Please ignore any output until this script exits."
# Prevent any old files from being included.
rm -rf html
# pdoc fails when trying to parse the setup.py file so rename until the doc are produced. 
mv setup.py setup.not_py
pdoc --html .
mv setup.not_py setup.py

echo "All done. HTML produced in html dir."

