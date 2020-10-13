#!/usr/bin/env python3
#
# run.py
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

import os
import sys
import time
import shutil
import subprocess

# add `src` directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')

from cmdline import ansi
from frontend import RootRequired, Env, HealthChecker

# keep testing start time
testing_start_time = time.time()

def load_test_env():
    ''' Loads a test environment directory '''
    # make environment directory
    env_dir = '/tmp/catitestenv.' + str(time.time())
    os.mkdir(env_dir)

    Env.base_path_dir = env_dir # set environment directory
    RootRequired.is_testing = True # set is testing for root access to don't require root permission

    HealthChecker.check({}) # run health checker to create needed files in test environment

print('Starting test system...')

print('Loading test environment...', end='')
load_test_env()
print('created in ' + Env.base_path())

# load tests list
tests_list = os.listdir('tests/items')

# clean up tests list
orig_tests = []
for test in tests_list:
    if test[len(test)-3:] == '.py':
        exec('from items.' + test[:len(test)-3] + ' import ' + test[:len(test)-3])
        exec("orig_tests.append(" + test[:len(test)-3] + "())")

# start running tests
count = 0
for test in orig_tests:
    test_name = test.get_name()
    print('\t' + test_name.replace('_', ' ') + ': ', end='', flush=True)
    test.run()
    print('\033[32mPASS\033[0m')
    count += 1

print('\033[32mAll ' + str(count) + ' tests passed successfuly\033[0m')

print('Cleaning up...')
shutil.rmtree(Env.base_path_dir)
