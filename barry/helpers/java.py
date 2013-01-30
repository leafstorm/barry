#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barry.helpers.java
==================
A custom assignment class for grading students' Java projects.
This currently only supports building projects directly using javac
and running them directly using java - IDE support is out of scope for
now, unless I end up as a TA for 216.

:copyright: (C) 2013, Matthew Frazier
:license:   MIT/X11, see LICENSE for details
"""
from ..specs import Assignment, Submission, INCOMPLETE, PROBLEM
from ..grading import StopGrading

class JavaSubmission(Submission):
    def compile_class(self, grade, classname):
        filename = classname + ".java"

        if self.has_file(filename):
            grade.mark_complete("File is named %s" % filename)
            grade.attach_file(filename)
        else:
            raise StopGrading(INCOMPLETE, "%s is missing!" % filename)

        javac = self.run_command("javac", filename)
        if javac.returncode != 0:
            grade.attach_data("Compiler errors", javac.stderr.read())
            raise StopGrading(INCOMPLETE, "%s did not compile!" % filename)

    def run_class(self, classname, *args, **options):
        command = ["java"]
        if options.pop("use_resources", False):
            command.extend(("-cp", self.assignment.directory))
        command.append(classname)
        command.extend(args)

        return self.run_command(*command, **options)

    def grade_class(self, grade, classname, *args, **options):
        options.setdefault("timeout", 1.0)
        fail_on_exception = options.get("fail_on_exception", False)

        subp = self.run_class(classname, *args, **options)
        if subp.timed_out:
            raise StopGrading(INCOMPLETE, "%s did not terminate!" % classname)
        elif fail_on_exception and subp.returncode == 1:
            grade.attach_data("%s errors" % classname, javac.stderr.read())
            raise StopGrading(INCOMPLETE,
                              "%s terminated with an exception!" % classname)
        return subp

class JavaAssignment(Assignment):
    submission_class = JavaSubmission
