#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barry.utils
===========
Internal utilities used by Barry, you know the drill.

:copyright: (C) 2013, Matthew Frazier
:license:   MIT/X11, see LICENSE for details
"""
import os
import subprocess

def run_command(command, directory, env=None):
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    subp = subprocess.Popen(command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=directory,
        env=full_env,
        shell=isinstance(command, basestring)
    )
    subp.wait()
    return subp


class HasDirectory(object):
    """
    This provides access to the files and directories inside a class's "main"
    directory. Subclasses of this class should have a `directory` attribute,
    with the full path to its directory.
    """
    def exists(self):
        return os.path.isdir(self.directory)

    def has_file(self, name):
        return os.path.isfile(os.path.join(self.directory, name))

    def open_file(self, name, mode):
        return open(os.path.join(self.directory, name), mode)

    def file_contents(self, name):
        with self.open_file(name, 'r') as fd:
            return fd.read()

    def has_dir(self, name):
        return os.path.isdir(os.path.join(self.directory, name))

