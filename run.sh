#!/bin/bash
py src/controller/main.py 2>/dev/null || python3 src/controller/main.py || python src/controller/main.py
