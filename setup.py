from setuptools import setup, find_packages

from pycommon_test._version import __version__
setup(
    name='pycommon_test',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        # Used to manage testing of a Flask application
        'flask_testing==0.7.1',
        # Used to manage testing of Flask RestPlus components
        'flask-restplus==0.12.1',
    ],
    extras_require={
        'adam': [
            # Used to mock ADAM Rest service
            'responses==0.10.2',
        ],
    },
)
