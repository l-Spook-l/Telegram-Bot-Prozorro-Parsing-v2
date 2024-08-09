#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

alembic upgrade head

source venv/bin/activate

TOKEN="$TOKEN"

python main.py

read -p "Press Enter to exit"