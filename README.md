moodle-autograder
=================
Autograding tools for courses that run with Moodle

Setup
=====
Clone the repository. It has been tested on OSX, and will most likely work fine
on the VM. Not tested in Windows.

Usage
=====
1. Go to moodle and export grades for the assignment you want.
To do this, go to Grade administration -> Export -> Plain text file. Then select your
grade group under the "Visible groups" drop down. Then go to the bottom and click
"Select all/none" to unselect all assignments. Then select the single assignment to
be graded now. This will download a csv of all student names with an empty field ready for
grades.
2. Download all of the submissions for this assignment from moodle (keep as zip archive).
3. Download the grading script from moodle (as zip archive)
4. Put all of these downloads in the autograder directory
5. Run the autograder (as specified under "Running the Autograder").
6. There should be a new directory called [assignment_name]_csv where the grade csv is.
Grades will be either 100 or 0.
7. You can add a new column for feedback if you'd like.
8. Go to moodle and select import csv. Import the modified csv. Be sure to change
the dropdowns "Map to" and "Map from" under "Identify user by" to say "Email address".
Also change to the grade field to map to the correct assignment. If you added a
feedback column, make sure it is set to map to the feedback for the assignment you
are grading.

Running the Autograder
======================
Run the following command:

```
python3 grade.py [assignment name] [grade export csv] [submission zip file] [grade script zip file]
```

Note that the assignment name argument is arbitrary, it is just used for naming the
folders that the submissions and output csv are stored in. It is recommended that
you enter something reasonable, such as "assignment6".

####Example:

```
python3 grade.py assignment6 CSCI1300-S14-Hoenigman\ Grades-20140221_2321-comma_separated.csv CSCI1300-S14-Hoenigman-Assignment\ 6\ Submit-8120.zip Assignment6_Tester.zip
```
