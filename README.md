moodle-autograder
=================
Autograding tools for courses run with Moodle

Usage
=====
1. Go to moodle and export grades for the assignment you want.
To do this, go to Grade administration -> Export -> Plain text file. Then select your
grade group under the "Visible groups" drop down. Then go to the bottom and click
"Select all/none" to unselect all assignments. Then select the single assignment to
be graded now. This will download a csv of all student names with an empty field ready for
grades.
2. Download all of the submissions for this assignment from moodle and unzip.
3. Run python3 grade_recitation.py [directory with submissions] [grade export csv]

  The autograder will first print a list of all the students it couldn't find submissions
for who are registered on moodle.

4. There will be a new file output.csv with the grades.
5. Go to moodle and select import csv. Import the output csv. Be sure to change
the dropdowns "Map to" and "Map from" under "Identify user by" to say "Email address".
Also change to the grade field to map to the correct assignment.
