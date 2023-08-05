#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype string joining utilities** (i.e., callables joining passed
strings into new strings delimited by passed substring delimiters).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                           }....................
from collections.abc import Sequence

# ....................{ JOINERS                           }....................
def join_delimited(
    strs: 'Sequence[str]',
    delimiter_if_two: str,
    delimiter_if_three_or_more_nonlast: str,
    delimiter_if_three_or_more_last: str
) -> str:
    '''
    Concatenate the passed sequence of zero or more strings delimited by the
    passed delimiter (conditionally depending on both the length of this
    sequence and index of each string in this sequence), yielding a
    human-readable string listing arbitrarily many substrings.

    Specifically, this function returns either:

    * If this sequence contains no strings, the empty string.
    * If this sequence contains one string, this string as is is unmodified.
    * If this sequence contains two strings, these strings delimited by the
      passed ``delimiter_if_two`` delimiter.
    * If this sequence contains three or more strings, a string listing these
      contained strings such that:

      * All contained strings except the last two are suffixed by the passed
        ``delimiter_if_three_or_more_nonlast`` delimiter.
      * The last two contained strings are delimited by the passed
        ``delimiter_if_three_or_more_last`` separator.

    Parameters
    ----------
    strs : Sequence[str]
        Sequence of all strings to be joined.
    delimiter_if_two : str
        Substring separating each string contained in this sequence if this
        sequence contains exactly two strings.
    delimiter_if_three_or_more_nonlast : str
        Substring separating each string *except* the last two contained in
        this sequence if this sequence contains three or more strings.
    delimiter_if_three_or_more_last : str
        Substring separating each string the last two contained in this
        sequence if this sequence contains three or more strings.

    Returns
    ----------
    str
        Concatenation of these strings.

    Examples
    ----------
    >>> join_delimited(
    ...     strs=('Fulgrim', 'Perturabo', 'Angron', 'Mortarion'),
    ...     delimiter_if_two=' and ',
    ...     delimiter_if_three_or_more_nonlast=', ',
    ...     delimiter_if_three_or_more_last=', and '
    ... )
    'Fulgrim, Perturabo, Angron, and Mortarion'
    '''
    assert isinstance(strs, Sequence) and not isinstance(strs, str), (
        '{!r} not non-string sequence.'.format(strs))
    assert isinstance(delimiter_if_two, str), (
        '{!r} not string.'.format(delimiter_if_two))
    assert isinstance(delimiter_if_three_or_more_nonlast, str), (
        '{!r} not string.'.format(delimiter_if_three_or_more_nonlast))
    assert isinstance(delimiter_if_three_or_more_last, str), (
        '{!r} not string.'.format(delimiter_if_three_or_more_last))

    # Number of strings in this sequence.
    num_strs = len(strs)

    # If no strings are passed, return the empty string.
    if num_strs == 0:
        return ''
    # If one string is passed, return this string as is.
    elif num_strs == 1:
        return strs[0]
    # If two strings are passed, return these strings delimited appropriately.
    elif num_strs == 2:
        #FIXME: Refactor to leverage f-strings after dropping Python 3.5
        #support, which are the optimal means of performing string formatting.
        return '{}{}{}'.format(strs[0], delimiter_if_two, strs[1])

    # Else, three or more strings are passed.
    #
    # All such strings except the last two, delimited appropriately.
    strs_nonlast = delimiter_if_three_or_more_nonlast.join(strs[0:-2])

    #FIXME: Refactor to leverage f-strings after dropping Python 3.5
    #support, which are the optimal means of performing string formatting.

    # The last two such strings, delimited appropriately.
    strs_last = '{}{}{}'.format(
        strs[-2], delimiter_if_three_or_more_last, strs[-1])

    # Return these two substrings, delimited appropriately.
    return '{}{}{}'.format(
        strs_nonlast, delimiter_if_three_or_more_nonlast, strs_last)


def join_delimited_disjunction(strs: 'Sequence[str]') -> str:
    '''
    Concatenate the passed sequence of zero or more strings delimited by commas
    and/or the conjunction "or" (conditionally depending on both the length of
    this sequence and index of each string in this sequence), yielding a
    human-readable string listing arbitrarily many substrings disjunctively.

    Specifically, this function returns either:

    * If this sequence contains no strings, the empty string.
    * If this sequence contains one string, this string as is is unmodified.
    * If this sequence contains two strings, these strings delimited by the
      conjunction "or".
    * If this sequence contains three or more strings, a string listing these
      contained strings such that:

      * All contained strings except the last two are suffixed by commas.
      * The last two contained strings are delimited by the conjunction "or".

    Parameters
    ----------
    strs : Sequence[str]
        Sequence of all strings to be concatenated disjunctively.

    Returns
    ----------
    str
        Disjunctive concatenation of these strings.
    '''

    return join_delimited(
        strs=strs,
        delimiter_if_two=' or ',
        delimiter_if_three_or_more_nonlast=', ',
        delimiter_if_three_or_more_last=', or '
    )
