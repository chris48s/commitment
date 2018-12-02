import os
from setuptools import setup

def _get_description():
    try:
        path = os.path.join(os.path.dirname(__file__), 'README.md')
        with open(path, encoding='utf-8') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name='commitment',
    version='2.0.0',
    author="chris48s",
    license="MIT",
    description='An incomplete Python 3 wrapper for the GitHub API',
    long_description=_get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/chris48s/commitment/",
    packages=['commitment'],
    install_requires=[
        'requests'
    ],
    extras_require={
        'testing': [
            'python-coveralls',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
