# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import re
import click
import platform

from apio import util
from apio.profile import Profile
from apio.resources import Resources


class System(object):  # pragma: no cover
    def __init__(self):
        profile = Profile()
        resources = Resources()

        self.name = 'system'
        self.version = util.get_package_version(self.name, profile)
        self.spec_version = util.get_package_spec_version(self.name, resources)

        self.ext = ''
        if 'Windows' == platform.system():
            self.ext = '.exe'

    def lsusb(self):
        returncode = 1
        result = self._run_command('lsusb')

        if result:
            returncode = result.get('returncode')

        return returncode

    def lsftdi(self):
        returncode = 1
        result = self._run_command('lsftdi')

        if result:
            returncode = result.get('returncode')

        return returncode

    def lsserial(self):
        returncode = 0
        serial_ports = util.get_serial_ports()
        click.secho(
            'Number of Serial devices found: {}\n'.format(len(serial_ports)))

        for serial_port in serial_ports:
            port = serial_port.get('port')
            description = serial_port.get('description')
            hwid = serial_port.get('hwid')
            click.secho(port, fg='cyan')
            click.secho('Description: {}'.format(description))
            click.secho('Hardware info: {}\n'.format(hwid))

        return returncode

    def get_usb_devices(self):
        usb_devices = []
        result = self._run_command('lsusb', silent=True)

        if result and result.get('returncode') == 0:
            usb_devices = self._parse_usb_devices(result.get('out'))
        else:
            raise Exception

        return usb_devices

    def get_ftdi_devices(self):
        ftdi_devices = []
        result = self._run_command('lsftdi', silent=True)

        if result and result.get('returncode') == 0:
            ftdi_devices = self._parse_ftdi_devices(result.get('out'))
        else:
            raise Exception

        return ftdi_devices

    def _run_command(self, command, silent=False):
        result = {}
        system_base_dir = util.get_package_dir('tools-system')
        system_bin_dir = util.safe_join(system_base_dir, 'bin')

        on_stdout = None if silent else self._on_stdout
        on_stderr = self._on_stderr

        if util.check_package(
            self.name,
            self.version,
            self.spec_version,
            system_bin_dir
        ):
            result = util.exec_command(
                util.safe_join(system_bin_dir, command + self.ext),
                stdout=util.AsyncPipe(on_stdout),
                stderr=util.AsyncPipe(on_stderr))

        return result

    def _on_stdout(self, line):
        click.secho(line)

    def _on_stderr(self, line):
        click.secho(line, fg='red')

    def _parse_usb_devices(self, text):
        pattern = '(?P<hwid>[a-f0-9]{4}:[a-f0-9]{4}?)\s'
        hwids = re.findall(pattern, text)

        usb_devices = []

        for hwid in hwids:
            usb_device = {
                'hwid': hwid
            }
            usb_devices.append(usb_device)

        return usb_devices

    def _parse_ftdi_devices(self, text):
        pattern = 'Number\sof\sFTDI\sdevices\sfound:\s(?P<n>\d+?)\n'
        match = re.search(pattern, text)
        n = int(match.group('n')) if match else 0

        pattern = '.*Checking\sdevice:\s(?P<index>.*?)\n.*'
        index = re.findall(pattern, text)

        pattern = '.*Manufacturer:\s(?P<n>.*?),.*'
        manufacturer = re.findall(pattern, text)

        pattern = '.*Description:\s(?P<n>.*?)\n.*'
        description = re.findall(pattern, text)

        ftdi_devices = []

        for i in range(n):
            ftdi_device = {
                'index': index[i],
                'manufacturer': manufacturer[i],
                'description': description[i]
            }
            ftdi_devices.append(ftdi_device)

        return ftdi_devices
