moodle-autograder
=================

Autograding tools for courses run with Moodle

Setup
=====

Clone the repository.

There are two files. grade.py is the main wrapper that reads and writes the csvs.
grade_functions.py is where individual functions for grading each assignment live.


Usage
=====

- Go to moodle and export grades for the assignment you want.
To do this, go to Grade administration -> Export -> Plain text file. Then select your
grade group under the "Visible groups" drop down. Then go to the bottom and click
"Select all/none" to unselect all assignments. Then you can easily select the assignment
be graded now. This will download a csv of all student names with an empty field ready for
grades.
- Download all of the submissions for this assignment from moodle.
- There are two ways of running the autograder.

1. Running by manually telling the autograder where the submissions and the exported
grade csv are. To do this, run the following:

```
python grade.py [assignment name] [directory with submissions] [grade export csv]
```

where [assignment name] is either assign_[number] or recitation_[number]

2. Alternatively, you can just leave the unextracted submissions zip and the grades
csv in your Downloads folder and run:

```
python grade.py [assignment name]
```

The program will automatically copy the files from the Downloads folder and organize
them inside of the moodle-autograder directory.

- Now the grade export csv has been overwritten with the grades from the submissions
- Go to moodle and select import csv. Import the modified csv. Be sure to change
the dropdowns "Map to" and "Map from" under "Identify user by" to say "Email address".
Also change change to the grade field to map to the correct assignment.
