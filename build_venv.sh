#/bin/bash
rm -rf venv
python3.10 -m venv venv
which python
source venv/bin/activate
which python
pip install --upgrade pip
# poetry install

# pip install -r requirements.txt