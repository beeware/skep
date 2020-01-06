import os

import boto3
from flask import Flask, abort, redirect, request

from skep import platforms


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        S3_BUCKET='briefcase-support',
        S3_REGION='us-west-2',
        STREAMING_CHUNK_SIZE=1024,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Views
    @app.route('/')
    def hello():
        return """
<html>
<head>
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Cutive">
    <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Roboto">
    <style>
        img {
            float: left;
        }
        h1 {
            font-family: 'Cutive', serif;
            padding-top: 2em;
        }
        p {
            font-family: 'Roboto', sans-serif;
        }
    </style>
</head>
<body>
    <img src="https://beeware.org/project/projects/tools/briefcase/briefcase.png" alt="Briefcase logo">
    <h1>Briefcase Support Repository</h1>
    <p>
        This is the support repository for
        <a href="https://briefcase.readthedocs.io">Briefcase</a>,
        the <a href="https://beeware.org/">BeeWare Project's</a> Python
        application packaging tool.
    </p>
    <p>
        For more details, see the <a href="https://briefcase.readthedocs.io">Briefcase
        documentation</a>. You may want to start with the
        <a href="https://briefcase.readthedocs.io">tutorial</a>.
    </p>
</body>
"""

    @app.route("/python", methods=['GET'])
    def support_package():
        # Extract arguments from the URL.
        py_version = request.args.get('version')
        platform = request.args.get('platform')
        host_arch = request.args.get('arch')

        if py_version is None:
            abort(400, "No Python version requested")
        if platform is None:
            abort(400, "No platform requested")

        try:
            if platform == 'windows':
                url = platforms.windows_support_url(
                    version=py_version,
                    host_arch=host_arch
                )
            else:
                url = platforms.support_url(
                    boto3.client('s3', region_name=app.config['S3_REGION']),
                    bucket=app.config['S3_BUCKET'],
                    platform=platform,
                    version=py_version,
                    host_arch=host_arch,
                )

            return redirect(url, code=302)
        except ValueError:
            abort(404)
        except RuntimeError:
            abort(502)

    return app
