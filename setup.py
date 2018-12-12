from setuptools import setup, find_packages

setup(
    name='pycommon_test',
    version=open("pycommon_test/_version.py").readlines()[-1].split()[-1].strip("\"'"),
    packages=find_packages(),
    install_requires=[
        # Used to manage testing of a Flask application
        'flask_testing==0.7.1',
        # Used to manage testing of Flask RestPlus components
        'flask-restplus==0.12.1',
        # Used to mock API responses
        'responses==0.10.4',
        # Used to run tests
        'nose==1.3.7',
        # Used to check code coverage
        'coverage==4.5.2',
    ],
    extras_require={
        'testing': [
            # Used to manage responses testing
            'requests==2.21.0',
        ],
    },
)
