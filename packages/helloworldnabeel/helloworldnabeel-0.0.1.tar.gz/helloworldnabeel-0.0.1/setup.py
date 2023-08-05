from setuptools import setup

setup(
    name='helloworldnabeel',
    version='0.0.1',
    description='Say hello!',
    py_modules=["helloworld","helloworldtest"],
    package_dir={'':'src'},




)

#py setup.py bdist_wheel
#pip install -e .  --> it will not copy in sitepackages directory rather than it will link it

#create venv and try to run it

#we will need .gitignore file https://www.toptal.com/developers/gitignore

#we will need a license LICENSE.txt  https://choosealicense.com/

#readme.md

#py setup.py sdist --> for source distribution
#ls dist/
#To push to pypi we need twine

#pip install twine
#twine upload dist/*
