# -*- coding: utf-8 -*-
"""
@author: Fredrik Wahlberg <fredrik.wahlberg@lingfil.uu.se>
"""

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
    distance : int

    Examples
    --------
    > wer("bacon spam spam", "spam spam")
    1
    """
    assert type(lhs) == str
    assert type(rhs) == str
    words1 = lhs.split()
    words2 = rhs.split()
    return _levenshtein._levenshtein_distance(words1, words2)[1]


def cer(lhs, rhs):
    """
    Character Error Rate (WER) using Levenshtein distance

    Parameters
    ----------
    lhs : str
    rhs : str

    Returns
    -------
    distance : int

    Examples
    --------
    > cer("bacon spam spam", "spam spam")
    6
    """
    assert type(lhs) == str
    assert type(rhs) == str
    lh_words = list(lhs)
    rh_words = list(rhs)
    assert np.all(np.asarray([len(w) for w in lh_words]) == 1)
    assert np.all(np.asarray([len(w) for w in rh_words]) == 1)
    return _levenshtein._levenshtein_distance(lh_words, rh_words)[1]


if __name__ == '__main__':
    t1 = "spam spam spam lovely spam wonderfull spam"
    t2 = "bacon spam spam lovely spam wonderfull spam"
    t3 = "spam spam"
    assert wer(t1, t2) == 1
    assert wer(t1, t3) == 5
    assert wer("spam spam", "spam bacon spam") == 1
    assert wer("bacon spam spam", "spam spam") == 1
    assert wer("spam spam", "bacon spam spam") == 1
    assert wer("spam spam", "spam spam") == 0
    assert cer(t1, t2) == 5
    assert cer(t1, t3) == 33
    assert cer("spam spam", "spam spam") == 0
    with open("Eisenhower.txt", 'r', encoding='utf-8') as file:
        text = file.read()
    import time
    from borrowed_code import wer as wer2
    t = time.time()
    cost1 = wer(text, text)
    print("wer %ims" % (1000*(time.time() - t)))
    t = time.time()
    cost2 = wer2(text.split(), text.split())
    print("wer2 %ims" % (1000*(time.time() - t)))
    assert cost1 == cost2
    assert wer(t1, t2) == wer2(t1.split(), t2.split())
