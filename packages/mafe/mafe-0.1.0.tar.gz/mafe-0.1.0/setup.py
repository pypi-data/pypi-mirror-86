from setuptools import setup
from setuptools.command.sdist import sdist as _sdist
import shutil
from os import path
import io

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class sdist(_sdist):
    def run(self):
        _sdist.run(self)


setup(
    name='mafe',
    description='Music Audio Feature Extractor: generate trainable data set from music files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0',
    author='Lene Preuss',
    packages=['mafe'],
    # SPDX-License-Identifier: MIT
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License'
    ],
    project_urls={
        'Source': 'https://gitlab.com/lilacashes/mafe.git'
    },
    test_suite="test",
    cmdclass={'sdist': sdist}
)
