from unittest import mock

import boto3

from skep import platforms


def test_no_version(test_client):
    "If a version is not provided, a 400 is returned"
    response = test_client.get('/python')
    assert response.status_code == 400
    assert b'No Python version requested' in response.data


def test_no_platform(test_client):
    "If a platform is not provided, a 400 is returned"
    response = test_client.get('/python?version=3.7')
    assert response.status_code == 400
    assert b'No platform requested' in response.data


def test_window_missing(test_client, monkeypatch):
    "If no windows support package can be found, a 404 is raised"
    mock_windows_support_url = mock.MagicMock()
    mock_windows_support_url.side_effect = ValueError
    monkeypatch.setattr(platforms, 'windows_support_url', mock_windows_support_url)

    response = test_client.get('/python?version=3.7&platform=windows')

    mock_windows_support_url.assert_called_with(
        version='3.7',
        host_arch=None
    )

    assert response.status_code == 404


def test_windows_exists(test_client, monkeypatch):
    "If a windows support package can be found, a redirect is returned"
    mock_windows_support_url = mock.MagicMock()
    mock_windows_support_url.return_value = 'https://example.com/object.zip'
    monkeypatch.setattr(platforms, 'windows_support_url', mock_windows_support_url)

    response = test_client.get('/python?version=3.7&platform=windows')

    mock_windows_support_url.assert_called_with(
        version='3.7',
        host_arch=None
    )

    assert response.status_code == 302
    assert response.location == 'https://example.com/object.zip'


def test_windows_with_arch_exists(test_client, monkeypatch):
    "If a windows support package can be found for a specific architecture, a redirect is returned"
    mock_windows_support_url = mock.MagicMock()
    mock_windows_support_url.return_value = 'https://example.com/object.zip'
    monkeypatch.setattr(platforms, 'windows_support_url', mock_windows_support_url)

    response = test_client.get('/python?version=3.7&platform=windows&arch=win32')

    mock_windows_support_url.assert_called_with(
        version='3.7',
        host_arch='win32',
    )

    assert response.status_code == 302
    assert response.location == 'https://example.com/object.zip'


def test_windows_python_org_failure(test_client, monkeypatch):
    "If a windows support package can be found for a specific architecture, a redirect is returned"
    mock_windows_support_url = mock.MagicMock()
    mock_windows_support_url.side_effect = RuntimeError
    monkeypatch.setattr(platforms, 'windows_support_url', mock_windows_support_url)

    response = test_client.get('/python?version=3.7&platform=windows&arch=win32')

    mock_windows_support_url.assert_called_with(
        version='3.7',
        host_arch='win32',
    )

    assert response.status_code == 502


def test_support_missing(test_client, monkeypatch):
    "If no support package can be found, a 404 is raised"
    mock_support_object = mock.MagicMock()
    mock_support_object.side_effecet = ValueError

    mock_s3_client = mock.MagicMock()
    mock_s3 = mock.MagicMock()
    mock_s3_client.return_value = mock_s3

    monkeypatch.setattr(platforms, 'support_object', mock_support_object)
    monkeypatch.setattr(boto3, 'client', mock_s3_client)

    response = test_client.get('/python?version=3.7&platform=linux')

    mock_support_object.assert_called_with(
        mock_s3,
        bucket='briefcase-support',
        version='3.7',
        platform='linux',
        host_arch=None,
    )

    assert response.status_code == 404


def test_support_exists(test_client, monkeypatch):
    "If a support package can be found, it is returned"
    mock_support_object = mock.MagicMock()
    mock_obj = mock.MagicMock()
    mock_support_object.return_value = 'support_file.tar.gz', mock_obj

    mock_s3_client = mock.MagicMock()
    mock_s3 = mock.MagicMock()
    mock_s3_client.return_value = mock_s3

    monkeypatch.setattr(platforms, 'support_object', mock_support_object)
    monkeypatch.setattr(boto3, 'client', mock_s3_client)

    response = test_client.get('/python?version=3.7&platform=linux')

    mock_support_object.assert_called_with(
        mock_s3,
        bucket='briefcase-support',
        version='3.7',
        platform='linux',
        host_arch=None,
    )

    assert response.status_code == 200
    assert response.mimetype == 'application/tar+gzip'
    assert response.headers['Content-Disposition'] == 'attachment;filename=support_file.tar.gz'


def test_support_with_arch_exists(test_client, monkeypatch):
    "If a support package for an architecture can be found, it is returned"
    mock_support_object = mock.MagicMock()
    mock_obj = mock.MagicMock()
    mock_support_object.return_value = 'support_file.tar.gz', mock_obj

    mock_s3_client = mock.MagicMock()
    mock_s3 = mock.MagicMock()
    mock_s3_client.return_value = mock_s3

    monkeypatch.setattr(platforms, 'support_object', mock_support_object)
    monkeypatch.setattr(boto3, 'client', mock_s3_client)

    response = test_client.get('/python?version=3.7&platform=linux&arch=amd64')

    mock_support_object.assert_called_with(
        mock_s3,
        bucket='briefcase-support',
        version='3.7',
        platform='linux',
        host_arch='amd64',
    )

    assert response.status_code == 200
    assert response.mimetype == 'application/tar+gzip'
    assert response.headers['Content-Disposition'] == 'attachment;filename=support_file.tar.gz'
