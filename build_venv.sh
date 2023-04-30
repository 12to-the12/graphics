#/bin/bash
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
# pip install -r requirements.txt