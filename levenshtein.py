# -*- coding: utf-8 -*-
"""
@author: Fredrik Wahlberg <fredrik.wahlberg@lingfil.uu.se>
"""

from  __future__ import division
import numpy as np
import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()},
                  reload_support=False)
import _levenshtein

__all__ = ['wer', 'cer']


def wer(lhs, rhs):
    """
    Word Error Rate (WER) using Levenshtein distance

    Parameters
    ----------
    lhs : str
    rhs : str

    Returns
    -------
    errors : int
    error_rate: float

    Examples
    --------
    > wer("bacon spam spam", "spam spam")
    (1, 0.3333333333333333)
    """
    assert type(lhs) == str
    assert type(rhs) == str
    lhs_words = lhs.split()
    rhs_words = rhs.split()
    errors = _levenshtein._levenshtein_distance(lhs_words, rhs_words)[1]
    error_rate = errors / max(len(lhs_words), len(rhs_words))
    return errors, error_rate


def cer(lhs, rhs):
    """
    Character Error Rate (WER) using Levenshtein distance

    Parameters
    ----------
    lhs : str
    rhs : str

    Returns
    -------
    errors : int
    error_rate: float

    Examples
    --------
    > cer("bacon spam spam", "spam spam")
    (6, 0.4)
    """
    assert type(lhs) == str
    assert type(rhs) == str
    lhs_characters = list(lhs)
    rhs_characters = list(rhs)
    #assert np.all(np.asarray([len(w) for w in lhs_characters]) == 1)
    #assert np.all(np.asarray([len(w) for w in rhs_characters]) == 1)
    errors = _levenshtein._levenshtein_distance(lhs_characters, rhs_characters)[1]
    error_rate = errors / max(len(lhs_characters), len(rhs_characters))
    return errors, error_rate


if __name__ == '__main__':
    # TODO Update these
    t1 = "spam spam spam lovely spam wonderfull spam"
    t2 = "bacon spam spam lovely spam wonderfull spam"
    t3 = "spam spam"
    assert wer(t1, t2)[0] == 1
    assert wer(t1, t3)[0] == 5
    assert wer("spam spam", "spam bacon spam")[0] == 1
    assert wer("bacon spam spam", "spam spam")[0] == 1
    assert wer("spam spam", "bacon spam spam")[0] == 1
    assert wer("spam spam", "spam spam")[0] == 0
    assert cer(t1, t2)[0] == 5
    assert cer(t1, t3)[0] == 33
    assert cer("spam spam", "spam spam")[0] == 0
    print("Tests ran successfully")
