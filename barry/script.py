#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barry.script
============
The command-line interface for Barry.

:copyright: (C) 2013, Matthew Frazier
:license:   MIT/X11, see LICENSE for details
"""
import argparse
import os.path
import progressbar
from .grading import GradingSession
from jinja2 import Environment, PackageLoader
from pygments.formatters import HtmlFormatter


def create_parser(title):
    parser = argparse.ArgumentParser(
        description="Create a grading report for " + title + ".",
        fromfile_prefix_chars="@"
    )

    parser.add_argument('names', metavar='NAME', nargs='+',
        help="The names of students to grade.")

    parser.add_argument('-s', '--submissions', dest='submissions_dir',
        default='.', help="The directory to search in for submissions.")

    parser.add_argument('-r', '--resources', dest='resources_dir',
        default='resources', help="The directory assignment resources are "
                                  "stored in.")

    parser.add_argument('-o', '--output', dest='output_filename',
        default='report.html', help="The file to write grading information to.")

    return parser


def grading_session(assignment_class):
    parser = create_parser(assignment_class.title)
    options = parser.parse_args()

    assignment = assignment_class(os.path.abspath(options.resources_dir))
    assignment.prepare_resources()
    session = GradingSession(assignment)

    for name in options.names:
        path = os.path.join(options.submissions_dir, name)
        session.add_submission(name, path)

    widgets = ["Grading assignments: ",
               progressbar.Bar(marker="=", left="[", right="]"),
               " ", progressbar.SimpleProgress()]
    pbar = progressbar.ProgressBar(widgets=widgets,
                                   maxval=len(session.submissions)).start()

    for i, (name, submission, grade) in enumerate(session.all_grades()):
        pbar.update(i + 1)
    pbar.finish()

    grades = list(session.all_grades())

    templates = Environment(loader=PackageLoader('barry', 'templates'))
    template = templates.get_template('report.html')

    formatter = HtmlFormatter()

    html = template.render({
        'assignment': assignment,
        'session': session,
        'grades': grades,
        'pygments': formatter
    })

    with open(options.output_filename, 'w') as fd:
        fd.write(html)

    print "Grading session finished - report is in", options.output_filename

