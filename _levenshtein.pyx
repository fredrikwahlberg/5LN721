# -*- coding: utf-8 -*-
"""
@author: Fredrik Wahlberg <fredrik.wahlberg@lingfil.uu.se>
"""

import numpy as np
cimport numpy as np
cimport cython

__all__ = ['_levenshtein_distance']

def _levenshtein_distance(lhs, rhs):
    cdef np.ndarray[np.int_t, ndim=2, mode="c"] cost_matrix
    cdef int i = 0, j = 0, substitution, insertion, deletion, cost
    cdef int m = len(lhs), n = len(rhs)

    cost_matrix = np.zeros((m+1, n+1), dtype=np.int)

    for i in range(1, cost_matrix.shape[0]):
        cost_matrix[i][0] = i
    for j in range(1, cost_matrix.shape[1]):
        cost_matrix[0][j] = j

    for i in range(1, cost_matrix.shape[0]):
        for j in range(1, cost_matrix.shape[1]):
            if lhs[i-1] == rhs[j-1]:
                substitution = cost_matrix[i-1][j-1]
            else:
                substitution = cost_matrix[i-1][j-1] + 1
            insertion = cost_matrix[i][j-1] + 1
            deletion = cost_matrix[i-1][j] + 1
            cost_matrix[i][j] = min(substitution, insertion, deletion)

    return cost_matrix, cost_matrix[m][n]