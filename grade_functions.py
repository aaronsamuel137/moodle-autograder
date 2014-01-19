"""
grade_functions.py

Put all individual assignment grading functions here.

"""

import zipfile
import os
import shutil

# constants for printing colors to the terminal
PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

IMAGE_EXT = {'gif', 'jpg', 'png'}

def get_extension(filename):
    return filename[filename.rfind('.')+1:]

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

        failed_dir = 'failed_' + submission_dir.split('/')[-1]
        if not os.path.exists(failed_dir):
            os.mkdir(failed_dir)
        for submission in submissions:
            shutil.copy(os.path.join(submission_dir, submission), failed_dir)
        print('\n')

    return 100

def grade_recitation_1(submission_dir, submissions):
    return 100
