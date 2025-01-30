from django.test import TestCase


def test_no_match():
    """
    this test should make a search were 0 parameters match, for which a special case is implemented
    """

def test_exactly_one_match():
    """
    given 3 parameters that fit exactly one db entry, this should always return one predictable result based on current db entries
    """

def test_many_displays():
    """
    using parameters that give a high amount of results, all the results should still be visible on the page all at once
    """

def test_invalid_entry():
    """
    test what happens with various invalid entries and adjust entry parameters if necessary
    """
