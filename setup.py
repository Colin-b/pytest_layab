from setuptools import setup, find_packages

from pycommon_test._version import __version__
setup(
    name='pycommon_test',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        # Used to manage testing of a Flask application
        'flask_testing==0.6.2',
    ],
    extras_require={
        'testing': [
        ],
    },
)
