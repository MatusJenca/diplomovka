import unittest
import numpy as np
import sys

sys.path.insert(1, '..')
from tools.integrator import DoubleNewton, EPSILON

DELTA = 0.1


class TestDN(DoubleNewton):
    def __init__(self, function):
        DoubleNewton.__init__(self, function=function, start=np.array((EPSILON, EPSILON)), end=np.array((1, 1)),
                              num=np.array(2 * [1000]))

class MyTestCase(unittest.TestCase):
    # Testy pre integral od 0 po 1 v oboch premennych
    def test_xy(self):
        self.assertAlmostEqual(TestDN(lambda x, y: x * y).integral_value(), 0.25, delta=DELTA)  # x*y

    def test_xpy(self):
        self.assertAlmostEqual(TestDN(lambda x, y: x + y).integral_value(), 1, delta=DELTA)  # x+y

    def test_sinxpy(self):
        self.assertAlmostEqual(TestDN(lambda x, y: np.sin(x + y)).integral_value(), 0.772364, delta=DELTA)  # sin(x+y)

    def test_cosxpy(self):
        self.assertAlmostEqual(TestDN(lambda x, y: np.cos(x + y)).integral_value(), 0.496751, delta=DELTA)  # cos(x+y)

    def test_arctgxy(self):
        self.assertAlmostEqual(TestDN(lambda x, y: np.arctan(x * y)).integral_value(), 0.2332,
                               delta=DELTA)  # arctg(x*y)

    def test_logxy(self):
        self.assertAlmostEqual(TestDN(lambda x, y: np.log(x * y)).integral_value(), -2, delta=DELTA)  # log(x*y)
    # testy pre rozne hodnoty

    def test_1(self):
        self.assertAlmostEqual(DoubleNewton(
            function=lambda x, y: x+2*y,
            start=np.array((0.3243, -7.71626)),
            end=np.array((12.56, 8.23)),
            num=np.array((989, 1010)),
        ).integral_value(), 1357.19, delta=1)

if __name__ == '__main__':
    unittest.main()
