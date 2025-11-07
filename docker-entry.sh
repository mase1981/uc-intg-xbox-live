#!/bin/bash

cd /usr/src/app
pip install --no-cache-dir -q -r requirements.txt
python uc_intg_xbox_live/driver.py