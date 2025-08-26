#!/bin/bash

echo "Running Python code linting and formatting..."

echo "1. Checking if linting tools are installed..."
if ! command -v isort &> /dev/null || ! command -v black &> /dev/null || ! command -v flake8 &> /dev/null; then
    echo "Installing missing linting tools..."
    pip install flake8 black isort
fi

echo "2. Sorting imports with isort..."
isort main.py

echo "3. Formatting code with black..."
black main.py

echo "4. Running flake8 linter..."
flake8 main.py

echo "Linting complete!"