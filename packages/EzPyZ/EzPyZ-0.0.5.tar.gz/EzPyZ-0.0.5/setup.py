"""
setup.py
~~~~~~~~
Sets up EzPyZ. Uses setup.cfg for configuration information.
"""

import setuptools

with open("README.md", "r") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

# Setup will be done using the information in setup.cfg
setuptools.setup(
    long_description=LONG_DESCRIPTION
)
