"""
grade.py - A tool for autograding with moodle

"""

import os
import threading
import stat
import sys
import shutil
import zipfile
import subprocess
import signal
import argparse

from subprocess import Popen, PIPE

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

ORIG_DIR = os.getcwd()
TMP = 'autograder_tmpdir'

# make ctrl-c work incase student code goes into infinite loop
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

def grade_assignment(submission_dir, submission_names, grader_zip):
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
                    subprocess.check_call(['unzip', '-d', name, grader_zip])

                except Exception as err:
                    print('Error unzipping files:', err)

                try:
                    os.chdir(name)
                    grade_dir_stem = grader_zip.split('.')[0].split('/')[-1]

                    for filename in os.listdir(grade_dir_stem):
                        shutil.move('/'.join([grade_dir_stem, filename]), os.getcwd())

                    grade_script = os.path.join(os.getcwd(), 'Grading_Script.py')
                    st = os.stat(grade_script)
                    os.chmod(grade_script, st.st_mode | stat.S_IEXEC)

                    cmd = grade_script
                    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = p.communicate()
                    output = stderr.decode().strip()
                    if '100' in output:
                        grades[name] = 100
                    else:
                        grades[name] = 0
                    print(GREEN, '\nOUTPUT\n------\n{}\n------\n'.format(output), ENDC)
                    print('GRADE:', grades[name])

                except Exception as err:
                    print('Error running script', err)

                os.chdir(tmp_dir)
            else:
                print('Got non-zip submission:', s)

    os.chdir(original_dir)
    shutil.rmtree(TMP)
    return grades

def extract_submissions(submissions, assignment_name):
    """
    Extract submissions from zip file into directory [assignment_name]_submissions.

    """
    if not os.path.exists(assignment_name + '_submissions'):
        os.mkdir(assignment_name + '_submissions')
    try:
        submission_dir = os.path.join(os.getcwd(), assignment_name + '_submissions')
        zipfile.ZipFile(submissions).extractall(submission_dir)
    except Exception as e:
        print('Error copying zip archive: {}'.format(e))

    return submission_dir

def generate_grade_csv(grades, moodle_grade_csv, assignment_name):
    """
    Writes a new csv file for submitting to moodle in directory [assignment_name]_csv.

    """
    if not os.path.exists(assignment_name + '_csv'):
        os.mkdir(assignment_name + '_csv')
    csv_dir = os.path.join(os.getcwd(), assignment_name + '_csv')

    shutil.copy(moodle_grade_csv, csv_dir)
    csv_copy = os.path.join(csv_dir, moodle_grade_csv)

    lines = open(moodle_grade_csv).readlines()

    with open(csv_copy, 'w') as f:
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

def main():
    # Setup Argument Parsing
    parser = argparse.ArgumentParser(description='Grade Moodle Submissions')
    parser.add_argument('assignment_name', type=str,
                       help='name of assignment')
    parser.add_argument('moodle_csv', type=str,
                       help='CSV file downloaded from moodle')
    parser.add_argument('submissions', type=str,
                       help='Zip file of all submissions')
    parser.add_argument('grading_script', type=str,
                       help='Submssion grading script')

    # Parse Arguments
    args = parser.parse_args(sys.argv[1:])
    assignment_name = args.assignment_name
    moodle_grade_csv = args.moodle_csv
    submission_dir = extract_submissions(args.submissions, assignment_name)
    grade_script = os.path.abspath(args.grading_script)

    # Get student names from csv
    names = get_moodle_students(moodle_grade_csv)

    # get submissions from students
    submissions, not_found = get_submissions(submission_dir, names)

    # run grade script
    grades = grade_assignment(submission_dir, submissions, grade_script)

    # output grades into csv
    generate_grade_csv(grades, moodle_grade_csv, assignment_name)

    # failed_dir = 'failed_' + submission_dir.split('/')[-1]

    print(RED + '\nNAMES NOT FOUND\n' + ('_' * 15))
    for name in not_found:
        print(name)
    print(ENDC)

    # print(GREEN + '\nAll failed submissions have been copied to directory "{}"'.format(failed_dir) + ENDC)

if __name__ == '__main__':
    main()
