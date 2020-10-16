#
# HealthChecker.py
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

''' Checks cati installation health and repair '''

import os
from frontend import Env

def repair_once_file(filepath: str, events: dict):
    ''' Repairs once file '''
    try:
        f = open(Env.base_path('/' + filepath), 'w')
        f.write('')
        f.close()
    except:
        events['failed_to_repair']('/' + filepath, 'file')

def repair_once_dir(dirpath: str, events: dict):
    ''' Repairs once dir '''
    try:
        os.mkdir(Env.base_path('/' + dirpath))
    except:
        events['failed_to_repair']('/' + dirpath, 'dir')

def check(events: dict):
    '''
    Check all of needed files and dirs for cati installation

    events:
    - failed_to_repair: will run when cati installation is corrupt and user has not root permission
    to repair it and passes filepath and type of that to function
    '''

    required_files = [
    ]

    required_dirs = [
        '/var',
        '/var/lib',
        '/var/lib/cati',
        '/var/lib/cati/lists',
        '/var/lib/cati/installed',
    ]

    for f in required_files:
        if not os.path.isfile(Env.base_path('/' + f)):
            repair_once_file(f)

    for d in required_dirs:
        if not os.path.isdir(Env.base_path('/' + d)):
            repair_once_dir(d, events)