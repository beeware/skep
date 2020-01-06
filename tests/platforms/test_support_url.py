from urllib.parse import urlparse, parse_qsl

import boto3
import pytest
from botocore.stub import Stubber

from skep.platforms import support_url

@pytest.fixture
def s3():
    session = boto3.Session(profile_name='test')
    return session.client('s3')


def test_single_match(s3):
    "If a single match exists, it is returned"
    stub_s3 = Stubber(s3)

    # Add the expected request/responses from S3
    stub_s3.add_response(
        method='list_objects_v2',
        expected_params={
            'Bucket': 'briefcase-support',
            'Prefix': 'python/3.X/tester/'
        },
        service_response={
            'Contents': [
                {'Key': 'python/3.X/tester/Python-3.X-tester-support.b1.tar.gz'}
            ],
            'KeyCount': 1,
        }
    )

    # We've set up all the expected S3 responses, so activate the stub
    stub_s3.activate()

    # Retrieve the property, retrieving the support package URL.
    url = support_url(
        s3,
        bucket='briefcase-support',
        platform='tester',
        version='3.X',
        host_arch=None,
    )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()

    # The URL that was returned is as expected.
    parsed_url = urlparse(url)
    assert parsed_url.scheme == 'https'
    assert parsed_url.netloc == 'briefcase-support.s3.amazonaws.com'
    assert parsed_url.path == '/python/3.X/tester/Python-3.X-tester-support.b1.tar.gz'
    query = dict(parse_qsl(parsed_url.query))
    assert 'Expires' in query
    assert 'AWSAccessKeyId' in query
    assert 'Signature' in query


def test_single_match_with_arch(s3):
    "If a single match exists and an arch is provided, it is returned"
    stub_s3 = Stubber(s3)

    # Add the expected request/responses from S3
    stub_s3.add_response(
        method='list_objects_v2',
        expected_params={
            'Bucket': 'briefcase-support',
            'Prefix': 'python/3.X/tester/dummy/'
        },
        service_response={
            'Contents': [
                {'Key': 'python/3.X/tester/dummy/Python-3.X-tester-dummy-support.b1.tar.gz'}
            ],
            'KeyCount': 1,
        }
    )

    # We've set up all the expected S3 responses, so activate the stub
    stub_s3.activate()

    # Retrieve the property, retrieving the support package URL.
    url = support_url(
        s3,
        bucket='briefcase-support',
        platform='tester',
        version='3.X',
        host_arch='dummy',
    )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()

    # The URL that was returned is as expected.
    parsed_url = urlparse(url)
    assert parsed_url.scheme == 'https'
    assert parsed_url.netloc == 'briefcase-support.s3.amazonaws.com'
    assert parsed_url.path == '/python/3.X/tester/dummy/Python-3.X-tester-dummy-support.b1.tar.gz'
    query = dict(parse_qsl(parsed_url.query))
    assert 'Expires' in query
    assert 'AWSAccessKeyId' in query
    assert 'Signature' in query


def test_multiple_match(s3):
    "If a multiple matches exists, the highest revision is returned"
    stub_s3 = Stubber(s3)

    # Add the expected request/responses from S3
    stub_s3.add_response(
        method='list_objects_v2',
        expected_params={
            'Bucket': 'briefcase-support',
            'Prefix': 'python/3.X/tester/'
        },
        service_response={
            'Contents': [
                {'Key': 'python/3.X/tester/Python-3.X-tester-support.b11.tar.gz'},
                {'Key': 'python/3.X/tester/Python-3.X-tester-support.b8.tar.gz'},
                {'Key': 'python/3.X/tester/Python-3.X-tester-support.b9.tar.gz'},
                {'Key': 'python/3.X/tester/Python-3.X-tester-support.b10.tar.gz'},
            ],
            'KeyCount': 4,
        }
    )

    # We've set up all the expected S3 responses, so activate the stub
    stub_s3.activate()

    # Retrieve the property, retrieving the support package URL.
    url = support_url(
        s3,
        bucket='briefcase-support',
        platform='tester',
        version='3.X',
        host_arch=None,
    )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()

    # The URL that was returned is as expected.
    parsed_url = urlparse(url)
    assert parsed_url.scheme == 'https'
    assert parsed_url.netloc == 'briefcase-support.s3.amazonaws.com'
    assert parsed_url.path == '/python/3.X/tester/Python-3.X-tester-support.b11.tar.gz'
    query = dict(parse_qsl(parsed_url.query))
    assert 'Expires' in query
    assert 'AWSAccessKeyId' in query
    assert 'Signature' in query


def test_no_match(s3):
    "If there is no plausible candidate support package, raise an error"
    stub_s3 = Stubber(s3)

    # Add the expected request/responses from S3
    stub_s3.add_response(
        method='list_objects_v2',
        expected_params={
            'Bucket': 'briefcase-support',
            'Prefix': 'python/3.X/tester/'
        },
        service_response={
            'KeyCount': 0,
        }
    )

    # We've set up all the expected S3 responses, so activate the stub
    stub_s3.activate()

    # Retrieve the property, retrieving the support package URL.
    with pytest.raises(ValueError):
        support_url(
            s3,
            bucket='briefcase-support',
            platform='tester',
            version='3.X',
            host_arch=None,
        )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()
