# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import click

from apio.managers.installer import Installer
from apio.resources import Resources
from apio.profile import Profile

platforms = ['linux_x86_64',
             'linux_i686',
             'linux_armv7l',
             'linux_aarch64',
             'windows',
             'darwin']


@click.command('uninstall')
@click.pass_context
@click.argument('packages', nargs=-1)
@click.option('-a', '--all', is_flag=True,
              help='Uninstall all packages.')
@click.option('-l', '--list', is_flag=True,
              help='List all installed packages.')
@click.option('-p', '--platform', type=click.Choice(platforms),
              metavar='platform',
              help='Set the platform [{}] (Advanced).'.format(
                ', '.join(platforms)))
def cli(ctx, packages, all, list, platform):
    """Uninstall packages."""

    if packages:
        _uninstall(packages, platform)
    elif all:  # pragma: no cover
        packages = Profile().packages
        _uninstall(packages, platform)
    elif list:
        Resources(platform).list_packages(installed=True, notinstalled=False)
    else:
        click.secho(ctx.get_help())


def _uninstall(packages, platform):
    if click.confirm('Do you want to continue?'):
        for package in packages:
            Installer(package, platform, checkversion=False).uninstall()
    else:
        click.secho('Abort!', fg='red')
