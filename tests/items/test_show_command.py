#
# test_show_command.py
#
# the cati project
# Copyright 2020-2021 parsa shahmaleki <parsampsh@gmail.com>
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

""" Test test_show_command """

from TestCore import TestCore

class test_show_command(TestCore):
    """ Test test_show_command """
    def run(self):
        """ Run test """
        self.assert_equals(self.run_command('show', ['gfdgfhghgfh']), 1)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkgc-2.0.cati'
        ]), 0)

        self.assert_equals(self.run_command('show', ['testpkgc']), 0)
        self.assert_equals(self.run_command('show', ['testpkgc', 'gfgfhfg']), 0)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'repository/test-repository/testpkg11.cati'
        ]), 0)

        self.assert_equals(self.run_command('show', ['testpkg11']), 0)
        self.assert_equals(self.run_command('show', ['testpkgc', 'testpkg11']), 0)
        self.assert_equals(self.run_command('show', ['testpkgc', 'fgfhghfhhgj', 'testpkg11']), 0)

        self.assert_equals(self.run_command('show', ['testpkgc=2.0']), 0)
        self.assert_equals(self.run_command('show', ['testpkgc=1.0']), 1)
