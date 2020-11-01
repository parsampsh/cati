#
# ArchiveModel.py
#
# the cati project
# Copyright 2020 parsa mpsh <parsampsh@gmail.com>
#
# This file is part of cati.
#
# cati is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cati is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cati.  If not, see <https://www.gnu.org/licenses/>.
##################################################

""" .cati package file model """

import tarfile
import json
from dotcati.PackageJsonValidator import PackageJsonValidator
from package.Pkg import Pkg

class archive_factory:
    """
    Archive model factory.

    the strcuture of packages, maybe change in new version of cati.
    so, cati should be compatible with old packages where
    created with old version of cati. this class
    is a factory to check package version and
    return archive model object by that
    version.
    """
    def __new__(self, file_path: str, type_str: str):
        # open v1 as default
        pkg = ArchiveModelV1(file_path, type_str)
        if pkg.pkg_version() == '1.0':
            return ArchiveModelV1(file_path, type_str)
        # return v1 object by default
        return ArchiveModelV1(file_path, type_str)

class BaseArchive(Pkg):
    """ base archive for archive versions """
    def __init__(self, file_path: str, type_str: str):
        self.tar = tarfile.open(file_path, type_str)

    def add(self, path, arcname=None):
        """ Add a file to package archive """
        return self.tar.add(path, arcname=arcname)

    def close(self):
        """ Close package archive """
        return self.tar.close()

    def extractall(self, path):
        """ Extract all of package files to `path` """
        return self.tar.extractall(path)

    def pkg_version(self) -> str:
        """ Returns dotcati package strcuture version """
        for member in self.tar.getmembers():
            if member.path == 'cati-version':
                # load dotcati package version
                f = self.tar.extractfile(member)
                return f.read().strip()
        # default version
        return '1.0'

    def members(self):
        """ Returns members of the archive """
        files = []
        for member in self.tar.getmembers():
            if member.path != '':
                files.append(member.path)
        return files

    def read(self):
        """ Load package information on object """
        self.data = self.info()
        if not PackageJsonValidator.validate(self.data):
            raise
        # try to compare version for version validation
        Pkg.compare_version(self.data['version'], '0.0.0')

    def info(self) -> dict:
        """ Returns package data.json information """
        for member in self.tar.getmembers():
            if member.path == 'data.json':
                f = self.tar.extractfile(member)
                return json.loads(f.read())

class ArchiveModelV1(BaseArchive):
    """ .cati package file model (v1.0) """
    pass
