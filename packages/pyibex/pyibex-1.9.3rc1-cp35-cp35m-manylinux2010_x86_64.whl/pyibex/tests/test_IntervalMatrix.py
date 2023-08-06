#!/usr/bin/env python
#============================================================================
#                                P Y I B E X
# File        : test_IntervalVector.py
# Author      : Benoit Desrochers
# Copyright   : Benoit Desrochers
# License     : See the LICENSE file
# Created     : Dec 28, 2014
#============================================================================


import unittest
import pyibex
from pyibex import IntervalMatrix, IntervalVector, Interval

try:
  import numpy as np
  has_np = True
except ImportError:
  print("NUMPY NOT FOUND")
  has_np = False



class TestIntervalMatrix(unittest.TestCase):


    def test_constructor(self):
        a = IntervalMatrix(3,3, Interval(3,4))
        b = IntervalVector([[1,1], [1,1], [1,1]])
        c = a*b
        self.assertEqual(c,IntervalVector(3, [9, 12]))

    @unittest.skipUnless(has_np, "Numpy not found")
    def test_contructor_numpy(self):
        lst = [Interval(i) for i in range(0,9)]
        M = IntervalMatrix(3,3,lst)
        m = np.arange(0, 9, dtype=np.float64).reshape((3, 3))
        self.assertEqual(M, IntervalMatrix(m))
        # print(M)
        
    def test_contructor(self):
        lst = [Interval(i) for i in range(0,9)]
        M = IntervalMatrix(3,3,lst)
        # print(M)

    @unittest.expectedFailure
    def test_contructor_dim_mismatch(self):
        lst = [Interval(i) for i in range(0,8)]
        M = IntervalMatrix(3,3,lst)
        # print(M)

    # def test_constructor_array(self):
    #     a = array([1,2,3])

    def test_get_set(self):
        a = IntervalMatrix(3,3, Interval(3,4))
        self.assertEqual(a[1], IntervalVector(3, Interval(3,4)))
        self.assertEqual(a[0][2], Interval(3,4))
        a[0][2] = Interval(0,0)
        self.assertEqual(a[0][2], Interval(0,0))
        a[0][0] = 0
        self.assertEqual(a[0][0], Interval(0,0))
        a[2][1] = 2.0
        self.assertEqual(a[2][1], Interval(2))

    def test_shape(self):
        a = IntervalMatrix(3,3, Interval(3,4))
        self.assertEqual(a.shape(), (3,3))

    # @unittest.skipUnless(has_np, "Numpy not found")
    # def test_op_numpy(self):
    #     lst = [Interval(i) for i in range(0,9)]
    #     M = IntervalMatrix(3,3,lst)
    #     m = np.array([[1,2,3], [4,5,6], [7,8,9]], dtype=np.float64)
    #     res = IntervalMatrix(3,3,Interval(0))
    #     self.assertEqual(M-IntervalMatrix(m), res)
    
 
if __name__ == '__main__':
    unittest.main()
