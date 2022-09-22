

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
        # Lock the most recent known versions as of the pre-release of Briefcase 0.3.10
        try:
            micro = {
                '3.5': 4,
                '3.6': 8,
                '3.7': 9,
                '3.8': 10,
                '3.9': 13,
                '3.10': 7,
            }[version]

            best_url = url.format(
                version=version,
                micro=micro,
                revision=micro,
                host_arch=host_arch,
            )
        except KeyError:
            raise ValueError('Unsupported major.minor version')

    return best_url


def support_url(s3, bucket, platform, version, host_arch, revision):
    try:
        if host_arch is None:
            prefix = f'python/{version}/{platform}'

            if platform == "android":
                best_revision = {
                    '3.6': 3,
                    '3.7': 9,
                    '3.8': 5,
                    '3.9': 3,
                    '3.10': 2,
                }[version]
                if revision is None:
                    revision = best_revision

                top_build = f"{prefix}/Python-{version}-Android-support.b{revision}.zip"
            elif platform in {"iOS", "macOS"}:
                best_revision = {
                    '3.5': 12,
                    '3.6': 14,
                    '3.7': 9,
                    '3.8': 9,
                    '3.9': 7,
                    '3.10': 3,
                }[version]
                if revision is None:
                    revision = best_revision

                top_build = f"{prefix}/Python-{version}-{platform}-support.b{revision}.tar.gz"
            else:
                top_build = None
        elif platform == "linux" and host_arch == "x86_64":
            prefix = f'python/{version}/{platform}/{host_arch}'

            best_revision = {
                '3.5': 2,
                '3.6': 4,
                '3.7': 6,
                '3.8': 6,
                '3.9': 4,
                '3.10': 3,
            }[version]
            if revision is None:
                revision = best_revision

            top_build = f"{prefix}/Python-{version}-linux-{host_arch}-support.b{revision}.tar.gz"
        else:
            top_build = None
    except KeyError:
        top_build = None

    # If we didn't find a file, raise 404.
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
