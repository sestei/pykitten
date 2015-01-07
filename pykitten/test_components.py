#!/usr/bin/python
import unittest
import components

class TestComponents(unittest.TestCase):
    def test_reflectivity(self):
        kw = {
            'T': '10m',
        }
        # check auto-setting of R
        kw = components.auto_reflectivity(kw)
        self.assertEqual(kw['R'], 0.99)

        # should not change anything if R and T set
        kw['R'] = 0.1
        kw = components.auto_reflectivity(kw)
        self.assertEqual(kw['R'], 0.1)

        # test auto-setting of T
        del(kw['T'])
        kw = components.auto_reflectivity(kw)
        self.assertEqual(kw['T'], 0.9)

        # as soon as loss is set, shouldn't touch anything
        kw['L'] = 0.0
        kw['T'] = 0.5
        kw = components.auto_reflectivity(kw)
        self.assertEqual(kw['T'], 0.5)


if __name__ == '__main__':
    unittest.main()