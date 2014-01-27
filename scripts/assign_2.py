#!/usr/bin/env python3

import os
import re
import subprocess
import sys

from grade_script import *

def close_to(a, b):
    if a > 10000:
        correct_range = 2
    else:
        correct_range = 0.5
    return abs(a - b) < correct_range

def main():
    answers = [6250, 310338195, 2.8]
    score = 0
    print_eval_name()

    for filename in os.listdir(os.getcwd()):
        if filename.endswith('py'):
            print_eval_problem(filename)
            output = subprocess.check_output(['python3', filename])
            output_str = output.decode().strip()

            output_match = re.search(r'[0-9.]+', output_str)
            problem_match = re.search(r'[0-9]+', filename)

            if problem_match:
                try:
                    correct_answer = answers[int(problem_match.group(0))-1]
                except:
                    correct_answer = 'Problem not identifiable by filename, answer is one of {}'.format(str(answers))
            else:
                correct_answer = 'Problem not identifiable by filename, answer is one of {}'.format(str(answers))

            if output_match:
                number_extracted = round(float(output_match.group(0)), 1)
            else:
                number_extracted = float('inf')

            if any(close_to(answer, number_extracted) for answer in answers):
                print(GREEN + '{} is correct'.format(filename) + ENDC, file=sys.stderr)
                score += 33

            else:
                score += interactive_grade(filename, correct_answer, output_str, number_extracted)
        else:
            if not filename.endswith('/'):
                print(RED + 'Submitted assignment {} does not end with "py"'.format(filename) + ENDC, file=sys.stderr)

    if score >= 99:
        print(100, file=sys.stdout)
    else:
        print(score, file=sys.stdout)

main()
