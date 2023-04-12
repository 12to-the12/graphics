source ./venv/bin/activate
pip freeze > requirements.sh

# careful, if this is run outside of the virtual enviroment, it will overwrite the requirements file to be the system wide packages