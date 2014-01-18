moodle-autograder
=================

Autograding tools for courses run with Moodle

setup
=====

Clone the repository.

There are two files. grade.py is the main wrapper that reads and writes the csvs.
grade_functions.py is where individual functions for grading each assignment live.
Right now, there is only a function for assignment 1 grading, but more can be added
as the semester goes on. In the future, you will need to manually edit grade.py to make
sure it is calling the correct grading function.

Usage
=====

- Go to moodle and export grades for the assignment you want.
To do this, go to Grade administration -> Export -> Plain text file. Then select your
grade group under the "Visible groups" drop down. Then go to the bottom and click
"Select all/none" to unselect all assignments. Then you can easily select the assignment
be graded now. This will download a csv of all student names with an empty field ready for
grades.
- Download all of the submissions for this assignment from moodle.
- Run the following:

```
python grade.py [directory with submissions] [grade export csv]
```

- The grade export csv has been overwritten with the grades from the submissions
- Go to moodle and select import csv. Import the modified csv. Be sure to change 
the dropdowns "Map to" and "Map from" under "Identify user by" to say "Email address".
Also change change to the grade field to map to the correct assignment.
