"""
grade_functions.py

Put all individual assignment grading functions here.

"""

import zipfile
import os
import shutil
import sys
import re
from io import StringIO

# constants for printing colors to the terminal
PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

IMAGE_EXT = {'gif', 'jpg', 'png'}

def check_submission_format(submission_dir, submissions):
    errors = []
    non_zip_submissions = []
    archive = None
    student = None

    for submission in submissions:
        if submission.endswith('zip'):
            try:
                student = submission.split('_')[0]
                archive = zipfile.ZipFile(os.path.join(submission_dir, submission))
            except Exception as e:
                errors.append('Invalid zip file')
        else:
            non_zip_submissions.append(submission)
            errors.append('Unzipped submission: {}'.format(submission))
    return archive, student, non_zip_submissions, errors

def exec_archived_files(archive):
    for filename in archive.namelist():
        contents = archive.read(filename)
        yield filename, get_code_output(contents)

def get_code_output(code):
    buff = StringIO()
    sys.stdout = buff
    try:
        exec(code)
    except:
        # this exception will not be caught if the code be executed throws an exception
        pass
    sys.stdout = sys.__stdout__
    return buff.getvalue()

def close_to(a, b):
    if a > 10000:
        correct_range = 2
    else:
        correct_range = 0.5
    return abs(a - b) < correct_range

def get_extension(filename):
    return filename[filename.rfind('.')+1:]

def move_to_failed_dir(submission_dir, submissions):
    failed_dir = 'failed_' + submission_dir.split('/')[-1]
    if not os.path.exists(failed_dir):
        os.mkdir(failed_dir)
    for submission in submissions:
        shutil.copy(os.path.join(submission_dir, submission), failed_dir)

def grade_assign_1(submission_dir, submissions):
    extensions = set()
    files = []
    reasons = []

    for submission in submissions:
        extensions.add(get_extension(submission))
        files.append(submission)

        if not submission.endswith('zip'):
            reasons.append('Unzipped Submission')
        else:
            try:
                archive = zipfile.ZipFile(os.path.join(submission_dir, submission))
                names = archive.namelist()
                for filename in names:
                    extensions.add(get_extension(filename))
                    files.append('\t' + filename)

            except Exception as e:
                reasons.append('Invalid zip file')

    if 'py' not in extensions:
        reasons.append('Missing py file')
    if not any(ext in extensions for ext in IMAGE_EXT):
        reasons.append('Missing image file')

    if len(reasons) > 0: # Did not get full credit from autograder
        message = 'Autograder output for student {}'.format(submissions[0].split('_')[0])
        print(RED + '{}\n{}'.format(message, '-' * len(message)) + ENDC)
        print('\tStudent submitted the following files:')
        for f in files:
            print(BLUE + '\t\t{}'.format(f) + ENDC)
        print('\n\tReason(s) for failure:')
        for reason in reasons:
            print(BLUE + '\t\t{}'.format(reason) + ENDC)

        move_to_failed_dir(submission_dir, submissions)
        print('\n')

    return 100

def grade_recitation_1(submission_dir, submissions):
    return 100

def grade_assign_2(submission_dir, submissions):
    answers = [6250, 310338195, 2.8]
    score = 0
    archive, student, non_zip_submissions, errors = check_submission_format(submission_dir, submissions)
    print(YELLOW + 'Evaluating submissions for {}'.format(student) + ENDC)

    if archive:
        for filename in archive.namelist():
            if filename.endswith('py'):
                if '/' in filename:
                    name = filename.split('/')[-1]
                else:
                    name = filename

                contents = archive.read(filename)
                output = get_code_output(contents)
                output_match = re.search(r'[0-9.]+', output)
                problem_match = re.search(r'[0-9]+', name)

                if problem_match:
                    try:
                        correct_answer = answers[int(problem_match.group(0))-1]
                    except:
                        correct_answer = 'Problem not identifiable by filename, answer is one of {}'.format(str(answers))
                else:
                    correct_answer = 'Problem not identifiable by filename, answer is one of {}'.format(str(answers))

                number = None
                if output_match:
                    number = round(float(output_match.group(0)), 1)
                    if any(close_to(answer, number) for answer in answers):
                        print(GREEN + '{} is correct'.format(filename) + ENDC)
                        score += 33
                else:
                    print(RED + 'Correct answer not found for {}. Printing code for evaluation:\n'.format(filename) + ENDC)
                    print(contents.decode('utf-8').strip())
                    print('\noutput: {}'.format(output.strip()))
                    if number is not None:
                        print('number extracted: {}'.format(number))
                    print('correct answer: {}'.format(correct_answer))
                    s = input('\nEnter grade: ')
                    score += int(s)
            else:
                if not filename.endswith('/'):
                    print(RED + 'Submitted assignment {} does not end with "py"'.format(filename) + ENDC)
                    # print(archive.read(filename))

        if score >= 99:
            return 100
        else:
            move_to_failed_dir(submission_dir, submissions)
            return score
    else:
        # for submission in non_zip_submissions:
        #     if submission.endswith('py'):
        #         contents = open(os.path.join(submission_dir, submission)).read()
        #         output = get_code_output(contents)
        move_to_failed_dir(submission_dir, submissions)
        print(RED + 'No zipfile found for {}'.format(student) + ENDC)
        return 0
