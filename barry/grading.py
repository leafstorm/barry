#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barry.grading
=============
Classes that store information about grading in progress.

:copyright: (C) 2013, Matthew Frazier
:license:   MIT/X11, see LICENSE for details
"""
import os
import traceback
from .specs import (Submission,
                    COMPLETE, PARTIAL, INCOMPLETE, EXTRA, SKIPPED, PROBLEM)
from pygments import highlight
from pygments.lexers import (get_lexer_by_name, guess_lexer_for_filename,
                             TextLexer)
from pygments.util import ClassNotFound


class StopGrading(BaseException):
    def __init__(self, category, reason):
        self.category = category
        self.reason = reason

    def __str__(self):
        return "%s: %s" % (self.category, self.reason)


class AttachedFile(object):
    def __init__(self, filename, content, format=None):
        self.filename = filename
        self.content = content
        self.format = format

    @classmethod
    def from_file(cls, path, format=None):
        with open(path, 'r') as fd:
            return cls(os.path.basename(path), fd.read(), format)

    def highlight(self, formatter):
        return highlight(self.content, self.lexer, formatter)

    @property
    def lexer(self):
        if self.format is None:
            try:
                return guess_lexer_for_filename(self.filename, self.content)
            except ClassNotFound:
                return TextLexer()
        else:
            return get_lexer_by_name(self.format)


class GradingSession(object):
    def __init__(self, assignment):
        self.assignment = assignment
        self.submissions = {}
        self.grades = {}

    def add_submission(self, name, path):
        if name is None:
            name = os.path.basename(path)
        sub = Submission(self.assignment, name, path)
        self.submissions[name] = sub
        return sub

    def grade(self, submission):
        grade = SubmissionGrade(submission)

        if submission.exists():
            try:
                category = self.assignment.grade(submission, grade)
            except StopGrading as exc:
                grade.add_mark(exc.category, exc.message)
                grade.category = exc.category
            except Exception as exc:
                grade.mark_problem("Grading generated an exception!")
                grade.category = INCOMPLETE
                tb = traceback.format_exc()
                grade.attach_data("Python Traceback", tb, "pytb")
            else:
                if category is not None:
                    grade.category = category
        else:
            grade.mark_incomplete("Did not submit an assignment")
            grade.category = SKIPPED

        return grade

    def all_grades(self):
        for name, submission in self.submissions.items():
            if name not in self.grades:
                self.grades[name] = self.grade(submission)
            yield name, submission, self.grades[name]


class SubmissionGrade(object):
    def __init__(self, submission):
        self.submission = submission
        self.marks = []
        self.files = []
        self.category = None

    def add_mark(self, category, text):
        if isinstance(text, str):
            text = text.decode('utf8')
        self.marks.append((category, text))

    def mark_complete(self, text):
        self.add_mark(COMPLETE, text)

    def mark_partial(self, text):
        self.add_mark(PARTIAL, text)

    def mark_incomplete(self, text):
        self.add_mark(INCOMPLETE, text)

    def mark_extra(self, text):
        self.add_mark(EXTRA, text)

    def mark_skipped(self, text):
        self.add_mark(SKIPPED, text)

    def mark_problem(self, text):
        self.add_mark(PROBLEM, text)

    def attach_file(self, name, format=None):
        if not self.submission.has_file(name):
            raise Exception(name + " is not in assignment")

        self.files.append(AttachedFile.from_file(
            os.path.join(self.submission.directory, name),
            format
        ))

    def attach_data(self, name, content, format=None):
        self.files.append(AttachedFile(name, content, format))

