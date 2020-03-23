#!/bin/bash

# pdoc fails when trying to parse the setup.py file so rename until the doc are produced. 
mv setup.py setup.not_py
pdoc --html .
mv setup.not_py setup.py

echo "HTML produced in html dir."

