#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barry.specs
===========
Classes for specifying assignments and submissions.

:copyright: (C) 2013, Matthew Frazier
:license:   MIT/X11, see LICENSE for details
"""
from .utils import HasDirectory, run_command
import os

#: A completely fulfilled requirement.
COMPLETE = u'complete'

#: A partially fulfilled requirement.
PARTIAL = u'partial'

#: A completely missed requirement.
INCOMPLETE = u'incomplete'

#: An extra requirement completed.
EXTRA = u'extra'

#: An extra requirement skipped.
SKIPPED = u'skipped'

#: Something went wrong grading.
PROBLEM = u'problem'


class Assignment(HasDirectory):
    """
    This represents an assignment Barry will grade.

    :param directory: The path to a directory containing the assignment
                      resources.
    """
    #: The assignment's title.
    title = None

    def __init__(self, directory):
        self.directory = directory

    def run_command(self, *command, **options):
        """
        Run a command in the resource directory, and return the corresponding
        Popen object.
        """
        options.setdefault("directory", self.directory)

        env = dict(RESOURCES=self.directory)
        if 'env' in options:
            env.update(options.get('env'))
        options['env'] = env

        return run_command(*command, **options)

    def prepare_resources(self):
        """
        This is called at the beginning of a grading session, and should
        set up any files that are required for the assignment.
        """
        pass

    def grade(self, submission, grade):
        """
        This should evaluate the submission and attach the appropriate marks.
        """
        pass


class Submission(HasDirectory):
    """
    This represents a student submission for the assignment.

    :param assignment: The assignment used to grade this submission.
    :param name: The name of the student who submitted this assignment.
    :param directory: The directory the assignment is located in.
    """
    def __init__(self, assignment, name, directory):
        self.assignment = assignment
        self.name = name
        self.directory = directory

    def run_command(self, *command, **options):
        """
        Run a command in the submission directory, and return the
        corresponding Popen object.
        """
        options.setdefault("directory", self.directory)

        env = dict(RESOURCES=self.assignment.directory)
        if 'env' in options:
            env.update(options.get('env'))
        options['env'] = env

        return run_command(*command, **options)

