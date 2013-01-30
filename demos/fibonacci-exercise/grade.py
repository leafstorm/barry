#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from barry import Assignment, grading_session, COMPLETE, PARTIAL, INCOMPLETE

class FibonacciExercise(Assignment):
    title = u"Exercise 1 - Fibonacci"

    def prepare_resources(self):
        make = self.run_command("make", "expected.txt", output="console")
        self.expected_output = self.file_contents("expected.txt")

    def grade(self, submission, grade):
        if submission.has_file("Fibonacci.java"):
            grade.mark_complete("File is named Fibonacci.java")
            grade.attach_file("Fibonacci.java")
        else:
            grade.mark_incomplete("Fibonacci.java is missing!")
            return INCOMPLETE

        javac = submission.run_command("javac", "Fibonacci.java")
        if javac.returncode != 0:
            grade.mark_incomplete("Fibonacci.java did not compile")
            grade.attach_data("Compiler errors", javac.stderr.read())
            return INCOMPLETE

        program = submission.run_command("java", "Fibonacci",
                                        timeout=0.5)
        if program.timed_out:
            grade.mark_incomplete("Fibonacci looped forever")
            return INCOMPLETE
        elif program.returncode != 0:
            grade.mark_incomplete("Fibonacci terminated with an exception")
            grade.attach_data("Fibonacci errors", program.stderr.read())
            return INCOMPLETE

        output = program.stdout.read()
        grade.attach_data("Fibonacci output", output)

        if output == self.expected_output:
            grade.mark_complete("Fibonacci generated the correct output")
            return COMPLETE
        else:
            grade.mark_partial("Fibonacci output is incorrect")
            return PARTIAL


grading_session(FibonacciExercise)
