# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import json
import click
from collections import OrderedDict

from apio import util
from apio.profile import Profile

BOARDS_MSG = """
Use `apio init --board <boardname>` to create a new apio """ \
"""project for that board"""


class Resources(object):

    def __init__(self, platform=''):
        self.packages = self._load_resource('packages')
        self.boards = self._load_resource('boards')
        self.fpgas = self._load_resource('fpgas')
        self.programmers = self._load_resource('programmers')
        self.distribution = self._load_resource('distribution')

        # Check available packages
        self.packages = self._check_packages(self.packages, platform)

        # Sort resources
        self.packages = OrderedDict(sorted(self.packages.items(),
                                           key=lambda t: t[0]))
        self.boards = OrderedDict(sorted(self.boards.items(),
                                         key=lambda t: t[0]))
        self.fpgas = OrderedDict(sorted(self.fpgas.items(),
                                        key=lambda t: t[0]))

    def _load_resource(self, name):
        resource = None
        filepath = util.safe_join(util.get_folder('resources'), name + '.json')
        with open(filepath, 'r') as f:
            # Load the JSON file
            resource = json.loads(f.read())
        return resource

    def get_package_release_name(self, package):
        return self.packages.get(package).get('release').get('package_name')

    def get_packages(self):
        # Classify packages
        installed_packages = []
        notinstalled_packages = []

        for package in self.packages:
            data = {
                'name': package,
                'version': None,
                'description': self.packages.get(package).get('description')
            }
            if package in self.profile.packages:
                data['version'] = self.profile.get_package_version(
                    package, self.get_package_release_name(package))
                installed_packages += [data]
            else:
                notinstalled_packages += [data]

        for package in self.profile.packages:
            if package not in self.packages:
                data = {
                    'name': package,
                    'version': 'Unknown',
                    'description': 'Unknown deprecated package'
                }
                installed_packages += [data]

        return installed_packages, notinstalled_packages

    def list_packages(self, installed=True, notinstalled=True):
        """Return a list with all the installed/notinstalled packages"""

        self.profile = Profile()

        # Classify packages
        installed_packages, notinstalled_packages = self.get_packages()

        # Print tables
        terminal_width, _ = click.get_terminal_size()

        if installed and installed_packages:

            # - Print installed packages table
            click.echo('\nInstalled packages:\n')

            PACKAGELIST_TPL = ('{name:20} {description:30} {version:<8}')

            click.echo('-' * terminal_width)
            click.echo(PACKAGELIST_TPL.format(
                name=click.style('Name', fg='cyan'), version='Version',
                description='Description'))
            click.echo('-' * terminal_width)

            for package in installed_packages:
                click.echo(PACKAGELIST_TPL.format(
                    name=click.style(package.get('name'), fg='cyan'),
                    version=package.get('version'),
                    description=package.get('description')))

        if notinstalled and notinstalled_packages:

            # - Print not installed packages table
            click.echo('\nNot installed packages:\n')

            PACKAGELIST_TPL = ('{name:20} {description:30}')

            click.echo('-' * terminal_width)
            click.echo(PACKAGELIST_TPL.format(
                name=click.style('Name', fg='yellow'),
                description='Description'))
            click.echo('-' * terminal_width)

            for package in notinstalled_packages:
                click.echo(PACKAGELIST_TPL.format(
                    name=click.style(package.get('name'), fg='yellow'),
                    description=package.get('description')))

    def list_boards(self):
        """Return a list with all the supported boards"""

        # Print table
        click.echo('\nSupported boards:\n')

        BOARDLIST_TPL = ('{board:25} {fpga:30} {arch:<8} '
                         '{type:<12} {size:<5} {pack:<10}')
        terminal_width, _ = click.get_terminal_size()

        click.echo('-' * terminal_width)
        click.echo(BOARDLIST_TPL.format(
            board=click.style('Board', fg='cyan'), fpga='FPGA',
            arch='Arch', type='Type', size='Size', pack='Pack'))
        click.echo('-' * terminal_width)

        for board in self.boards:
            fpga = self.boards.get(board).get('fpga')
            click.echo(BOARDLIST_TPL.format(
                board=click.style(board, fg='cyan'),
                fpga=fpga,
                arch=self.fpgas.get(fpga).get('arch'),
                type=self.fpgas.get(fpga).get('type'),
                size=self.fpgas.get(fpga).get('size'),
                pack=self.fpgas.get(fpga).get('pack')))

        click.secho(BOARDS_MSG, fg='green')

    def list_fpgas(self):
        """Return a list with all the supported FPGAs"""

        # Print table
        click.echo('\nSupported FPGAs:\n')

        FPGALIST_TPL = ('{fpga:40} {arch:<8} {type:<12} {size:<5} {pack:<10}')
        terminal_width, _ = click.get_terminal_size()

        click.echo('-' * terminal_width)
        click.echo(FPGALIST_TPL.format(
            fpga=click.style('FPGA', fg='cyan'), type='Type', arch='Arch',
            size='Size', pack='Pack'))
        click.echo('-' * terminal_width)

        for fpga in self.fpgas:
            click.echo(FPGALIST_TPL.format(
                fpga=click.style(fpga, fg='cyan'),
                arch=self.fpgas.get(fpga).get('arch'),
                type=self.fpgas.get(fpga).get('type'),
                size=self.fpgas.get(fpga).get('size'),
                pack=self.fpgas.get(fpga).get('pack')))

    def _check_packages(self, packages, current_platform=''):
        filtered_packages = {}
        for pkg in packages.keys():
            check = True
            release = packages.get(pkg).get('release')
            if 'available_platforms' in release:
                platforms = release.get('available_platforms')
                check = False
                current_platform = current_platform or util.get_systype()
                for platform in platforms:
                    check |= current_platform in platform
            if check:
                filtered_packages[pkg] = packages.get(pkg)
        return filtered_packages
