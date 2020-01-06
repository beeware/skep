import boto3
import pytest
from botocore.stub import Stubber

from skep.platforms import support_object


def test_single_match():
    "If a single match exists, it is returned"
    s3 = boto3.client('s3')

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

    stub_s3.add_response(
        method='get_object',
        expected_params={
            'Bucket': 'briefcase-support',
            'Key': 'python/3.X/tester/Python-3.X-tester-support.b1.tar.gz',
        },
        service_response={
            'Body': '...content...'
        }
    )

    # We've set up all the expected S3 responses, so activate the stub
    stub_s3.activate()

    # Retrieve the property, retrieving the support package URL.
    filename, obj = support_object(
        s3,
        bucket='briefcase-support',
        platform='tester',
        version='3.X',
        host_arch=None,
    )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()

    # The object that was returned is as expected.
    assert filename == 'Python-3.X-tester-support.b1.tar.gz'
    assert obj['Body'] == '...content...'


def test_single_match_with_arch():
    "If a single match exists and an arch is provided, it is returned"
    s3 = boto3.client('s3')

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

    stub_s3.add_response(
        method='get_object',
        expected_params={
            'Bucket': 'briefcase-support',
            'Key': 'python/3.X/tester/dummy/Python-3.X-tester-dummy-support.b1.tar.gz',
        },
        service_response={
            'Body': '...content...'
        }
    )

    # We've set up all the expected S3 responses, so activate the stub
    stub_s3.activate()

    # Retrieve the property, retrieving the support package URL.
    filename, obj = support_object(
        s3,
        bucket='briefcase-support',
        platform='tester',
        version='3.X',
        host_arch='dummy',
    )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()

    # The object that was returned is as expected.
    assert filename == 'Python-3.X-tester-dummy-support.b1.tar.gz'
    assert obj['Body'] == '...content...'


def test_multiple_match():
    "If a multiple matches exists, the highest revision is returned"
    s3 = boto3.client('s3')

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

    stub_s3.add_response(
        method='get_object',
        expected_params={
            'Bucket': 'briefcase-support',
            'Key': 'python/3.X/tester/Python-3.X-tester-support.b11.tar.gz',
        },
        service_response={
            'Body': '...content...'
        }
    )

    # We've set up all the expected S3 responses, so activate the stub
    stub_s3.activate()

    # Retrieve the property, retrieving the support package URL.
    filename, obj = support_object(
        s3,
        bucket='briefcase-support',
        platform='tester',
        version='3.X',
        host_arch=None,
    )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()

    # The object that was returned is as expected.
    assert filename == 'Python-3.X-tester-support.b11.tar.gz'
    assert obj['Body'] == '...content...'


def test_no_match():
    "If there is no plausible candidate support package, raise an error"
    s3 = boto3.client('s3')

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
        support_object(
            s3,
            bucket='briefcase-support',
            platform='tester',
            version='3.X',
            host_arch=None,
        )

    # Check the S3 calls have been exhausted
    stub_s3.assert_no_pending_responses()
