from setuptools import find_packages, setup

setup(
    name='exposureAPI',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'gspread',
        'oauth2client',
        'pandas',
        'flask_cors',
        'python-dateutil'
    ],
)
