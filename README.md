# commitment

[![Build Status](https://travis-ci.org/chris48s/commitment.svg?branch=master)](https://travis-ci.org/chris48s/commitment)
[![Coverage Status](https://coveralls.io/repos/github/chris48s/commitment/badge.svg?branch=master)](https://coveralls.io/github/chris48s/commitment?branch=master)
![PyPI Version](https://img.shields.io/pypi/v/commitment.svg)
![License](https://img.shields.io/pypi/l/commitment.svg)
![Python Support](https://img.shields.io/pypi/pyversions/commitment.svg)

An incomplete Python 3 wrapper for the [GitHub API](https://developer.github.com/v3/).

Note this project does not aim to provide a complete abstraction over the GitHub API - just a few high-level convenience methods for pushing data to a GitHub repo.

## Installation

`pip install commitment`

## Usage

Generate a GitHub API key: https://github.com/settings/tokens

```python
from commitment import GitHubCredentials, GitHubClient

credentials = GitHubCredentials(
    repo="myuser/somerepo",
    name="myuser",
    email="someone@example.com",
    api_key="f00b42",
)

client = GitHubClient(credentials)

client.create_branch('my_new_branch', base_branch='master')
client.push_file('Hello World!', 'directory/filename.txt', 'my commit message', branch='my_new_branch')
client.open_pull_request('my_new_branch', 'title', 'body', base_branch='master')
```
