import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "p6-barrier",
    "version": "0.0.26",
    "description": "p6-barrier",
    "license": "Apache-2.0",
    "url": "https://github.com/p6m7g8/p6-barrier.git",
    "long_description_content_type": "text/markdown",
    "author": "Philip M. Gollucci<pgollucci@p6m7g8.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/p6m7g8/p6-barrier.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "p6_barrier",
        "p6_barrier._jsii"
    ],
    "package_data": {
        "p6_barrier._jsii": [
            "p6-barrier@0.0.26.jsii.tgz"
        ],
        "p6_barrier": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.74.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.74.0, <2.0.0",
        "aws-cdk.aws-ssm>=1.74.0, <2.0.0",
        "aws-cdk.core>=1.74.0, <2.0.0",
        "aws-cdk.custom-resources>=1.74.0, <2.0.0",
        "constructs>=3.2.0, <4.0.0",
        "jsii>=1.14.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
