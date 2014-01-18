"""
grade.py - A tool for autograding with moodle

Note, each assignment will need is own GRADE_FUNCTION. Write a function for
grading that particular assignnment and set the value of GRADE_FUNCTION to
that function's name.

To Use:
- Go to moodle and export grades for the assignment you want and your group
    (these will be empty to start unless you have already done some grading)
- Download all of the submissions for this assignment from moodle
- Run python grade.py [directory with submissions] [grade export csv]
- The grade export csv has been overwritten with the grades from the submissions

"""

import os
import sys
import grade_functions

CU_CSV_FOLDER = 'mycuinfo_csvs'

GRADE_FUNCTION = grade_functions.grade_assign_1

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
    if len(sys.argv) == 3:
        submission_dir = sys.argv[1]
        moodle_grade_csv = sys.argv[2]
    else:
        print('Error! Wrong number of arguments')

    names = get_moodle_students(moodle_grade_csv)
    submissions = get_submissions(submission_dir, names)
    grades = grade_assignment(submission_dir, submissions, GRADE_FUNCTION)
    generate_grade_csv(grades, moodle_grade_csv)
    print('All failed submissions have been copies to directory "Failed_Submissions"')
