#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re
import pathlib

from setuptools import setup, find_packages

def _read(*parts, **kwargs):
    filepath = os.path.join(os.path.dirname(__file__), *parts)
    encoding = kwargs.pop('encoding', 'utf-8')
    with io.open(filepath, encoding = encoding) as fh:
        text = fh.read()
    return text



def get_long_description():
    return _read('README.md')


def get_requirements(path):
    content = _read(path)
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
    ]
install_requires = get_requirements('requirements.txt')

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name = 'stripenn',
    version = '1.0.27',
    author = 'Sora Yoon',
    author_email = 'sora.yoon@pennmedicine.upenn.edu',
    description = "Image-processing based detection of architectural stripes from chromatic conformation data",
    long_description=README,
    long_description_content_type="text/markdown",
    url = 'https://github.com/ysora/stripenn',
    #package_dir={'': 'src'},
    #packages=['stripenn'],
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    entry_points={
    	"console_scripts": ["stripenn = stripenn.stripenn:main"]
    },
)
