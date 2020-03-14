import requests


def windows_support_url(version, host_arch, revision):
    if host_arch is None:
        host_arch = 'amd64'

    # The URL for embed packages is known:
    url = (
        'https://www.python.org/ftp/python/{version}.{micro}'
        '/python-{version}.{revision}-embed-{host_arch}.zip'
    )

    if revision:
        # A specific revision has been requested.
        parts = revision.split('.')
        best_url = url.format(
            version=version, micro=parts[0], revision=revision, host_arch=host_arch
        )
    else:
        # We can shortcut the process by priming the minor versions
        # that we already know exist.
        micro = {
            '3.5': 4,
            '3.6': 8,
            '3.7': 5,
            '3.8': 2,
        }.get(version, 0)

        # There are micro versions that are known bad.
        # Remove them from consideration.
        known_bad = {
            '3.7': {7},
        }.get(version, [])

        best_url = None
        while True:
            candidate_url = url.format(
                version=version,
                micro=micro,
                revision=micro,
                host_arch=host_arch,
            )

            # If the micro version is in the list of known bad releases,
            # remove it from consideration.
            if micro in known_bad:
                found_candidate = False
            else:
                response = requests.head(candidate_url)
                if response.status_code == 200:
                    found_candidate = True
                elif response.status_code == 404:
                    found_candidate = False
                else:
                    raise RuntimeError('Problem detecting Windows support package')

            if found_candidate:
                best_url = candidate_url
            else:
                # No base version; look for a post release.
                candidate_url = url.format(
                    version=version,
                    micro=micro,
                    revision=f'{micro}.post1',
                    host_arch=host_arch,
                )
                response = requests.head(candidate_url)

                if response.status_code == 200:
                    best_url = candidate_url
                elif response.status_code == 404:
                    # No micro version candidate, and no post release of
                    # micro version; we've hit the end of our search
                    break
                else:
                    raise RuntimeError('Problem detecting Windows support package')

            # Try the next micro version.
            micro += 1

    if best_url is None:
        raise ValueError('Unsupported major.minor version')

    return best_url


def support_url(s3, bucket, platform, version, host_arch, revision):
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
            if revision:
                if f'b{build_number}' == revision:
                    top_build = item['Key']
                    break
            else:
                if build_number > top_build_number:
                    top_build_number = build_number
                    top_build = item['Key']

    # If we didn't find at least one file, raise 404.
    if top_build is None:
        raise ValueError()

    return s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket,
            'Key': top_build
        },
        ExpiresIn=60
    )
