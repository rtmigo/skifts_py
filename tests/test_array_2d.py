import unittest

import numpy as np
import numpy.testing as tst

from skifts._array2d import Array2D


class Test(unittest.TestCase):
    def test_keep(self):
        arr = np.array([[1, 0, 3, 0, 5],
                        [10, 20, 30, 40, 50]])
        mod = Array2D.keep_columns_with_nonzero_first_row(arr)
        tst.assert_array_equal(mod, [[1, 3, 5],
                                     [10, 30, 50]])

