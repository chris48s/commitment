# commitment

[![Build Status](https://travis-ci.org/chris48s/commitment.svg?branch=master)](https://travis-ci.org/chris48s/commitment)
[![Coverage Status](https://coveralls.io/repos/github/chris48s/commitment/badge.svg?branch=master)](https://coveralls.io/github/chris48s/commitment?branch=master)
![PyPI Version](https://img.shields.io/pypi/v/commitment.svg)
![License](https://img.shields.io/pypi/l/commitment.svg)
![Python Support](https://img.shields.io/pypi/pyversions/commitment.svg)

Python 3 wrapper to push data to a GitHub repo using the GitHub [contents api](https://developer.github.com/v3/repos/contents/)

## Installation

`pip install commitment`

## Usage

Generate a GitHub API key: https://github.com/settings/tokens

```python
from commitment import GitHubCredentials, GitHubClient

credentials = GitHubCredentials(
    repo="myuser/somerepo",
    branch='master',
    name="myuser",
    email="someone@example.com",
    api_key="f00b42",
)

client = GitHubClient(credentials)

g.push_file('Hello World!', 'directory/filename.txt', 'my commit message')
```
