"""
grade_recitation.py - Grades a moodle assignment as 100 if there is a submission,
    or 0 otherwise

Usage
=====
1. Go to moodle and export grades for the assignment you want.
To do this, go to Grade administration -> Export -> Plain text file. Then select your
grade group under the "Visible groups" drop down. Then go to the bottom and click
"Select all/none" to unselect all assignments. Then select the single assignment to
be graded now. This will download a csv of all student names with an empty field ready for
grades.
2. Download all of the submissions for this assignment from moodle and unzip.
3. Run python grade.py [directory with submissions] [grade export csv]

  The autograder will first print a list of all the students it couldn't find submissions
for who are registered on moodle.

4. There will be a new file output.csv with the grades.
5. Go to moodle and select import csv. Import the output csv. Be sure to change
the dropdowns "Map to" and "Map from" under "Identify user by" to say "Email address".
Also change to the grade field to map to the correct assignment.

Example Usage
=============

python3 grade_recitation.py ~/Downloads/CSCI1300-S14-Hoenigman-Recitation\ 11\ submit--9850 ~/Downloads/CSCI1300-S14-Hoenigman\ Grades-20140411_2049-comma_separated.csv

"""

import os
import sys
import shutil
import zipfile

COURSE_NAME = 'CSCI1300-S14-Hoenigman'

# constants for printing colors
GREEN = '\033[92m'
ENDC = '\033[0m'

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

def grade_assignment(submission_dir, submission_names):
    """
    Returns a dict where keys are the student moodle name and values are the
    student's grade.

    """
    grades = {}
    for name, submissions in submission_names.items():
        grades[name] = 100
    return grades

def generate_grade_csv(grades, moodle_grade_csv):
    """
    Writes over the moodle_grade_csv file with the grades added in place of the old grade.

    """
    lines = open(moodle_grade_csv).readlines()

    with open('output.csv', 'w') as f:
        f.write(lines[0])
        for line in lines[1:]:
            fields = line.split(',')
            firstname = fields[0].replace('"', '').replace("'", '').strip()
            lastname = fields[1].replace('"', '').replace("'", '').strip()
            name = "{} {}".format(firstname, lastname)
            fields.pop()
            if name in grades:
                fields.append(str(grades[name]))
            else:
                fields.append('0')
            line = ','.join(fields) + '\n'
            f.write(line)

if __name__ == '__main__':

    if len(sys.argv) == 3:
        submission_dir = sys.argv[1]
        moodle_grade_csv = sys.argv[2]
    else:
        print('Error! Wrong number of arguments')

    names = get_moodle_students(moodle_grade_csv)
    submissions, not_found = get_submissions(submission_dir, names)
    grades = grade_assignment(submission_dir, submissions)
    generate_grade_csv(grades, moodle_grade_csv)

    print('\nNAMES NOT GRADED\n' + ('_' * 15))
    for name in not_found:
        print(name)
