This module is responsible for persisting users and handling communicaton with AWS Cognito.

## Create Package

pip3 install setuptools twine 
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*

pip install YOURPACKAGE --upgrade