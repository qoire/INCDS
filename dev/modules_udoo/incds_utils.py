# Maintainence class for INCDS
from pyo import *
import global_var

class INCDSUtils(object):

    @staticmethod
    def calc_in_out(dev_input, dev_output):
        if not (dev_input == 'macbook' or dev_input == 'jawbone' or dev_input == 'yeti'):
            print "Could not find supported device"
            raise
        
        if not (dev_output == 'macbook' or dev_output == 'jawbone'):
            print "Could not find supported device"
            raise

        input_string = pa_list_devices()
        input_list = input_string.split('\n')

        for line in input_list:
            

INCDSUtils.calc_in_out('macbook', 'macbook')