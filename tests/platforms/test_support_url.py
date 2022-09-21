from urllib.parse import urlparse, parse_qsl

import boto3
import pytest

from skep.platforms import support_url


@pytest.fixture
def s3():
    session = boto3.Session()
    return session.client('s3')


@pytest.mark.parametrize(
    "platform, version, host_arch, revision, expected_path",
    [
        ("linux", "3.8", "x86_64", None, "/python/3.8/linux/x86_64/Python-3.8-linux-x86_64-support.b6.tar.gz"),
        ("linux", "3.10", "x86_64", None, "/python/3.10/linux/x86_64/Python-3.10-linux-x86_64-support.b3.tar.gz"),
        ("linux", "3.8", "x86_64", "2", "/python/3.8/linux/x86_64/Python-3.8-linux-x86_64-support.b2.tar.gz"),

        ("android", "3.8", None, None, "/python/3.8/android/Python-3.8-Android-support.b5.zip"),
        ("android", "3.10", None, None, "/python/3.10/android/Python-3.10-Android-support.b2.zip"),
        ("android", "3.8", None, "2", "/python/3.8/android/Python-3.8-Android-support.b2.zip"),

        ("iOS", "3.8", None, None, "/python/3.8/iOS/Python-3.8-iOS-support.b9.tar.gz"),
        ("iOS", "3.10", None, None, "/python/3.10/iOS/Python-3.10-iOS-support.b3.tar.gz"),
        ("iOS", "3.8", None, "2", "/python/3.8/iOS/Python-3.8-iOS-support.b2.tar.gz"),

        ("macOS", "3.8", None, None, "/python/3.8/macOS/Python-3.8-macOS-support.b9.tar.gz"),
        ("macOS", "3.10", None, None, "/python/3.10/macOS/Python-3.10-macOS-support.b3.tar.gz"),
        ("macOS", "3.8", None, "2", "/python/3.8/macOS/Python-3.8-macOS-support.b2.tar.gz"),
    ]
)
def test_valid_support_url(s3, platform, version, host_arch, revision, expected_path):
    "The support URLs in place at the time of the release of Briefcase v0.3.10 can be returned"
    # Retrieve the property, retrieving the support package URL.
    url = support_url(
        s3,
        bucket='briefcase-support',
        platform=platform,
        version=version,
        host_arch=host_arch,
        revision=revision,
    )

    # The URL that was returned is as expected.
    parsed_url = urlparse(url)
    assert parsed_url.scheme == 'https'
    assert parsed_url.netloc == 'briefcase-support.s3.amazonaws.com'
    assert parsed_url.path == expected_path
    query = dict(parse_qsl(parsed_url.query))
    assert 'Expires' in query
    assert 'AWSAccessKeyId' in query
    assert 'Signature' in query


@pytest.mark.parametrize(
    "platform, version, host_arch, revision",
    [
        # Unknown platform
        ("something", "3.8", "x86_64", "2"),
        ("something", "3.8", "x86_64", None),
        ("something", "3.8", None, "2"),
        ("something", "3.8", None, None),

        # Linux without a host architecture
        ("linux", "3.8", None, "2"),
        ("linux", "3.8", None, None),

        # Linux with a non-x86_64 host architecture
        ("linux", "3.8", "arm64", "2"),
        ("linux", "3.8", "arm64", None),

        # Non-linux with host architecture
        ("android", "3.8", "x86_64", "2"),
        ("android", "3.8", "x86_64", None),

        ("iOS", "3.8", "x86_64", "2"),
        ("iOS", "3.8", "x86_64", None),

        ("macOS", "3.8", "x86_64", "2"),
        ("macOS", "3.8", "x86_64", None),

        # Unsupported Python versions
        ("linux", "2.7", "x86_64", None),
        ("linux", "2.7", "x86_64", "2"),
        ("linux", "3.4", "x86_64", None),
        ("linux", "3.4", "x86_64", "2"),
        ("linux", "3.11", "x86_64", None),
        ("linux", "3.11", "x86_64", "2"),

        ("android", "2.7", None, None),
        ("android", "2.7", None, "2"),
        ("android", "3.5", None, None),
        ("android", "3.5", None, "2"),
        ("android", "3.11", None, None),
        ("android", "3.11", None, "2"),

        ("iOS", "2.7", None, None),
        ("iOS", "2.7", None, "2"),
        ("iOS", "3.4", None, None),
        ("iOS", "3.4", None, "2"),
        ("iOS", "3.11", None, None),
        ("iOS", "3.11", None, "2"),

        ("macOS", "2.7", None, None),
        ("macOS", "2.7", None, "2"),
        ("macOS", "3.4", None, None),
        ("macOS", "3.4", None, "2"),
        ("macOS", "3.11", None, None),
        ("macOS", "3.11", None, "2"),

    ]
)
def test_invalid_support_url(s3, platform, version, host_arch, revision):
    "Bad support URL requests are rejected."
    # Retrieve the property, retrieving the support package URL.
    with pytest.raises(ValueError):
        support_url(
            s3,
            bucket='briefcase-support',
            platform=platform,
            version=version,
            host_arch=host_arch,
            revision=revision,
        )
