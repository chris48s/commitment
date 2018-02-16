import json
import base64
import requests
import urllib.parse
from hashlib import sha1


def force_bytes(data, encoding='utf-8'):
    if isinstance(data, (bytes, bytearray)):
        return data
    return bytes(data, encoding)


class GitHubCredentials:

    def __init__(self, repo, name, email, api_key):
        self.repo = repo
        self.name = name
        self.email = email
        self.api_key = api_key


class GitHubClient:

    def __init__(self, credentials):
        if not isinstance(credentials, GitHubCredentials):
            raise TypeError('expected GitHubCredentials object')
        self.credentials = credentials
        self.base_url = 'https://api.github.com/'

    def _request(self, method, url, payload):
        r = requests.request(
            method,
            url,
            data=payload,
            headers={'Authorization': 'token %s' % (self.credentials.api_key)}
        )
        if r.status_code not in [200, 201]:
            print(r.json())
        r.raise_for_status()
        return r.status_code

    def _get_contents_payload(self, content, message, branch, parent_sha=None, encoding='utf-8'):
        # assemble a payload we can use to make a request
        # to the /contents endpoint in the GitHub API
        # https://developer.github.com/v3/repos/contents/#create-a-file
        payload = {
            'message': message,
            'content': base64.b64encode(
                force_bytes(content, encoding)).decode('utf-8'),
            'branch': branch,
            "committer": {
                "name": self.credentials.name,
                "email": self.credentials.email
            },
        }
        # if we're updating, we need to set the 'sha' key
        # https://developer.github.com/v3/repos/contents/#update-a-file
        if parent_sha:
            payload['sha'] = parent_sha
        return json.dumps(payload)

    def _get_file(self, filename, branch):
        url = 'https://raw.githubusercontent.com/%s/%s/%s' % (
            urllib.parse.quote(self.credentials.repo),
            urllib.parse.quote(branch),
            urllib.parse.quote(filename)
        )
        r = requests.get(url)
        r.raise_for_status()
        return r

    def _get_blob_sha(self, data):
        # work out the git SHA of a blob
        # (this is not the same as the commit SHA)
        # https://stackoverflow.com/questions/552659/how-to-assign-a-git-sha1s-to-a-file-without-git/552725#552725
        s = sha1()
        s.update(("blob %u\0" % len(data)).encode('utf-8'))
        s.update(data)
        return s.hexdigest()

    def _get_head_sha(self, branch):
        # get the HEAD commit SHA of `branch`
        url = self.base_url + 'repos/%s/git/refs/heads/%s' % (
            urllib.parse.quote(self.credentials.repo),
            urllib.parse.quote(branch)
        )
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data['object']['sha']

    def get_file_bytes(self, filename, branch='master'):
        r = self._get_file(filename, branch)
        return r.content

    def get_file_str(self, filename, branch='master'):
        r = self._get_file(filename, branch)
        return r.text

    def create_branch(self, new_branch, base_branch='master'):
        url = self.base_url + 'repos/%s/git/refs' % (
            urllib.parse.quote(self.credentials.repo)
        )
        payload = json.dumps({
            "ref": "refs/heads/%s" % (new_branch),
            "sha": self._get_head_sha(base_branch)
        })
        return self._request('POST', url, payload)

    def push_file(self, content, filename, message, branch='master', encoding='utf-8'):
        try:
            repo_content = self.get_file_bytes(filename, branch)
            # check if we need to do a commit because the /contents
            # endpoint will allow us to make an empty commit
            if force_bytes(content, encoding) == repo_content:
                payload = None
            else:
                payload = self._get_contents_payload(
                    content,
                    message,
                    branch,
                    parent_sha=self._get_blob_sha(repo_content),
                    encoding=encoding
                )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                payload = self._get_contents_payload(
                    content, message, branch, encoding=encoding)
            else:
                raise

        if payload:
            url = self.base_url + 'repos/%s/contents/%s' % (
                urllib.parse.quote(self.credentials.repo),
                urllib.parse.quote(filename)
            )
            return self._request('PUT', url, payload)
        else:
            return None

    def open_pull_request(self, head_branch, title, body, base_branch='master'):
        url = self.base_url + 'repos/%s/pulls' % (
            urllib.parse.quote(self.credentials.repo)
        )
        payload = json.dumps({
            "title": title,
            "body": body,
            "head": head_branch,
            "base": base_branch,
            "maintainer_can_modify": True,
        })
        return self._request('POST', url, payload)
