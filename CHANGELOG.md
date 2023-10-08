# Changelog

## :package: [3.0.1](https://pypi.org/project/commitment/3.0.1/) - 2023-10-08

* Convert python requirement to open range
* Tested on python 3.11, 3.12

## :package: [3.0.0](https://pypi.org/project/commitment/3.0.0/) - 2021-10-17

* Dropped testing on python < 3.7
* Tested on python 3.9, 3.10

## :package: [2.0.2](https://pypi.org/project/commitment/2.0.2/) - 2019-10-19

* Tested on python 3.8
* Adopt poetry for packaging

## :package: [2.0.1](https://pypi.org/project/commitment/2.0.1/) - 2018-12-02

Support python 3.7

## :package: [2.0.0](https://pypi.org/project/commitment/2.0.0/) - 2018-02-17

### Backwards-incompatible changes
* `GitHubCredentials` constructor signature changed from
  * `__init__(self, repo, branch, name, email, api_key)` to
  * `__init__(self, repo, name, email, api_key)`
* `GitHubClient.push_file()` signature changed from
  * `push_file(self, content, filename, message, encoding='utf-8')` to
  * `push_file(self, content, filename, message, branch='master', encoding='utf-8')`

### New Methods
* `GitHubClient.create_branch()`
* `GitHubClient.get_file_bytes()`
* `GitHubClient.get_file_str()`
* `GitHubClient.open_pull_request()`

## :package: [1.0.0](https://pypi.org/project/commitment/1.0.0/) - 2017-10-29

First Release
