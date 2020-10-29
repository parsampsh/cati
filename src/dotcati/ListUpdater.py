#
# ListUpdater.py
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

""" Packages list updater """

import os, json
from frontend.RootRequired import require_root_permission
from frontend import Env

def update_indexes(events: dict):
    """
    This function loads available versions of a package and index them in index file
    and do this action for all of packages in lists

    the `events` argument should be a dictonary from functions. this will use to handle errors
    for example if some thing went wrong, the spesific function in events
    will run

    events:
    - cannot_read_file: if in this process, an error happened while reading a file, this will run with file path arg
    - invalid_json_data: if json content of a file is curropt, this will run with file path and content args
    """

    require_root_permission()

    for pkg in os.listdir(Env.packages_lists()):
        pkg_index = {}
        if os.path.isdir(Env.packages_lists('/' + pkg)):
            for version in os.listdir(Env.packages_lists('/' + pkg)):
                if version != 'index':
                    if os.path.isfile(Env.packages_lists('/' + pkg + '/' + version)):
                        content = None
                        try:
                            f = open(Env.packages_lists('/' + pkg + '/' + version), 'r')
                            content = f.read()
                        except:
                            events['cannot_read_file'](Env.packages_lists('/' + pkg + '/' + version))

                        if content != None:
                            try:
                                content_json = json.loads(content)
                                try:
                                    tmp = pkg_index[content_json['arch']]
                                    del tmp
                                except:
                                    pkg_index[content_json['arch']] = []
                                pkg_index[content_json['arch']].append(content_json['version'])
                            except:
                                events['invalid_json_data'](Env.packages_lists('/' + pkg + '/' + version), content)
        # write generated index to index file
        f_index = open(Env.packages_lists('/' + pkg + '/index'), 'w')
        f_index.write(json.dumps(pkg_index))
        f_index.close()
