"""
Linguist 278: Programming for Linguists
Stanford Linguistics, Fall 2020
Christopher Potts

Assignment 1

Distributed 2020-09-14
Due 2020-09-28

NOTES:

Please submit a modified version of this file, including all the
comments it currently contains.

Your file should not execute any functions when imported as a module
-- all function calls must be placed in the scope of
`if __name__ == '__main__'` at the bottom of this file.

Please name the file ling278_assign01_NAME.py

where NAME is a version of your name containing only letters and/or
underscores. (This will allow me to import your file as a Python
module; more about that later.)

"""
import math
import pprint


"""===================================================================
1   [1 point]

Complete the function `mean` for calculating the mean (average) of a
list of numeric values. Your function should take a list vals as its
argument and return a float.

In class, we wrote this with a for-loop. Consider doing it instead with
the in-line function `sum`, which facilitates a fast and readable
one-line version of the function.
"""

def mean(vals):
    """Return the mean of the values in vals, presupposed to be
    numeric (float or int)."""

    total = 0.0

    for val in vals:
        total += val

    return total / float(len(vals))


"""===================================================================
2   [1 point]

Complete the function `sd` for calculating the standard deviation of a
list of numeric values. Your function should take a list of ints or
floats as its value and return a float.

For details on calculating the standard deviation, see
http://en.wikipedia.org/wiki/Standard_deviation

I suggest using `len(vals)-1` for the denominator, but `len(vals)` is
fine. (An optional, advanced approach is to have an optional function
argument `sd_corr=1` that puts this correction under the user's
control, but don't worry about this if you don't already know about
optional arguments.)

To get the square root of a float `x`, use

import math

math.sqrt(x)
"""


def sd(vals, sd_corr=1):
    """Return the standard deviation of the values in vals,
    presupposed to be numeric (float or int)."""

    if len(vals) < 2:
        return 0

    mu = mean(vals)
    total = 0.0

    for val in vals:
        total += (val - mu)**2

    return math.sqrt(total / float(len(vals)-sd_corr))




"""
===================================================================
3   [1 point]

Complete the function `zscore` for computing the z-score (normal
score) of a list of numeric values. Your function should take a list
of ints or floats as its value and return a list of z-score normed
values. Use `mean` and `sd`, as defined above, for this calculation.

For details on calculating the z-score, see
http://en.wikipedia.org/wiki/Z_score

"""

def zscore(vals):
    """Return the z-scored version of vals."""
    mu = mean(vals)
    std = std(vals)
    zscores = []

    for val in vals:
        zscores.append((val - mu) / std)

    return zscores




"""===================================================================
4   [2 points]

Complete the function `palindrome_detector` for identifying
palindromes (words that are the same forward and backwards). Your
function should be case-insensitive (e.g., 'Wow' should count as a
palindrome) and it should ignore spaces (e.g., 'race car' is a
palindrome).

To test your function, call `palindrome_detector_test`, which will work
with no modifications.
"""

def palindrome_detector(s):
    """The input is any str s. The return value is True if s is a
    palindrome, else False."""

    cleaned = s.lower().replace(' ', '')
    return s == "".join(reversed(cleaned))

def palindrome_detector_test():
    """Simple unit test for palindrome_detector."""
    sample = (
        ('deleveled', True),
        ('Malayalam', True),
        ('detartrated', True),
        ('a', True),
        ('repaper', True),
        ('Al lets Della call Ed Stella', True),
        ('Lisa Bonet ate no basil', True),
        ('Linguistics', False),
        ('Python', False),
        ('palindrome', False),
        ('an', False),
        ('re-paper', False)
        )
    for s, val in sample:
        try:
            assert palindrome_detector(s) == val
        except AssertionError:
            print('palindrome_detector in error for {}'.format(s))


"""===================================================================
5

Intro to comma-separated values. The string `myspreadsheet` stores 11
lines of comma-separated values, with the first line giving the column
names and the other lines giving the data on 10 imaginary subjects.
Below are some questions that ask you to write functions for working
with this data.
"""

myspreadsheet ="""Subject,Height,Occupation
1,74.37000326528938,Psychologist
2,67.49686206937491,Psychologist
3,74.92356434760966,Psychologist
4,64.62372198999978,Psychologist
5,67.76787900026083,Linguist
6,61.50397707923559,Psychologist
7,62.73680961908566,Psychologist
8,68.60803984763902,Linguist
9,70.16090500135535,Psychologist
10,76.81144438287173,Linguist"""

"""--------------------------------------------------
Random facts: The column of heights, presumably in
inches, was generated with

import random

and then repeated runs of

random.uniform(60,77)

The column of occupations was generated with

d = {0:'Psychologist',1:'Linguist'}

and then repeated runs of

d[random.randint(0,1)]
--------------------------------------------------"""


"""===================================================================
5.1  [3 points]

Basic CSV parser. Complete the following function for turning the str
myspreadsheet into a 10x3 matrix of data.  I should emphasize that the
top line of myspreadsheet is not part of the data.  It's just there to
help us out.

Column 0 of your data should be int values.

Column 1 of your data should be float values.

To test your parser, call `csv_parser_test`, which will work with
no modifications.
"""

def csv_parser(s):
    """Parses the str `s` into lines, and then parses those lines by
    splitting on the comma and converting the numerical data to int.
    The output is a list of lists of subject data."""

    # Data is our output. It will be a list of lists.
    data = []

    # Split csv into lines and store them in a list called 'lines'.
    lines = s.splitlines()

    # Remove the first element from lines, so that you have only the
    # data lines left.
    lines.pop(0)

    # At this stage, we loop through the list called lines.
    # As you loop
    #     i. split each line on the commas;
    #    ii. convert the Subject variable to int.
    #   iii. convert the Height variable to float.
    #    iv. add to data a list consisting of this line's Subject,
    #        Height, and Occupation values
    for line in lines:
        subject = int(line.split(',')[0])
        height = float(line.split(',')[1])
        occupation = line.split(',')[2]
        data.append([subject, height, occupation])

    return data

def csv_parser_test():
    """Display the output of `csv_parser(myspreadsheet)` and
    test it a little bit."""
    data = csv_parser(myspreadsheet)
    err_count = 0
    # Did your parser work?
    for row_num, row in enumerate(data):
        try:
            assert len(row) == 3
        except AssertionError:
            print("Row {} seems to be misparsed; its length is {}".format(
                row_num, len(row)))
            err_count += 1
    # Check on one of the values:
    try:
        assert data[4][2] == 'Linguist'
    except AssertionError:
        print("Error: data[4][2] should equal 'Linguist'; actual value is {}".format(
            data[4][2]))
        err_count += 1
    # Did you remember your int conversions?
    try:
        assert isinstance(data[0][0], int)
    except AssertionError:
        print("Error: data[0][0] should be an int")
        err_count += 1
    # Did you remember your float conversions?
    try:
        assert isinstance(data[6][1], float)
    except AssertionError:
        print("Error: data[6][1] should be a float")
        err_count += 1
    print("{} errors for csv_parser".format(err_count))
    # A look at your data structure:
    if err_count > 0:
        print('Your data object:')
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)


"""===================================================================
5.2  [1 point]

Complete the following function for computing the mean height of the
subjects in this data set, using your `mean` function from above.
"""

import numpy as np

def mean_height(data):
    """Return the mean numerical value of column 1 in an list of lists.
    data is the output of csv_parser(myspreadsheet)"""

    total = 0.0

    for row in data:
        total += float(row[1])

    length = np.array(data).shape[0]

    return total / length


"""===================================================================
5.3  [1 point]

Occupation distribution. Complete the following function so that it
returns a dict mapping occupation names into the number of times
they occur in the data.
"""

from collections import defaultdict

def occupation_distribution(data):
    """Returns the dict of occupations given in column 2 of `data`
    mapped to the number of times they occur. `data` is the output
    `of csv_parser(myspreadsheet)`."""

    job_dict = defaultdict(int)

    for row in data:
        job_dict[row[2]] +=1

    return job_dict



"""===================================================================
Place all function calls below the following conditional so that they
are called only if this module is called with

`python ling278_assign01.py`

No functions should execute if it is instead imported with

import ling278_assign01

in the interactive shell.
"""
if __name__ == '__main__':
    palindrome_detector_test()
    csv_parser_test()
    data = csv_parser(myspreadsheet)
    print(mean_height(data))
    data = csv_parser(myspreadsheet)
    print(occupation_distribution(data))
