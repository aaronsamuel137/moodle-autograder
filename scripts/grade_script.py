import sys
import os

# constants for printing colors to the terminal
PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

def interactive_grade(filename, correct_answer, output_str, number):
    print(RED + 'Correct answer not found for {}. Printing code for evaluation:\n'.format(filename) + ENDC, file=sys.stderr)
    print(BLUE, '-' * 30, '\n', open(filename).read().strip(), '\n', '-' * 30, ENDC, file=sys.stderr)
    print('output:\n{}'.format(output_str), file=sys.stderr)
    if number is not None:
        print('number extracted: {}'.format(number), file=sys.stderr)
    print('correct answer: {}'.format(correct_answer), file=sys.stderr)
    print('\nEnter grade: ', file=sys.stderr)
    s = input()
    return int(s)

def print_eval_name():
    student_name = os.getcwd().split('/')[-1]
    print(YELLOW + 'Evaluating submissions for {}'.format(student_name) + ENDC, file=sys.stderr)

def print_eval_problem(filename):
    print(PURPLE + 'Evaluating submission {}'.format(filename) + ENDC, file=sys.stderr)
