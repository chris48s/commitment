# commitment

[![Run tests](https://github.com/chris48s/commitment/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/chris48s/commitment/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/chris48s/commitment/branch/master/graph/badge.svg?token=4BL8HL7913)](https://codecov.io/gh/chris48s/commitment)
![PyPI Version](https://img.shields.io/pypi/v/commitment.svg)
![License](https://img.shields.io/pypi/l/commitment.svg)
![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fcommitment%2Fjson)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

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

## Versioning

commitment follows [semantic versioning](https://semver.org/).

From version 4 onwards, commitment will drop compatibility with unsupported python versions without incrementing the major version. This is in line with common practice in the python community.
