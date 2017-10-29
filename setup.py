import os
from setuptools import setup

def _get_description():
    try:
        path = os.path.join(os.path.dirname(__file__), 'README.rst')
        with open(path, encoding='utf-8') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name='commitment',
    version='1.0.0',
    author="chris48s",
    license="MIT",
    description='Python 3 wrapper to push data to a GitHub repo using the GitHub contents api',
    long_description=_get_description(),
    url="https://github.com/chris48s/commitment/",
    packages=['commitment'],
    install_requires=[
        'requests'
    ],
)
