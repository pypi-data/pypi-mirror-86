# -*- coding: utf-8 -*-
import glob
from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

with open('README.md') as f:
    readme = f.read()

requirements = [
    "pymongo",
    "logbook",
    "flask",
    "click",
    "prettytable",
    "tensorflow==1.13.1",
    "imageio==2.9.0",
    "numpy==1.16.2",
    "Pillow==7.2.0",
    "flask-socketio",
    "python-socketio",
    "Pillow",
    "click"
]
setup(
    version="1.0.2",
    name="PixelInstagram",
    description="a simple app",
    # long_description=readme,
    keywords="PixelInstagram",
    include_package_data=True,
    packages=find_packages(include=["PixelInstagram", "PixelInstagram.*"]),
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "PI = PixelInstagram.main:cli",
        ]
    },
    # long_description_content_type='text/markdown',
    author="wjh1119",
    author_email="20091755G@connect.polyu.hk",
    url='https://gitee.com/wjh1119'
)
