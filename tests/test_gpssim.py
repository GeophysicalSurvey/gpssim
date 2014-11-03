'''
Created on 03/11/2014

@author: hashtonmartyn
'''
import unittest
import traceback
from gpssim import GpsSim, constants
        
class TestGPSSim(unittest.TestCase):
    
    def setUp(self):
        self.sim = GpsSim()
    
    def tearDown(self):
        pass
    
    def test_invalid_fix__step(self):
        """
        Tests a fix for this issue https://bitbucket.org/wjiang/gpssim/issue/1/unhandled-exception-while-serving-an
        """
        self.sim.gps.fix = constants.GPS_INVALID_FIX
        self.sim._GpsSim__step()
        try:
            self.sim._GpsSim__step()
        except TypeError as err:
            self.fail("A type error was raised" % traceback.print_exc())
            raise err


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()