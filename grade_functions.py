"""
grade_functions.py

Put all individual assignment grading functions here.

"""

import zipfile
import os
import shutil

def get_extension(filename):
    return filename[filename.rfind('.')+1:]

def grade_assign_1(submission_dir, submissions):
    extensions = set()
    files = []
    reasons = []

    failed = True
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
                    files.append(filename)
                if 'py' not in extensions:
                    reasons.append('Missing py file')
                if 'png' not in extensions and 'jpg' not in extensions:
                    reasons.append('Missing image file')
                if len(reasons) == 0:
                    failed = False
            except Exception as e:
                reasons.append('Invalid zip file')
    if failed:
        message = 'Autograder failed for student {}'.format(submissions[0].split('_')[0])
        print('{}\n{}'.format(message, '-' * len(message)))
        print('\tStudent submitted the following files:')
        for f in files:
            print('\t\t{}'.format(f))
        print('\n\tReason(s) for failure:')
        for reason in reasons:
            print('\t\t{}'.format(reason))
        print('\n\n\n')

        try:
            os.mkdir('Failed_Submissions')
        except OSError:
            pass
        for submission in submissions:
            shutil.copy(os.path.join(submission_dir, submission), 'Failed_Submissions')

    return 100