#!/usr/bin/python

from setuptools import find_packages, setup

setup(
    name="qool-board",
    install_requires=[
        "mitama",
        "pytz",
        "python-dateutil"
    ],
    extra_requires={"develop": ["unittest"]},
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    package_data={
        "board": [
            "templates/*.html",
            "templates/**/*.html",
            "static/*",
        ]
    }
)
