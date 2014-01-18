"""
grade_functions.py

Put all individual assignment grading functions here.

"""

import zipfile
import os
import shutil

IMAGE_EXT = {'gif', 'jpg', 'png'}

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
                if not any(ext in extensions for ext in IMAGE_EXT):
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

        failed_dir = 'failed_' + submission_dir.split('/')[-1]
        if not os.path.exists(failed_dir):
            os.mkdir(failed_dir)
        for submission in submissions:
            shutil.copy(os.path.join(submission_dir, submission), failed_dir)

        print('Autgrader gave grade: 50.\nFeel free to edit in the csv before submitting')
        return 50

    return 100

def grade_recitation_1(submission_dir, submissions):
    return 100
