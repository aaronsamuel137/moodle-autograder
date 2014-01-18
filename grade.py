"""
grade.py - A tool for autograding with moodle

Note, each assignment will need is own GRADE_FUNCTION. Write a function for
grading that particular assignnment and set the value of GRADE_FUNCTION to
that function's name.

"""

import os
import sys
import shutil
import zipfile
import grade_functions
from os.path import expanduser

COURSE_NAME = 'CSCI1300-S14-Hoenigman'
# GRADE_FUNCTION = grade_functions.grade_assign_1
GRADE_FUNCTION = grade_functions.grade_recitation_1

def get_moodle_students(filename):
    """
    Returns a list of moodle student names. The argument filename is a grade export of
    your grading group downloaded from moodle as a csv.

    """
    lines = open(filename).readlines()
    names = []
    for line in lines[1:]:
        fields = line.split(',')
        firstname = fields[0].replace('"', '').strip()
        lastname = fields[1].replace('"', '').strip()
        name = "{} {}".format(firstname, lastname)
        names.append(name)
    return names

def get_submissions(submission_dir, names):
    """
    Returns a dict where keys are moodle student names and values are a list
    containing all the submissions of the student.

    """
    submission_names = {}
    for filename in os.listdir(submission_dir):
        name = filename.split('_')[0]
        if name in names:
            if name in submission_names:
                submission_names[name].append(filename)
            else:
                submission_names[name] = [filename]

    print('NAMES NOT FOUND\n' + ('_' * 15))
    name_set = set(submission_names.keys())
    for name in names:
        if name not in name_set:
            print(name)

    print("\n{} names found in moodle csv".format(len(names)))
    print("{} names found in submissions download\n".format(len(submission_names)))

    return submission_names

def grade_assignment(submission_dir, submission_names, grade_function):
    """
    Returns a dict where keys are the student moodle name and values are the
    student's grade.

    """
    grades = {}
    for name, submissions in submission_names.items():
        grades[name] = grade_function(submission_dir, submissions)
    return grades

def copy_files_from_downloads(assignment_name):
    home = expanduser('~')
    downloads = os.path.join(home, 'Downloads')
    for filename in os.listdir(downloads):
        if COURSE_NAME in filename:
            if 'submit' in filename.lower():
                if not os.path.exists(assignment_name + '_submissions'):
                    os.mkdir(assignment_name + '_submissions')
                try:
                    submission_dir = os.path.join(os.getcwd(), assignment_name + '_submissions')
                    shutil.copy(os.path.join(downloads, filename), submission_dir)
                    zipfile.ZipFile(os.path.join(submission_dir, filename)).extractall(submission_dir)
                except Exception as e:
                    print('Error copying zip archive: {}'.format(e))

            else:
                if not os.path.exists(assignment_name + '_csv'):
                    os.mkdir(assignment_name + '_csv')
                try:
                    grade_csv_dir = os.path.join(os.getcwd(), assignment_name + '_csv')
                    shutil.copy(os.path.join(downloads, filename), grade_csv_dir)
                    grade_csv = os.path.join(grade_csv_dir, filename)
                except Exception as e:
                    print('Error copying csv file: {}'.format(e))

    return submission_dir, grade_csv

def generate_grade_csv(grades, moodle_grade_csv):
    lines = open(moodle_grade_csv).readlines()

    with open(moodle_grade_csv, 'w') as f:
        f.write(lines[0])
        for line in lines[1:]:
            fields = line.split(',')
            firstname = fields[0].replace('"', '').strip()
            lastname = fields[1].replace('"', '').strip()
            name = "{} {}".format(firstname, lastname)
            if name in grades:
                line = line.replace('-', str(grades[name]))
            else:
                line = line.replace('-', '0')
            f.write(line)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        assignment_name = sys.argv[1]
        submission_dir, moodle_grade_csv = copy_files_from_downloads(assignment_name)
    elif len(sys.argv) == 3:
        submission_dir = sys.argv[1]
        moodle_grade_csv = sys.argv[2]
    else:
        print('Error! Wrong number of arguments')

    names = get_moodle_students(moodle_grade_csv)
    submissions = get_submissions(submission_dir, names)
    grades = grade_assignment(submission_dir, submissions, GRADE_FUNCTION)
    generate_grade_csv(grades, moodle_grade_csv)

    failed_dir = 'failed_' + submission_dir.split('/')[-1]
    print('All failed submissions have been copies to directory "{}"'.format(failed_dir))
