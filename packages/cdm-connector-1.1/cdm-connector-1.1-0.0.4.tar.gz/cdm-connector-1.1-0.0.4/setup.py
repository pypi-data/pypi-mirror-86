﻿# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.

import os
from os.path import isfile, join
from os import listdir
from shutil import copytree, ignore_patterns, rmtree
import distutils.cmd
import distutils.log
import setuptools

from typing import List, Optional


class CopyResourcesCommand(distutils.cmd.Command):
    """A command which is copying the resources from SchemaDocuments."""

    description = 'Copy resources from schema documents into this project.'  # type: Optional[str]

    user_options = []  # type: List

    def copy_and_overwrite(self, from_path, to_path, paths_to_ignore):
        """Copies the folder from path and overwrites the to path folder."""
        if os.path.exists(to_path):
            rmtree(to_path)
        copytree(from_path, to_path, ignore=ignore_patterns(*paths_to_ignore))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Copying files from schema documents....")
        root_path = os.getcwd()

        paths_to_ignore = ['*.manifest.cdm.json', '*.0.6.cdm.json', '*.0.7.cdm.json', '*.0.8.cdm.json', '*.0.8.1.cdm.json',
                           '*.0.9.cdm.json', '*.1.0.cdm.json', '*core*', '*office*', '*.git*', '*.jpg', '*.md']

        self.copy_and_overwrite('{}/../schemaDocuments/'.format(root_path), '{}/resources/'.format(root_path), paths_to_ignore)


def list_files_in_folder(folders):
    """Finds all files in a folder, used by data files in setuptools as it has to be in this format."""
    path = '/'.join(folders)
    if os.path.exists(path):
        return [join(*folders, f) for f in listdir(path) if isfile(join(*folders, f))]


with open("README.md", "r") as fh:
    long_description = fh.read()

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

def requirements():
    with open('requirements.txt') as req_file:
        reqs = req_file.read().splitlines()
    return reqs



setuptools.setup(
    name="cdm-connector-1.1",
    version="0.0.4",
    author="SkyPoint Cloud",
    author_email="support@skypointcloud.com",
    description="Common Data Model Object Model library for Python. Customized for SkyPoint use cases.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/skypointcloud/skypoint-python-cdm1.1-connector",
    packages=setuptools.find_packages(),
    license="GPL-3.0",
    data_files=[
        ('resources', list_files_in_folder(['resources'])),
        ('resources/extensions', list_files_in_folder(['resources', 'extensions'])),
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=requirements()
)
