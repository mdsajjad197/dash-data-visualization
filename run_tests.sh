#!/usr/bin/env bash

cd "$(dirname "$0")" || exit 1

if [ -f "venv/bin/activate" ]; then
    source "venv/bin/activate"
elif [ -f "venv/Scripts/activate" ]; then
    source "venv/Scripts/activate"
else
    echo "Virtual environment not found."
    exit 1
fi

python process_data.py || exit 1
python -m pytest
test_result=$?

if [ "$test_result" -eq 0 ]; then
    echo "All tests passed."
    exit 0
fi

echo "Tests failed."
exit 1
