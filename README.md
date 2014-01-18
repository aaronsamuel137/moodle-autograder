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

- Go to moodle and export grades for the assignment you want and your group
(these will be empty to start unless you have already done some grading)
- Download all of the submissions for this assignment from moodle
- Run the following:

```
python grade.py [directory with submissions] [grade export csv]
```

- The grade export csv has been overwritten with the grades from the submissions
- Go to moodle and select import csv. Import the modified csv.
