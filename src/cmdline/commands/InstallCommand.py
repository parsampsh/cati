#
# InstallCommand.py
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

""" Install command """

from cmdline.BaseCommand import BaseCommand
from package.Pkg import Pkg
from frontend import RootRequired, Env
from cmdline import pr, ansi, ArgParser
from transaction.Calculator import Calculator
from cmdline.components import TransactionShower
from cmdline.commands.DownloadCommand import DownloadCommand
from cmdline.commands.RemoveCommand import RemoveCommand
from cmdline.commands.PkgCommand import PkgCommand

class InstallCommand(BaseCommand):
    """ Install command """
    def help(self):
        """
        install packages

        Usage: cati install [options] pkg1 pkg2 pkg3 ...
        ...... cati install [options] pkg1 pkg2=<version> ...

        Options:
        -y|--yes: don't ask for user confirmation
        """
        pass

    def config(self) -> dict:
        """ Define and config this command """
        return {
            'name': 'install',
            'options': {
                '-y': [False, False],
                '--yes': [False, False],
            },
            'max_args_count': None,
            'min_args_count': 1,
        }

    def run(self):
        """ Run command """

        RootRequired.require_root_permission()

        pr.p('Loading packages list...')
        pr.p('========================')

        loaded_packages = []

        for argument in self.arguments:
            arg_parts = argument.split('=')
            if len(arg_parts) == 1:
                # load last version as default
                pkg = Pkg.load_last(argument)
            else:
                # load specify version
                pkg = Pkg.load_version(arg_parts[0], arg_parts[1])
                if pkg == 1:
                    pkg = False
                elif pkg == 2:
                    self.message('package "' + arg_parts[0] + '" has not version "' + arg_parts[1] + '"' + ansi.reset, before=ansi.red)
                    continue
            if pkg:
                loaded_packages.append(pkg)
            else:
                self.message('unknow package "' + argument + '"' + ansi.reset, before=ansi.red)

        # remove local packages from list
        new_loaded_packages = []
        for pkg in loaded_packages:
            try:
                file_path = pkg.data['file_path']
                new_loaded_packages.append(pkg)
            except:
                self.message('package "' + pkg.data['name'] + '" is a local package', is_error=True)
        loaded_packages = new_loaded_packages

        if not loaded_packages:
            return 1

        # calculate transactions
        pr.p('Calculating transactions...')
        calc = Calculator()
        i = 0
        while i < len(loaded_packages):
            loaded_packages[i].is_manual = True
            i += 1
        calc.install(list(reversed(loaded_packages)))

        # show transaction
        TransactionShower.show(calc)

        if not self.has_option('-y') or self.has_option('--yes'):
            pr.p('Do you want to continue? [Y/n] ', end='')
            answer = input()
            if answer == 'y' or answer == 'Y' or answer == '':
                pass
            else:
                pr.p('Abort.')
                return 1

        # start download packages
        pr.p('Downloading packages...')
        downloaed_paths = []
        for pkg in calc.to_install:
            download_path = Env.cache_dir('/archives/' + pkg.data['name'] + '-' + pkg.wanted_version + '-' + pkg.data['arch'])
            download_cmd = DownloadCommand()
            i = 0
            res = 1
            tmp = True
            while tmp:
                if i > 5:
                    pr.e(ansi.red + 'Failed to download packages' + ansi.reset)
                    return res
                pr.p('Downloading ' + pkg.data['name'] + ':' + pkg.data['version'] + ':' + pkg.data['arch'] + '...')
                res = download_cmd.handle(ArgParser.parse(['cati', 'download', '-q', pkg.data['name'] + '=' + pkg.wanted_version, '--output=' + download_path]))
                if res == 1 or res == None:
                    tmp = False
                i += 1
            downloaed_paths.append([download_path, pkg.is_manual])
        pr.p('Download completed.')

        # remove packages
        if calc.to_remove:
            pr.p('Removing packages...')
            package_names = [pkg.data['name'] for pkg in calc.to_remove]
            remove_cmd = RemoveCommand()
            res = remove_cmd.handle(ArgParser.parse(['cati', 'remove', *package_names, '-y']))
            if res != 0 and res != None:
                pr.e(ansi.red + 'Failed to remove packages' + ansi.reset)
                return res

        # install packages
        pr.p('Installing packages...')
        for path in downloaed_paths:
            is_auto = []
            if not path[1]:
                is_auto = ['--auto']
            pkg_cmd = PkgCommand()
            res = pkg_cmd.handle(ArgParser.parse(['cati', 'pkg', 'install', path[0], *is_auto]))
            if res != 0 and res != None:
                pr.e(ansi.red + 'Failed to install packages' + ansi.reset)
                return res

        pr.p(ansi.green + 'Done.' + ansi.reset)
