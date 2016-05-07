'''
Created on 03/11/2014

@author: hashtonmartyn
'''
import unittest
import traceback
import datetime
import random
from gpssim import GpsSim, constants, ModelGpsReceiver, TimeZone

LAT = 0.0
LON = 0.0
ALTITUDE = 0.0
GEOID_SEP = 0.0
HDOP = 1.0
VDOP = 1.0
PDOP = 1.0
KPH = 0.0
HEADING = 0.0
MAG_HEADING = None
MAG_VAR = 0.0


class TestGPSSim(unittest.TestCase):

    def setUp(self):
        self.sim = GpsSim()

    def tearDown(self):
        pass

    def test_invalid_fix__step(self):
        """
        Tests a fix for this issue https://bitbucket.org/wjiang/gpssim/issue/1/unhandled-exception-while-serving-an
        """
        self.sim.gps.fix = constants.INVALID_FIX
        self.sim._GpsSim__step()
        try:
            self.sim._GpsSim__step()
        except TypeError as err:
            self.fail("A type error was raised" % traceback.print_exc())
            raise err


class TestModelGpsReceiver(unittest.TestCase):

    def setUp(self):
        # Necessary because some of the initial data eg PRNs is generated at
        # random on initialisation
        random.seed(0)
        dt = datetime.datetime(2014, 11, 27, 9, 20, 53, 555000)
        print dt.isoformat()
        self.gps = ModelGpsReceiver(lat=LAT,
                                    lon=LON,
                                    altitude=ALTITUDE,
                                    geoid_sep=GEOID_SEP,
                                    hdop=HDOP,
                                    vdop=VDOP,
                                    pdop=PDOP,
                                    kph=KPH,
                                    heading=HEADING,
                                    mag_heading=MAG_HEADING,
                                    mag_var=MAG_VAR,
                                    date_time=dt)

    def tearDown(self):
        pass

    def test_lat_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.lat, LAT)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.lat, LAT)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.lat, LAT)

    def test_lon_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.lon, LON)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.lon, LON)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.lon, LON)

    def test_altitude_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.altitude, ALTITUDE)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.altitude, ALTITUDE)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.altitude, ALTITUDE)

    def test_geoid_sep_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.geoid_sep, GEOID_SEP)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.geoid_sep, GEOID_SEP)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.geoid_sep, GEOID_SEP)

    def test_hdop_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.hdop, HDOP)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.hdop, HDOP)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.hdop, HDOP)

    def test_vdop_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.vdop, VDOP)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.vdop, VDOP)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.vdop, VDOP)

    def test_pdop_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.pdop, PDOP)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.pdop, PDOP)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.pdop, PDOP)

    def test_kph_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.kph, KPH)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.kph, KPH)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.kph, KPH)

    def test_heading_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.heading, HEADING)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.heading, HEADING)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.heading, HEADING)

    def test_mag_heading_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.mag_heading, MAG_HEADING)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.mag_heading, MAG_HEADING)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.mag_heading, MAG_HEADING)

    def test_mag_var_property_returns_same_value_if_fix_is_gps_invalid_fix(self):
        self.assertEqual(self.gps.mag_var, MAG_VAR)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.mag_var, MAG_VAR)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.mag_var, MAG_VAR)

    def test_solution_invalid_fix_results_in_invalid_solution(self):
        self.assertEqual(self.gps.solution, constants.AUTONOMOUS_SOLUTION)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.solution, constants.INVALID_SOLUTION)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.solution, constants.AUTONOMOUS_SOLUTION)

    def test_vdop_is_same_value_when_altitude_is_None(self):
        self.assertEqual(self.gps.vdop, VDOP)
        self.gps.altitude = None
        self.assertEqual(self.gps.vdop, VDOP)
        self.gps.altitude = ALTITUDE
        self.assertEqual(self.gps.vdop, VDOP)

    def test_pdop_is_same_value_when_altitude_is_None(self):
        self.assertEqual(self.gps.pdop, PDOP)
        self.gps.altitude = None
        self.assertEqual(self.gps.pdop, PDOP)
        self.gps.altitude = ALTITUDE
        self.assertEqual(self.gps.pdop, PDOP)

    def test_get_output_returns_info_when_fix_is_valid(self):
        expected_valid_data = ['$GPGGA,092053.555,0000.000,N,00000.000,E,1,12,1.0,0.0,M,0.0,M,,*66',
                               '$GPGLL,0000.000,N,00000.000,E,092053.555,A,A*51',
                               '$GPGSA,A,3,1,3,4,7,9,10,13,20,21,22,25,29,1.0,1.0,1.0*05',
                               '$GPGSV,3,1,12,1,82,303,37,3,43,184,34,4,19,282,33,7,71,101,37*78',
                               '$GPGSV,3,2,12,9,71,327,39,10,21,291,39,13,56,169,31,20,65,296,36*4E',
                               '$GPGSV,3,3,12,21,55,0,34,22,7,312,32,25,76,85,39,29,10,39,35*4F',
                               '$GPRMC,092053.555,A,0000.000,N,00000.000,E,0.0,0.0,271114,0.0,E,A*0D',
                               '$GPVTG,0.0,T,,M,0.0,N,0.0,K,A*0D',
                               '$GPZDA,092053.555,27,11,2014,,*5C']

        expected_invalid_data = ['$GPGGA,092053.555,0000.000,N,00000.000,E,0,12,1.0,0.0,M,0.0,M,,*67',
                                 '$GPGLL,0000.000,N,00000.000,E,092053.555,V,N*49',
                                 '$GPGSA,A,1,1,3,4,7,9,10,13,20,21,22,25,29,1.0,1.0,1.0*07',
                                 '$GPGSV,3,1,12,1,82,303,37,3,43,184,34,4,19,282,33,7,71,101,37*78',
                                 '$GPGSV,3,2,12,9,71,327,39,10,21,291,39,13,56,169,31,20,65,296,36*4E',
                                 '$GPGSV,3,3,12,21,55,0,34,22,7,312,32,25,76,85,39,29,10,39,35*4F',
                                 '$GPRMC,092053.555,V,0000.000,N,00000.000,E,0.0,0.0,271114,0.0,E,N*15',
                                 '$GPVTG,0.0,T,,M,0.0,N,0.0,K,N*02',
                                 '$GPZDA,092053.555,27,11,2014,,*5C']
        self.assertEqual(self.gps.get_output(), expected_valid_data)
        self.gps.fix = constants.INVALID_FIX
        self.assertEqual(self.gps.get_output(), expected_invalid_data)
        self.gps.fix = constants.SPS_FIX
        self.assertEqual(self.gps.get_output(), expected_valid_data)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
