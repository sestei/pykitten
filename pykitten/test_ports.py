#!/usr/bin/python
import unittest

from components import *
from ports import DetectorPort,AlreadyLinked

class TestPorts(unittest.TestCase):
    def test_port_connection(self):
        pa = Port(None)
        pb = Port(None)

        # connect pa and pb, should result in both targets
        # being the same
        pa >> pb
        self.assertEqual(pa.targetname, pa.targetname)

        pc = Port(None)
        self.assertRaises(AlreadyLinked, pb.connect, pb, pc)

    def test_dump_port(self):
        pd = DumpPort(None)
        self.assertGreater(pd.precedence, 0)
        self.assertEqual(pd.targetname, 'dump')

    def test_detector_port(self):
        pa = Port(None)
        pb = Port(None)
        pd1 = DetectorPort(None)
        pd2 = DetectorPort(None)

        pa >> pd1
        self.assertEqual(pa.targetname, pd1.targetname)
        
        pd2 >> pb
        self.assertEqual(pb.targetname + '*', pd2.targetname)

    def test_space_creation(self):
        pa = Port(None)

        sp = pa >> 1
        self.assertIsInstance(sp, Space)
        self.assertEqual(sp._kwargs['L'], 1)

        pa = Port(None)
        sp = pa >> 2.0
        self.assertIsInstance(sp, Space)
        self.assertEqual(sp._kwargs['L'], 2.0)

        pa = Port(None)
        sp = pa >> (1, 2.0)
        self.assertIsInstance(sp, Space)
        self.assertEqual(sp._kwargs['L'], 1.0)
        self.assertEqual(sp._kwargs['n'], 2.0)


if __name__ == '__main__':
    unittest.main()