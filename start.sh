#!/bin/bash
alembic upgrade head
python -m flask run --host=0.0.0.0
