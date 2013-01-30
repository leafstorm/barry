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
import time
import subprocess

def run_command(*command, **options):
    """
    Runs a command using `subprocess`. It accepts a plethora of options.
    All of them except `command` should be specified by keyword.

    :param command:     The actual command to run. Each word is an argument,
                        this does not parse using the shell.
    :param directory:   The working directory to use for the command.
                        (The default is, of course, the working directory.)
    :param env:         A dictionary to update the current environment with.
    :param wait:        If `True` (the default), `run_command` will wait for
                        the process to complete before returning.
                        (It will also automatically close the program's
                        stdin to prevent it from hanging.)
    :param timeout:     If this is not `None`, the program will automatically
                        be terminated after `timeout` seconds elapse.
                        The returned subprocess's `timed_out` attribute will
                        be `True` if this occurred, and `False` if not.
                        (In case you have really devious students, this will
                        go for a SIGKILL 0.05 seconds later if the process
                        doesn't terminate.)
    :param output:      This can accept one of three values. ``"split"`` (the
                        default) captures stdout and stderr like normal, as
                        separate streams. ``"merge"`` pipes stderr into
                        stdout, so that all output can be read from stderr.
                        ``"console"`` sends output to the console.
    :param input:       If `True`, this connects stdin to your console.
                        (Probably a bad idea, since the whole point of using
                        Barry is *not* having to type things.)
                        If otherwise not `None`, this will be fed into the
                        process's standard input before it returns.
    """
    directory = options.get("directory")
    full_env = os.environ.copy()
    if "env" in options and options["env"] is not None:
        full_env.update(options["env"])

    outputs = {
        'split':    (subprocess.PIPE,   subprocess.PIPE),
        'merge':    (subprocess.PIPE,   subprocess.STDOUT),
        'console':  (None,              None)
    }
    stdout, stderr = outputs[options.get("output", "split")]
    input = options.get("input")

    subp = subprocess.Popen(command,
        stdin=(None if input is True else subprocess.PIPE),
        stdout=stdout,
        stderr=stderr,
        cwd=directory,
        env=full_env
    )

    if input is not None and input is not True:
        subp.stdin.write(input)

    subp.timed_out = False
    if options.get("wait", True):
        subp.stdin.close()

        timeout = options.get("timeout")
        if timeout is not None:
            deadline = time.time() + timeout
            while time.time() < deadline and subp.poll() is None:
                time.sleep(0.1)
            if subp.poll() is None:
                subp.terminate()
                subp.timed_out = True
                # Protect against programs that absorb SIGTERM
                time.sleep(0.05)
                if subp.poll() is None:
                    subp.kill()
        else:
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

