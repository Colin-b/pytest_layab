import os

from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="pytest_layab",
    version=open("pytest_layab/version.py").readlines()[-1].split()[-1].strip("\"'"),
    description="Pytest fixtures for layab.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        # Used to manage testing of a Flask application
        "pytest-flask==0.15.0",
    ],
    python_requires=">=3.6",
    project_urls={
        "Changelog": "https://github.tools.digital.engie.com/GEM-Py/pytest_layab/blob/master/CHANGELOG.md",
        "Issues": "https://github.tools.digital.engie.com/GEM-Py/pytest_layab/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Build Tools",
    ],
    keywords=["test", "flask"],
    platforms=["Windows", "Linux"],
)
