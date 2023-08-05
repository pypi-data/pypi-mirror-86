import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-bar",
    "version": "0.1.0",
    "description": "cdk-bar",
    "license": "Apache-2.0",
    "url": "https://github.com/pahudnet/cdk-bar.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud<pahudnet@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pahudnet/cdk-bar.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_bar",
        "cdk_bar._jsii"
    ],
    "package_data": {
        "cdk_bar._jsii": [
            "cdk-bar@0.1.0.jsii.tgz"
        ],
        "cdk_bar": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.73.0, <2.0.0",
        "aws-cdk.aws-ecs-patterns>=1.73.0, <2.0.0",
        "aws-cdk.aws-ecs>=1.73.0, <2.0.0",
        "aws-cdk.core>=1.73.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
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
