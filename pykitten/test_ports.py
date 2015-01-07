#!/usr/bin/python
import unittest

from components import *
from ports import DetectorPort

class TestPorts(unittest.TestCase):
    def test_port_connection(self):
        pa = Port()
        pb = Port()

        # connect pa and pb, should result in both targets
        # being now pa's original target
        initial = pa.targetname
        pa >> pb
        self.assertEqual(pa.targetname, initial)
        self.assertEqual(pb.targetname, initial)

        # pc should have precedence over pb
        pc = Port(precedence=100)
        initial = pc.targetname
        pb >> pc
        self.assertEqual(pb.targetname, initial)

        # pd should not have precendence over pc
        pd = Port(precedence=-100)
        initial = pd.targetname
        pc >> pd
        self.assertNotEqual(pd.targetname, initial)

    def test_dump_port(self):
        pd = DumpPort()
        self.assertGreater(pd.precedence, 0)
        self.assertEqual(pd.targetname, 'dump')

    def test_detector_port(self):
        pa = Port()
        pb = Port()
        pd = DetectorPort()

        pa >> pd
        self.assertEqual(pa.targetname, pd.targetname)
        
        pd >> pb
        self.assertEqual(pb.targetname + '*', pd.targetname)

    def test_space_creation(self):
        pa = Port()

        sp = pa >> 1
        self.assertIsInstance(sp, Space)
        self.assertEqual(sp._kwargs['L'], 1)

        sp = pa >> 2.0
        self.assertIsInstance(sp, Space)
        self.assertEqual(sp._kwargs['L'], 2.0)

        sp = pa >> (1, 2.0)
        self.assertIsInstance(sp, Space)
        self.assertEqual(sp._kwargs['L'], 1.0)
        self.assertEqual(sp._kwargs['n'], 2.0)


if __name__ == '__main__':
    unittest.main()