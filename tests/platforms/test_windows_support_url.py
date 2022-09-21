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

    url = windows_support_url(version='3.7', host_arch=None, revision=None)

    assert url == 'https://www.python.org/ftp/python/3.7.9/python-3.7.9-embed-amd64.zip'


def test_explicit_revision_default_arch(monkeypatch):
    "A specific windows version will be returned if requested"

    url = windows_support_url(version='3.7', host_arch=None, revision='4')

    # The explicit revision is returned
    assert url == 'https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-amd64.zip'


def test_explicit_post_revision(monkeypatch):
    "A specific windows post-release version will be returned if requested"
    mock_head = mock.MagicMock()
    monkeypatch.setattr(requests, 'head', mock_head)

    url = windows_support_url(version='3.7', host_arch=None, revision='4.post1')

    # The explicit revision is returned
    assert url == 'https://www.python.org/ftp/python/3.7.4/python-3.7.4.post1-embed-amd64.zip'


def test_find_version_explicit_arch(monkeypatch):
    "A windows version can be found with an explicit architecture"

    url = windows_support_url(version='3.7', host_arch='win32', revision=None)

    assert url == 'https://www.python.org/ftp/python/3.7.9/python-3.7.9-embed-win32.zip'


def test_explicit_revision_and_arch(monkeypatch):
    "A specific windows version for a given arch will be returned if requested"

    url = windows_support_url(version='3.7', host_arch='win32', revision='4')

    # The explicit revision is returned
    assert url == 'https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-win32.zip'
