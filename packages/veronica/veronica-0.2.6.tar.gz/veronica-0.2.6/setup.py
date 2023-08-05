#!/usr/bin/env python

from setuptools import setup, find_packages  # type: ignore


setup(
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    description="",
    entry_points={"console_scripts": ["veronica=veronica.cli:main",],},
    install_requires=[],
    license="MIT license",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # package_data={"veronica": ["py.typed"]},
    # include_package_data=True,
    keywords="veronica",
    name="veronica",
    # package_dir={"": "src"},
    packages=find_packages(include=["src/veronica", "src/veronica.*"]),
    setup_requires=[],
    url="https://github.com/nirmalhk7/veronica",
    version="0.2.6",
    zip_safe=False,
)
