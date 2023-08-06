# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import json
import click
import semantic_version

from os.path import isfile, isdir

from apio import util


class Profile(object):

    def __init__(self):
        self.config = {'exe': 'default', 'verbose': 0}
        self.labels = {'exe': 'Executable', 'verbose': 'Verbose'}
        self.settings = {}
        self.packages = {}
        self._profile_path = util.safe_join(
            util.get_home_dir(), 'profile.json')
        self.load()

    def installed_version(self, name, version):
        if name in self.packages:
            pkg_version = self.get_package_version(name)
            pkg_version = self._convert_old_version(pkg_version)
            version = self._convert_old_version(version)
            return (semantic_version.Version(pkg_version) ==
                    semantic_version.Version(version))

    def _convert_old_version(self, version):
        # Convert old versions to new format
        try:
            v = int(version)
            version = '1.{}.0'.format(v)
        except ValueError:
            pass
        return version

    def check_exe_default(self):
        return self.config.get('exe', '') == 'default'

    def add_package(self, name, version):
        self.packages[name] = {'version': version}

    def add_setting(self, key, value):
        self.settings[key] = value

    def add_config(self, key, value):
        if self.config.get(key, None) != value:
            self.config[key] = value
            self.save()
            click.secho('{0} mode updated: {1}'.format(
                self.labels.get(key, ''), value), fg='green')
        else:
            click.secho('{0} mode already {1}'.format(
                self.labels.get(key, ''), value), fg='yellow')

    def remove_package(self, name):
        if name in self.packages.keys():
            del self.packages[name]

    def get_verbose_mode(self):
        return int(self.config.get('verbose', False))

    def get_package_version(self, name, release_name=''):
        version = '0.0.0'
        if name in self.packages:
            version = self.packages.get(name).get('version')
        elif release_name:
            dir_name = util.get_package_dir(release_name)
            if isdir(dir_name):
                filepath = util.safe_join(dir_name, 'package.json')
                try:
                    with open(filepath, 'r') as json_file:
                        tmp_data = json.load(json_file)
                        if 'version' in tmp_data.keys():
                            version = tmp_data.get('version')
                except Exception:
                    pass
        return version

    def load(self):
        if isfile(self._profile_path):
            with open(self._profile_path, 'r') as profile:
                try:
                    self._load_profile(profile)
                except Exception:
                    pass

    def _load_profile(self, profile):
        data = json.load(profile)
        if 'config' in data.keys():
            self.config = data.get('config')
            if 'exe' not in self.config.keys():
                self.config['exe'] = 'default'
            if 'verbose' not in self.config.keys():
                self.config['verbose'] = 0
        if 'settings' in data.keys():
            self.settings = data.get('settings')
        if 'packages' in data.keys():
            self.packages = data.get('packages')
        else:
            self.packages = data  # Backward compatibility

    def save(self):
        util.mkdir(self._profile_path)
        with open(self._profile_path, 'w') as profile:
            data = {
                'config': self.config,
                'settings': self.settings,
                'packages': self.packages
            }
            json.dump(data, profile, indent=4, sort_keys=True)

    def list(self):
        for key in self.config:
            click.secho('{0} mode: {1}'.format(
                    self.labels.get(key, ''), self.config.get(key, '')),
                fg='yellow')
