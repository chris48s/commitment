# commitment

Python 3 wrapper to push data to a GitHub repo using the GitHub [contents api](https://developer.github.com/v3/repos/contents/)

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

## Licensing

`commitment` is made available under the MIT License
