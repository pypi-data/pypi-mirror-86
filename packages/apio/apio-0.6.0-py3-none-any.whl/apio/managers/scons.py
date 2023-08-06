# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import os
import re
import sys
import time
import click
import datetime
import pkg_resources
import semantic_version

from os.path import isfile

from apio import util
from apio.managers.arguments import process_arguments
from apio.managers.arguments import format_vars
from apio.managers.system import System
from apio.profile import Profile
from apio.resources import Resources


class SCons(object):

    def __init__(self, project_dir=''):
        self.profile = Profile()
        self.resources = Resources()

        if project_dir is not None:
            # Move to project dir
            project_dir = util.check_dir(project_dir)
            os.chdir(project_dir)

    @util.command
    def clean(self, args):
        try:
            var, board, arch = process_arguments(args, self.resources)
        except Exception:
            arch = "ice40"
            pass
        return self.run('-c', arch=arch, packages=['scons'])

    @util.command
    def verify(self, args):
        var, board, arch = process_arguments(args, self.resources)
        return self.run('verify', arch=arch, packages=['scons',
                                                       'iverilog',
                                                       'yosys'])

    @util.command
    def lint(self, args):
        var_dummy, board, arch = process_arguments(None, self.resources)
        var = format_vars({
            'all': args.get('all'),
            'top': args.get('top'),
            'nowarn': args.get('nowarn'),
            'warn': args.get('warn'),
            'nostyle': args.get('nostyle')
        })
        return self.run('lint', var, arch=arch, packages=['scons',
                                                          'verilator',
                                                          'yosys'])

    @util.command
    def sim(self):
        var, board, arch = process_arguments(None, self.resources)
        return self.run('sim', arch=arch, packages=['scons', 'iverilog',
                                                    'yosys', 'gtkwave'])

    @util.command
    def build(self, args):
        var, board, arch = process_arguments(args, self.resources)
        return self.run('build', var, board, arch, packages=['scons', 'yosys',
                                                             arch])

    @util.command
    def time(self, args):
        var, board, arch = process_arguments(args, self.resources)
        return self.run('time', var, board, arch, packages=['scons', 'yosys',
                                                            arch])

    @util.command
    def upload(self, args, serial_port, ftdi_id, sram, flash):
        var, board, arch = process_arguments(args, self.resources)
        programmer = self.get_programmer(board, serial_port, ftdi_id,
                                         sram, flash)
        var += ['prog={0}'.format(programmer)]
        return self.run('upload', var, board, arch, packages=['scons', 'yosys',
                                                              arch])

    def get_programmer(self, board, ext_serial, ext_ftdi_id, sram, flash):
        programmer = ''

        if board:
            board_data = self.resources.boards.get(board)

            # Check platform
            self.check_platform(board_data)

            # Check pip packages
            self.check_pip_packages(board_data)

            # Serialize programmer command
            programmer = self.serialize_programmer(board_data, sram, flash)

            # Replace USB vendor id
            if '${VID}' in programmer:
                vid = board_data.get('usb').get('vid')
                programmer = programmer.replace('${VID}', vid)

            # Replace USB product id
            if '${PID}' in programmer:
                pid = board_data.get('usb').get('pid')
                programmer = programmer.replace('${PID}', pid)

            # Replace FTDI index
            if '${FTDI_ID}' in programmer:
                self.check_usb(board, board_data)
                ftdi_id = self.get_ftdi_id(board, board_data, ext_ftdi_id)
                programmer = programmer.replace('${FTDI_ID}', ftdi_id)

            # TinyFPGA BX board is not detected in MacOS HighSierra
            if 'tinyprog' in board_data and 'darwin' in util.get_systype():
                # In this case the serial check is ignored
                return 'tinyprog --libusb --program'

            # Replace Serial port
            if '${SERIAL_PORT}' in programmer:
                self.check_usb(board, board_data)
                device = self.get_serial_port(board, board_data, ext_serial)
                programmer = programmer.replace('${SERIAL_PORT}', device)

        return programmer

    def check_platform(self, board_data):
        if 'platform' not in board_data:
            return

        platform = board_data.get('platform')
        current_platform = util.get_systype()
        if platform != current_platform:
            # Incorrect platform
            if platform == 'linux_armv7l':
                raise Exception(
                    'incorrect platform: RPI2 or RPI3 required')
            else:
                raise Exception(
                    'incorrect platform {0}'.format(platform))

    def check_pip_packages(self, board_data):
        prog_info = board_data.get('programmer')
        content = self.resources.programmers.get(prog_info.get('type'))
        all_pip_packages = self.resources.distribution.get('pip_packages')

        pip_packages = content.get('pip_packages') or []
        for pip_pkg in pip_packages:
            try:
                # Check pip_package version
                spec = semantic_version.Spec(all_pip_packages.get(pip_pkg, ''))
                pkg_version = pkg_resources.get_distribution(pip_pkg).version
                version = semantic_version.Version(pkg_version)
                if not spec.match(version):
                    click.secho(
                        'Error: \'{}\' '.format(pip_pkg) +
                        'version ({}) '.format(version) +
                        'does not match {}'.format(spec),
                        fg='red')
                    click.secho('Please run:\n'
                                '   pip install -U apio[{}]'.format(pip_pkg),
                                fg='yellow')
                    raise Exception
            except pkg_resources.DistributionNotFound:
                click.secho(
                    'Error: \'{}\' is not installed'.format(pip_pkg),
                    fg='red')
                click.secho('Please run:\n'
                            '   pip install -U apio[{}]'.format(pip_pkg),
                            fg='yellow')
                raise Exception
            try:
                # Check pip_package itself
                __import__(pip_pkg)
            except Exception as e:
                # Exit if a package is not working
                python_version = util.get_python_version()
                message = '\'{}\' not compatible with '.format(pip_pkg)
                message += 'Python {}'.format(python_version)
                message += '\n       {}'.format(e)
                raise Exception(message)

    def serialize_programmer(self, board_data, sram, flash):
        prog_info = board_data.get('programmer')
        content = self.resources.programmers.get(prog_info.get('type'))

        programmer = content.get('command')

        # Add args
        if content.get('args'):
            programmer += ' {}'.format(content.get('args'))

        # Add extra args
        if prog_info.get('extra_args'):
            programmer += ' {}'.format(prog_info.get('extra_args'))

        # Enable SRAM programming
        if sram:
            # Only for iceprog programmer
            if programmer.startswith('iceprog'):
                programmer += ' -S'

        if flash:
            # Only for ujprog programmer
            if programmer.startswith('ujprog'):
                programmer = programmer.replace('SRAM', 'FLASH')

        return programmer

    def check_usb(self, board, board_data):
        if 'usb' not in board_data:
            raise Exception('Missing board configuration: usb')

        usb_data = board_data.get('usb')
        hwid = '{0}:{1}'.format(
            usb_data.get('vid'),
            usb_data.get('pid')
        )
        found = False
        for usb_device in System().get_usb_devices():
            if usb_device.get('hwid') == hwid:
                found = True
                break

        if not found:
            # Board not connected
            if 'tinyprog' in board_data:
                click.secho(
                    'Activate bootloader by pressing the reset button',
                    fg='yellow')
            raise Exception('board ' + board + ' not connected')

    def get_serial_port(self, board, board_data, ext_serial_port):
        # Search Serial port by USB id
        device = self._check_serial(board, board_data, ext_serial_port)
        if device is None:
            # Board not connected
            raise Exception('board ' + board + ' not connected')
        return device

    def _check_serial(self, board, board_data, ext_serial_port):
        if 'usb' not in board_data:
            raise Exception('Missing board configuration: usb')

        usb_data = board_data.get('usb')
        hwid = '{0}:{1}'.format(
            usb_data.get('vid'),
            usb_data.get('pid')
        )

        # Match the discovered serial ports
        serial_ports = util.get_serial_ports()
        if len(serial_ports) == 0:
            # Board not available
            raise Exception('board ' + board + ' not available')
        for serial_port_data in serial_ports:
            port = serial_port_data.get('port')
            if ext_serial_port and ext_serial_port != port:
                # If the --device options is set but it doesn't match
                # the detected port, skip the port.
                continue
            if hwid.lower() in serial_port_data.get('hwid').lower():
                if 'tinyprog' in board_data and \
                   not self._check_tinyprog(board_data, port):
                    # If the board uses tinyprog use its port detection
                    # to double check the detected port.
                    # If the port is not detected, skip the port.
                    continue
                # If the hwid and the description pattern matches
                # with the detected port return the port.
                return port

    def _check_tinyprog(self, board_data, port):
        desc_pattern = '^' + board_data.get('tinyprog').get('desc') + '$'
        for tinyprog_meta in util.get_tinyprog_meta():
            tinyprog_port = tinyprog_meta.get('port')
            tinyprog_name = tinyprog_meta.get('boardmeta').get('name')
            if port == tinyprog_port and re.match(desc_pattern, tinyprog_name):
                # If the port is detected and it matches the pattern
                return True

    def get_ftdi_id(self, board, board_data, ext_ftdi_id):
        # Search device by FTDI id
        ftdi_id = self._check_ftdi(board, board_data, ext_ftdi_id)
        if ftdi_id is None:
            # Board not connected
            raise Exception('board ' + board + ' not connected')
        return ftdi_id

    def _check_ftdi(self, board, board_data, ext_ftdi_id):
        if 'ftdi' not in board_data:
            raise Exception('Missing board configuration: ftdi')

        desc_pattern = '^' + board_data.get('ftdi').get('desc') + '$'

        # Match the discovered FTDI chips
        ftdi_devices = System().get_ftdi_devices()
        if len(ftdi_devices) == 0:
            # Board not available
            raise Exception('board ' + board + ' not available')
        for ftdi_device in ftdi_devices:
            index = ftdi_device.get('index')
            if ext_ftdi_id and ext_ftdi_id != index:
                # If the --device options is set but it doesn't match
                # with the detected index, skip the port.
                continue
            if re.match(desc_pattern, ftdi_device.get('description')):
                # If matches the description pattern
                # return the index for the FTDI device.
                return index

    def run(self, command, variables=[], board=None, arch=None, packages=[]):
        """Executes scons for building"""

        # -- Check for the SConstruct file
        if not isfile(util.safe_join(util.get_project_dir(), 'SConstruct')):
            variables += ['-f']
            variables += [util.safe_join(
                util.get_folder('resources'), arch, 'SConstruct')]
        else:
            click.secho('Info: use custom SConstruct file')

        # -- Resolve packages
        if self.profile.check_exe_default():
            # Run on `default` config mode
            if not util.resolve_packages(
              packages,
              self.profile.packages,
              self.resources.distribution.get('packages')
             ):
                # Exit if a package is not installed
                raise Exception
        else:
            click.secho('Info: native config mode')

        # -- Execute scons
        return self._execute_scons(command, variables, board)

    def _execute_scons(self, command, variables, board):
        terminal_width, _ = click.get_terminal_size()
        start_time = time.time()

        if command == 'build' or \
           command == 'upload' or \
           command == 'time':
            if board:
                processing_board = board
            else:
                processing_board = 'custom board'
            click.echo('[%s] Processing %s' % (
                datetime.datetime.now().strftime('%c'),
                click.style(processing_board, fg='cyan', bold=True)))
            click.secho('-' * terminal_width, bold=True)

        if self.profile.get_verbose_mode() > 0:
            click.secho('Executing: {}'.format(
                        ' '.join(util.scons_command + ['-Q', command] +
                                 variables)))

        result = util.exec_command(
            util.scons_command + ['-Q', command] + variables,
            stdout=util.AsyncPipe(self._on_stdout),
            stderr=util.AsyncPipe(self._on_stderr)
        )

        # -- Print result
        exit_code = result.get('returncode')
        is_error = exit_code != 0
        summary_text = ' Took %.2f seconds ' % (time.time() - start_time)
        half_line = '=' * int(
            ((terminal_width - len(summary_text) - 10) / 2))
        click.echo('%s [%s]%s%s' % (
            half_line,
            (click.style(' ERROR ', fg='red', bold=True)
             if is_error else click.style('SUCCESS', fg='green', bold=True)),
            summary_text,
            half_line
        ), err=is_error)

        return exit_code

    def _on_stdout(self, line):
        fg = 'green' if 'is up to date' in line else None
        click.secho(line, fg=fg)

    def _on_stderr(self, line):
        if '%|' in line and '100%|' not in line:
            # Remove previous line for tqdm progress bar
            CURSOR_UP = '\033[F'
            ERASE_LINE = '\033[K'
            sys.stdout.write(CURSOR_UP + ERASE_LINE)
        fg = 'red' if 'error' in line.lower() else 'yellow'
        click.secho(line, fg=fg)
