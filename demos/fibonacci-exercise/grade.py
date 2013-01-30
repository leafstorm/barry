#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from barry import grading_session, COMPLETE, PARTIAL, INCOMPLETE
from barry.helpers.java import JavaAssignment

class FibonacciExercise(JavaAssignment):
    title = u"Exercise 1 - Fibonacci"

    def prepare_resources(self):
        make = self.run_command("make", "expected.txt", output="console")
        self.expected_output = self.file_contents("expected.txt")

    def grade(self, submission, grade):
        submission.compile_class(grade, "Fibonacci")
        program = submission.grade_class(grade, "Fibonacci")

        output = program.stdout.read()
        grade.attach_data("Fibonacci output", output)

        if output == self.expected_output:
            grade.mark_complete("Fibonacci generated the correct output")
            return COMPLETE
        else:
            grade.mark_partial("Fibonacci output is incorrect")
            return PARTIAL


grading_session(FibonacciExercise)
