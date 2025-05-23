#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import unittest
from unittest import mock

import requests

from commitment import GitHubClient, GitHubCredentials


# GitHubClient._get_file() mocks
def mock_get_file_return_foo(obj, filename, branch):
    return b"foo"


def mock_get_file_raise_500(obj, filename, branch):
    resp = requests.Response()
    resp.status_code = 500
    raise requests.exceptions.HTTPError(response=resp)


def mock_get_file_raise_404(obj, filename, branch):
    resp = requests.Response()
    resp.status_code = 404
    raise requests.exceptions.HTTPError(response=resp)


# request mocks
def mock_request_success(obj, *args, **kwargs):
    resp = requests.Response()
    resp.status_code = 201
    return resp


def mock_request_failure(obj, *args, **kwargs):
    resp = requests.Response()
    resp.status_code = 500
    return resp


# requests.json() mock
def mock_json(obj, **kwargs):
    return ""


class GitHubClientTests(unittest.TestCase):
    def setUp(self):
        self.creds = GitHubCredentials(
            repo="myuser/somerepo",
            name="myuser",
            email="chad.fernandez@example.com",
            api_key="f00b42",
        )

    def test_init_invalid(self):
        with self.assertRaises(TypeError):
            GitHubClient("cheese")

    def test_init_valid(self):
        g = GitHubClient(self.creds)
        self.assertIsInstance(g, GitHubClient)

    def test_get_contents_payload_utf8_no_parent(self):
        g = GitHubClient(self.creds)
        payload = json.loads(
            g._get_contents_payload("abcd", "commit my file", "branch")
        )
        self.assertEqual("commit my file", payload["message"])
        self.assertEqual("branch", payload["branch"])
        self.assertEqual(self.creds.name, payload["committer"]["name"])
        self.assertEqual(self.creds.email, payload["committer"]["email"])
        self.assertEqual("YWJjZA==", payload["content"])
        self.assertFalse("sha" in payload)

    def test_get_contents_payload_windows1252(self):
        g = GitHubClient(self.creds)
        content = b"you\xe2\x80\x99re".decode("windows-1252")
        payload = json.loads(
            g._get_contents_payload(
                content, "commit my file", "branch", encoding="windows-1252"
            )
        )
        self.assertEqual(b"you\xe2\x80\x99re", base64.b64decode(payload["content"]))

    def test_get_contents_payload_with_parent(self):
        g = GitHubClient(self.creds)
        payload = json.loads(
            g._get_contents_payload(
                "abcd", "commit my file", "branch", parent_sha="xyz"
            )
        )
        self.assertEqual("xyz", payload["sha"])

    def test_get_blob_sha_invalid(self):
        g = GitHubClient(self.creds)
        with self.assertRaises(TypeError):
            g._get_blob_sha("not bytes")

    def test_get_blob_sha_valid(self):
        g = GitHubClient(self.creds)
        sha = g._get_blob_sha(b"bytes")
        self.assertEqual(40, len(sha))

    @mock.patch("commitment.GitHubClient.get_file_bytes", mock_get_file_return_foo)
    def test_push_file_remote_file_equals_local_file(self):
        g = GitHubClient(self.creds)
        res = g.push_file("foo", "foo/bar.baz", "my commit message")
        # If the local content is the same as
        # the remote content push_file() should do nothing
        self.assertIsNone(res)

    @mock.patch("commitment.GitHubClient.get_file_bytes", mock_get_file_raise_404)
    @mock.patch("requests.request", mock_request_success)
    def test_push_file_no_remote_file(self):
        g = GitHubClient(self.creds)
        res = g.push_file("foo", "foo/bar.baz", "my commit message")
        # If no remote content exists
        # push_file() should push the local content
        self.assertEqual(201, res.status_code)

    @mock.patch("commitment.GitHubClient.get_file_bytes", mock_get_file_return_foo)
    @mock.patch("requests.request", mock_request_success)
    def test_push_file_remote_file_not_equal_local_file(self):
        g = GitHubClient(self.creds)
        res = g.push_file("bar", "foo/bar.baz", "my commit message")
        # If remote content != local content
        # push_file() should push the local content
        self.assertEqual(201, res.status_code)

    @mock.patch("commitment.GitHubClient.get_file_bytes", mock_get_file_raise_500)
    def test_push_file_remote_file_raises_500(self):
        g = GitHubClient(self.creds)
        # if getting remote content raises
        # push_file() should re-raise
        with self.assertRaises(requests.exceptions.HTTPError):
            g.push_file("foo", "foo/bar.baz", "my commit message")

    @mock.patch("commitment.GitHubClient.get_file_bytes", mock_get_file_raise_404)
    @mock.patch("requests.request", mock_request_failure)
    @mock.patch("requests.Response.json", mock_json)
    def test_push_file_put_failure(self):
        g = GitHubClient(self.creds)
        # if put() raises
        # push_file() should re-raise
        with self.assertRaises(requests.exceptions.HTTPError):
            g.push_file("foo", "foo/bar.baz", "my commit message")

    @mock.patch("requests.get", mock_request_success)
    @mock.patch("requests.Response.json", lambda x: {"object": {"sha": "foo"}})
    def test_get_head_sha_success(self):
        g = GitHubClient(self.creds)
        self.assertEqual("foo", g._get_head_sha("master"))

    @mock.patch("requests.get", mock_request_failure)
    def test_get_head_sha_failure(self):
        g = GitHubClient(self.creds)
        with self.assertRaises(requests.exceptions.HTTPError):
            g._get_head_sha("master")

    @mock.patch("requests.request", mock_request_success)
    def test_open_pull_request_success(self):
        g = GitHubClient(self.creds)
        res = g.open_pull_request("foo", "bar", "baz")
        self.assertEqual(201, res.status_code)

    @mock.patch("requests.request", mock_request_failure)
    @mock.patch("requests.Response.json", mock_json)
    def test_open_pull_request_failure(self):
        g = GitHubClient(self.creds)
        with self.assertRaises(requests.exceptions.HTTPError):
            g.open_pull_request("foo", "bar", "baz")

    @mock.patch("commitment.GitHubClient._get_head_sha", lambda x, y: "foo")
    @mock.patch("requests.request", mock_request_success)
    def test_create_branch_success(self):
        g = GitHubClient(self.creds)
        res = g.create_branch("foo")
        self.assertEqual(201, res.status_code)

    @mock.patch("commitment.GitHubClient._get_head_sha", lambda x, y: "foo")
    @mock.patch("requests.request", mock_request_failure)
    @mock.patch("requests.Response.json", mock_json)
    def test_create_branch_failure(self):
        g = GitHubClient(self.creds)
        with self.assertRaises(requests.exceptions.HTTPError):
            g.create_branch("foo")


if __name__ == "__main__":
    unittest.main()
