import requests


def windows_support_url(version, host_arch):
    if host_arch is None:
        host_arch = 'amd64'

    # We can shortcut the process by priming the minor versions
    # that we already know exist.
    try:
        micro = {
            '3.5': 4,
            '3.6': 8,
            '3.7': 5,
            '3.8': 0,
        }[version]
    except KeyError:
        raise ValueError('Unsupported major.minor version')

    # The URL for embed packages is known:
    url = (
        'https://www.python.org/ftp/python/{version}.{micro}'
        '/python-{version}.{micro}-embed-{host_arch}.zip'
    )

    while True:
        response = requests.head(
            url.format(version=version, micro=micro, host_arch=host_arch)
        )

        if response.status_code == 404:
            # Micro version doesn't exist; highest released version
            # is therefore the previous micro version.
            micro = micro - 1
            break
        elif response.status_code != 200:
            raise RuntimeError('Problem detecting Windows support package')

        micro += 1

    return url.format(version=version, micro=micro, host_arch=host_arch)


def support_object(s3, bucket, platform, version, host_arch):
    if host_arch is None:
        prefix = f'python/{version}/{platform}/'
    else:
        prefix = f'python/{version}/{platform}/{host_arch}/'

    # List all the objects in the bucket.
    # Look for the highest build number.
    top_build_number = 0
    top_build = None
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get('Contents', []):
            build_number = int(
                item['Key'].split('.')[-3].lstrip('b')
            )
            if build_number > top_build_number:
                top_build_number = build_number
                top_build = item['Key']

    # If we didn't find at least one file, raise 404.
    if top_build is None:
        raise ValueError()

    # Get the object that is the most recent build
    s3_object = s3.get_object(Bucket=bucket, Key=top_build)
    filename = top_build.rsplit('/')[-1]

    return filename, s3_object
