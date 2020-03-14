from unittest import mock

import pytest
import requests

from skep.platforms import windows_support_url


def test_unsupported_version():
    "If the major.minor version isn't supported, raise an error"
    with pytest.raises(ValueError):
        windows_support_url(version='2.7', host_arch=None, revision=None)


def test_find_version_default_arch(monkeypatch):
    "A windows version can be found with the default architecture"
    mock_head = mock.MagicMock()

    # Set up responses such that the following versions exsit:
    # * Python 3.7.5
    # * Python 3.7.6.post1
    # * Python 3.7.7 (known bad)
    # Python 3.7.6.post1 will be the best candidate.
    mock_head.side_effect = [
        mock.MagicMock(status_code=200),
        mock.MagicMock(status_code=404),
        mock.MagicMock(status_code=200),
        mock.MagicMock(status_code=404),
    ]
    monkeypatch.setattr(requests, 'head', mock_head)

    url = windows_support_url(version='3.7', host_arch=None, revision=None)

    # Three URLs were tested
    mock_head.assert_has_calls([
        mock.call('https://www.python.org/ftp/python/3.7.5/python-3.7.5-embed-amd64.zip'),
        mock.call('https://www.python.org/ftp/python/3.7.6/python-3.7.6-embed-amd64.zip'),
        mock.call('https://www.python.org/ftp/python/3.7.6/python-3.7.6.post1-embed-amd64.zip'),
        mock.call('https://www.python.org/ftp/python/3.7.7/python-3.7.7.post1-embed-amd64.zip'),
    ])

    # The second last one is the one returned.
    assert url == 'https://www.python.org/ftp/python/3.7.6/python-3.7.6.post1-embed-amd64.zip'


def test_explicit_revision_default_arch(monkeypatch):
    "A specific windows version will be returned if requested"
    mock_head = mock.MagicMock()
    monkeypatch.setattr(requests, 'head', mock_head)

    url = windows_support_url(version='3.7', host_arch=None, revision='4')

    # No URLs were tested
    mock_head.assert_not_called()

    # The explicit revision is returned
    assert url == 'https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-amd64.zip'


def test_explicit_post_revision(monkeypatch):
    "A specific windows post-release version will be returned if requested"
    mock_head = mock.MagicMock()
    monkeypatch.setattr(requests, 'head', mock_head)

    url = windows_support_url(version='3.7', host_arch=None, revision='4.post1')

    # No URLs were tested
    mock_head.assert_not_called()

    # The explicit revision is returned
    assert url == 'https://www.python.org/ftp/python/3.7.4/python-3.7.4.post1-embed-amd64.zip'


def test_find_version_explicit_arch(monkeypatch):
    "A windows version can be found with an explicit architecture"
    mock_head = mock.MagicMock()
    # Find the first two candidate micro versions.
    mock_head.side_effect = [
        mock.MagicMock(status_code=200),
        mock.MagicMock(status_code=200),
        mock.MagicMock(status_code=404),
    ]
    monkeypatch.setattr(requests, 'head', mock_head)

    url = windows_support_url(version='3.7', host_arch='win32', revision=None)

    # Three URLs were tested
    mock_head.assert_has_calls([
        mock.call('https://www.python.org/ftp/python/3.7.5/python-3.7.5-embed-win32.zip'),
        mock.call('https://www.python.org/ftp/python/3.7.6/python-3.7.6-embed-win32.zip'),
        mock.call('https://www.python.org/ftp/python/3.7.7/python-3.7.7.post1-embed-win32.zip'),
    ])

    # The second last one is the one returned.
    assert url == 'https://www.python.org/ftp/python/3.7.6/python-3.7.6-embed-win32.zip'


def test_explicit_revision_and_arch(monkeypatch):
    "A specific windows version for a given arch will be returned if requested"
    mock_head = mock.MagicMock()
    monkeypatch.setattr(requests, 'head', mock_head)

    url = windows_support_url(version='3.7', host_arch='win32', revision='4')

    # No URLs were tested
    mock_head.assert_not_called()

    # The explicit revision is returned
    assert url == 'https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-win32.zip'


def test_server_error(monkeypatch):
    "A windows version can be found with the default architecture"
    mock_head = mock.MagicMock()
    # Simulate a python.org failure
    mock_head.side_effect = mock.MagicMock(status_code=500)
    monkeypatch.setattr(requests, 'head', mock_head)

    with pytest.raises(RuntimeError):
        windows_support_url(version='3.7', host_arch=None, revision=None)

    # One URL was tested
    mock_head.assert_has_calls([
        mock.call('https://www.python.org/ftp/python/3.7.5/python-3.7.5-embed-amd64.zip'),
    ])
