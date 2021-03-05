"""
Linguist 278: Programming for Linguists
Stanford Linguistics, Fall 2020
Christopher Potts

Assignment 2

Distributed 2020-09-28
Due 2020-10-05

NOTES:

Please submit a modified version of this file, including all the
comments it currently contains.

Your file should not execute any functions when imported as a module
-- all function calls must be placed in the scope of
`if __name__ == '__main__'` at the bottom of this file.

Please name the file ling278_assign02_NAME.py

where NAME is a version of your name containing only letters and/or
underscores. (This will allow me to import your file as a Python
module; more about that later.)
"""

"""===================================================================
1.  [3 points]

Tokenizing. This is one of the most common (and vexing) operations
when processing text data. There is no single correct way to do it; the
correct method will depend on the task at hand.

This problem is designed to give you a sense for the challenges and the
possibilities, but the design of the tokenizer is scoped very tightly,
as described in the documentation for the function.

If the function `test_simple_tokenize` runs with no errors (i.e., it
gives no output when called), then your tokenizer is correct.
"""

def simple_tokenize(s):
    """Break str `s` into a list of str.

    1. `s` has all of its peripheral whitespace removed.
    1. `s` is downcased with `lower`.
    2. `s` is split on whitespace.
    3. For each token, any peripheral punctuation on it is stripped
       off. Punctuation is here defined by `string.punctuation`.

    Parameters
    ----------
    s : str
        The string to tokenize.

    Returns
    -------
    list of str

    """
    import string

    # This is a str of concatenated punctuation marks:
    punct = string.punctuation

    final_tokens = []

    tokens = s.strip().lower().split()

    for token in tokens:
        final_tokens.append(token.strip(punct))

    return final_tokens

def test_simple_tokenize():
    examples = [
        ["The dog barked.", ["the", "dog", "barked"]],
        ['"Hello?", she said.', ["hello", "she", "said"]],
        ["A non-issue.", ["a", "non-issue"]]]
    err_count = 0
    for x, expected in examples:
        result = simple_tokenize(x)
        if result != expected:
            print('simple_tokenize error for "{}":\n\tGot: {}\n\tExpected: {}'.format(
                x, result, expected))
            err_count += 1
    print("test_simple_tokenize completed with {} errors".format(err_count))


"""===================================================================
2.  [2 points]

Word counts. Write a function that takes as inputs a string `s`,
uses `simple_tokenize` to tokenize it, and returns a dict mapping
each word in `s` to the number of times it appears in `s`.

If `test_count_words_from_string` runs with no errors, then your
function is correct.
"""

def count_words_from_string(s):
    """Count distribution for the words in `s` according to `simple_tokenize`.

    Parameters
    ----------
    s : str
        String to tokenize and get  word counts for.

    Returns
    -------
    dict mapping str to int

    """
    tokenized = simple_tokenize(s)

    count_dict = {}

    for tokens in tokenized:
        count_dict[tokens] = count_dict.get(tokens, 0) + 1

    return count_dict


def test_count_words_from_string():
    examples = [
        ["a a b c", {"a": 2, "b": 1, "c": 1}],
        ["", {}]]
    err_count = 0
    for x, expected in examples:
        result = dict(count_words_from_string(x))
        if result != expected:
            print("count_words_from_string error for {}:\n\tGot: {}\n\tExpected: {}".format(
                x, result, expected))
            err_count += 1
    print("test_count_words_from_string completed with {} errors".format(err_count))


"""===================================================================
3.  [2 points]

Count the words in a file. The goal here is to write a function that
lets you go directly from a filename to a word-count dictionary
using `count_words_from_string`. This should be a very quick function
that just reads the contents of the file into a string and uses
`count_words_from_string`.
"""

def count_words_from_filename(filename):
    """Read the contents of `filename` into a str and return the
    results of running `count_words_from_string` on that string

    Parameters
    ----------
    filename : str
        Full path to the file you want to process.

    Returns
    -------
    dict

    """
    with open(filename) as f:
        contents = f.read()

    return count_words_from_string(contents)


def test_count_words_from_filename(filename):
    """To run this test, download

    http://www.stanford.edu/class/linguist278/data/alice.txt

    to your computer, place it in the same directory as this homework
    file, and call this test with

    test_count_words_from_filename("alice.txt")
    """
    examples = {
        "the": 807,
        "and": 404,
        "a": 328,
        "to": 327,
        "she": 237,
        "of": 318}
    counts = count_words_from_filename(filename)
    err_count = 0
    for word, expected in examples.items():
        result = counts[word]
        if result != expected:
            print("count_words_from_filename error for '{}':\n\tGot: {}\n\tExpected: {}".format(
                word, result, expected))
    print("test_count_words_from_filename completed with {} errors".format(err_count))


"""===================================================================
4.  [3 points]

The raw data files for the Google Books collection are available for
download. The files are huge, so I created a sample. Download this
file to your computer and make sure it is in the same directory
as this homework file:

http://www.stanford.edu/class/linguist278/data/googlebooks-eng-all-1gram-20120701-a-sample

The format of this file is as follows (whitespace inserted for
readability):

word TAB year TAB match_count TAB volume_count NEWLINE

The TAB character is "\t", which you can treat like any other (for
example, you can split a string on "\t").

Your task: complete `googlebooks_counts_by_year` so that it processes
the sample file and returns a 2d dictionary with this structure:

{
  word1: {year1: match_count, year2: match_count ...},
  word2: {year1: match_count, year2: match_count ...},
  ...
}

where the nature of the year dicts is determined by the file,
the years are ints, and the match_counts as ints.

Different words will have different years and counts associated
with them.
"""

def googlebooks_counts_by_year(filename, gz=False):
    """Maps a Google books 1-grams file to a 2d dictionary
    giving each word's counts by year.

    Parameters
    ----------
    filename : str
        Full path to the Google Books count file to parse.
    gz : bool
        If True, `filename` is presumed to be compressed.

    Returns
    -------
    dict mapping words to dicts giving their counts by year.

    """

    from collections import defaultdict

    if gz:
        f = gz.open(filename, mode='rt', encoding='utf-8')
    else:
        f = open(filename)

    data = defaultdict(int)
    with f:
        for line in f:
            w, y, c, _ = line.split('\t')
            y = int(y)
            c = int(c)

            data[w][y] = c

    return dict(data)


def test_googlebooks_counts_by_year(filename):
    counts = googlebooks_counts_by_year(filename)
    examples = {
        ("abstained", 1980): 3846,
        ("abstained", 1990): 4323}
    err_count = 0
    for (word, year), expected in examples.items():
        if word not in counts:
            print("test_googlebooks_counts_by_year: {} should be present as an outer key".format(word))
            err_count += 1
        elif year not in counts[word]:
            print("test_googlebooks_counts_by_year: {} should be present as an inner key for {}".format(year, word))
            err_count += 1
        else:
            result = counts[word][year]
            if result != expected:
                print("test_googlebooks_counts_by_year error for {}:\n\tGot: {}\n\tExpected: {}".format(
                    (word, year), result, expected))
                err_count += 1
    print("test_googlebooks_counts_by_year completed with {} errors".format(err_count))


"""===================================================================
Extra credit (up to 1 point): The full file associated with
the file googlebooks-eng-all-1gram-20120701-a-sample from problem 4 is
350MB when zipped up and 1.8GB when unzipped. So we would like to
avoid having to unzip it!

To iterate through a zipped file, one can simply do this:

import gzip

with gzip.open(filename, mode='rt', encoding='utf8') as f:
    ...

For the extra credit: Improve `googlebooks_counts_by_year` so that it
has a keyword argument `gz` that tells the function how to open
`filename`, and update the file-opening code so that it handles both
text and gzip formats.

To test your function, you can download one of the alphabetic 1-grams
files from

http://storage.googleapis.com/books/ngrams/books/datasetsv2.html

(The alphabetic ones are a, b, c, d, e, f, g, h, i, j, k, l, m, n,
o, p, q, r, s, t, u, v, w, x, y, and z)
"""


"""===================================================================
Place all function calls below the following conditional so that they
are called only if this module is called with

`python ling278_assign02.py`

No functions should execute if it is instead imported with

import ling278_assign02

in the interactive shell.
"""

if __name__ == '__main__':
    pass
