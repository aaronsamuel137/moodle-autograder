"""
grade.py - A tool for autograding with moodle

Each assignment gets it own function for grading in grade_functions.py.
To add a new assignment, add the function to grade_functions.py and then
put a reference to it in the global ASSIGNMENTS dictionary.

"""

import os
import sys
import shutil
import zipfile
import grade_functions
import subprocess
import signal
from os.path import expanduser

COURSE_NAME = 'CSCI1300-S14-Hoenigman'

# constants for printing colors
GREEN = '\033[92m'
ENDC = '\033[0m'

ORIG_DIR = os.getcwd()
TMP = 'autograder_tmpdir'

def signal_handler(signal, frame):
    tmp_dir = '/'.join([ORIG_DIR, TMP])
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_moodle_students(filename):
    """
    Returns a list of moodle student names. The argument filename is a grade export of
    your grading group downloaded from moodle as a csv.

    """
    lines = open(filename).readlines()
    names = []
    for line in lines[1:]:
        fields = line.split(',')
        firstname = fields[0].replace('"', '').replace("'", '').strip()
        lastname = fields[1].replace('"', '').replace("'", '').strip()
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

    submissions_not_found = []
    name_set = set(submission_names.keys())
    for name in names:
        if name not in name_set:
            submissions_not_found.append(name)

    return submission_names, submissions_not_found

def grade_assignment(submission_dir, submission_names, grade_script):
    """
    Returns a dict where keys are the student moodle name and values are the
    student's grade.

    """
    grades = {}
    original_dir = os.path.abspath(os.getcwd())

    try:
        os.mkdir(TMP)
    except:
        shutil.rmtree(TMP)
        os.mkdir(TMP)

    os.chdir(TMP)
    tmp_dir = os.path.abspath(os.getcwd())

    for name, submissions in submission_names.items():
        student_dir = os.mkdir(name)
        for s in submissions:
            if s.endswith('.zip'):
                try:
                    subprocess.check_call(['unzip', '-d', name, os.path.join(submission_dir, s)])
                except Exception as err:
                    print('Error unzipping files:', err)

                try:
                    os.chdir(name)
                    output = subprocess.check_output([grade_script])
                    output_str = output.decode().strip()
                    # grade = output_str.split('\n')[-1]
                    print('GRADE:', output_str)
                except Exception as err:
                    print('Error running script', err)
                os.chdir(tmp_dir)
            else:
                print('Got non-zip submission:', s)

    os.chdir(original_dir)
    shutil.rmtree(TMP)
    return grades

def copy_files_from_downloads(assignment_name):
    """
    Copies the zip archive of submissions and grade csv from moodle into the autograder
    directory. Each gets a folder created for it to ensure organization. The zip archive
    is extracted. Returns the names of each of these files.

    """
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
    """
    Writes over the moodle_grade_csv file with the grades added in place of the old grade.

    """
    lines = open(moodle_grade_csv).readlines()

    with open(moodle_grade_csv, 'w') as f:
        f.write(lines[0])
        for line in lines[1:]:
            fields = line.split(',')
            firstname = fields[0].replace('"', '').strip()
            lastname = fields[1].replace('"', '').strip()
            name = "{} {}".format(firstname, lastname)
            fields.pop()
            if name in grades:
                fields.append(str(grades[name]))
            else:
                fields.append('0')
            line = ','.join(fields) + '\n'
            f.write(line)

if __name__ == '__main__':
    # run with one arg: automatically copy files from Downloads
    if len(sys.argv) == 3:
        assignment_name = sys.argv[1]
        grade_script = os.path.abspath(sys.argv[2])
        # grading_function = get_assignment_function(assignment_name)
        submission_dir, moodle_grade_csv = copy_files_from_downloads(assignment_name)

    # run with three args: specify files to use for grading
    elif len(sys.argv) == 4:
        assignment_name = sys.argv[1]
        grading_function = get_assignment_function(assignment_name)
        submission_dir = sys.argv[2]
        moodle_grade_csv = sys.argv[3]
    else:
        print('Error! Wrong number of arguments')

    names = get_moodle_students(moodle_grade_csv)
    submissions, not_found = get_submissions(submission_dir, names)
    grades = grade_assignment(submission_dir, submissions, grade_script)
    generate_grade_csv(grades, moodle_grade_csv)

    failed_dir = 'failed_' + submission_dir.split('/')[-1]

    print('\nNAMES NOT FOUND\n' + ('_' * 15))
    for name in not_found:
        print(name)

    print(GREEN + '\nAll failed submissions have been copied to directory "{}"'.format(failed_dir) + ENDC)
