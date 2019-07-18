from setuptools import setup, find_packages

setup(
    name="pycommon_test",
    version=open("pycommon_test/version.py").readlines()[-1].split()[-1].strip("\"'"),
    packages=find_packages(),
    install_requires=[
        # Used to manage testing of a Flask application
        "pytest-flask==0.15.0",
        # Used to manage testing of Flask RestPlus components
        "flask-restplus==0.12.1",
        # Used to mock API responses
        "responses==0.10.6",
        # Used to run tests and cover
        "pytest-cov==2.7.1",
    ],
    extras_require={
        "testing": [
            # Used to manage responses testing
            "requests==2.22.0",
            # Used by LDAP mock
            "ldap3==2.6",
        ]
    },
)
