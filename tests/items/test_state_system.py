#
# test_state_system.py
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

""" Test test_state_system """

from TestCore import TestCore
from frontend import Env

class test_state_system(TestCore):
    """ Test test_state_system """
    def run(self):
        """ Run test """
        self.refresh_env()

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkgc-2.0.cati'
        ]), 0)

        state_f = open(Env.state_file(), 'w')
        state_f.write(f'install%testpackage1%1.0%amd64\nremove%anotherpackage')
        state_f.close()

        self.assert_equals(self.run_command('remove', [
            'testpkgc',
            '-y',
        ]), 1)

        self.assert_equals(self.run_command('pkg', [
            'install',
            'tests/test-packages/packages/testpkgc-2.0.cati'
        ]), 1)

        self.refresh_env()