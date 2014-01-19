moodle-autograder
=================
Autograding tools for courses run with Moodle

Setup
=====
Clone the repository.

There are two files:
- grade.py is the main wrapper that reads and writes the csvs
- grade_functions.py is where individual functions for grading each assignment live


Usage
=====
1. Go to moodle and export grades for the assignment you want.
To do this, go to Grade administration -> Export -> Plain text file. Then select your
grade group under the "Visible groups" drop down. Then go to the bottom and click
"Select all/none" to unselect all assignments. Then you can easily select the assignment
be graded now. This will download a csv of all student names with an empty field ready for
grades.
2. Download all of the submissions for this assignment from moodle.
3. Run the autograder in one of the two ways specified below.

  The autograder will first print a list of all the students it couldn't find submissions
for who are registered on moodle.

  Then it will print out some info for every student who doesn't get full credit. All non full credit submissions will be copied to a new directory for easy browsing.
4. The grade export csv has been overwritten with the grades from the submissions. Manually
overwrite any grades that the autograder did not correctly output.
5. Go to moodle and select import csv. Import the modified csv. Be sure to change
the dropdowns "Map to" and "Map from" under "Identify user by" to say "Email address".
Also change to the grade field to map to the correct assignment.

Running the Autograder
======================
To run the autograder, you will need to specify which assignment you are wanting to grade.
To run it for assignment 1, give the commandline argument "assign_1". For recitation 1,
use "recitation_1".

There are two ways of running the autograder.

- Manually telling the autograder where the assignemnt submissions and the exported
grade csv are. To do this, run the following:

```
python grade.py [assignment name] [directory with submissions] [grade export csv]
```

- Alternatively, you can just leave the unextracted submissions zip and the grades
csv in your Downloads folder and run:

```
python grade.py [assignment name]
```

The program will automatically copy the files from the Downloads folder and organize
them inside of the moodle-autograder directory. Make sure that these are the only two
files in the Downloads folder with the prefix "CSCI1300-S14-Hoenigman"
