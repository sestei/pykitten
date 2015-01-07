#!/usr/bin/python
import unittest

from utils import Singleton

@Singleton
class A(object):
    def __init__(self):
        self.x = 1

    def set_x(self, x):
        self.x = x

class TestSingleton(unittest.TestCase):
    def direct_instantiation():
        a = A()

    def test_singleton(self):
        self.assertRaises(TypeError, self.direct_instantiation)
        
        a = A.Instance()
        a.set_x(10)
        self.assertEqual(a.x, 10)

        b = A.Instance()
        self.assertEqual(b.x, 10)       


if __name__ == '__main__':
    unittest.main()