# Maintainence class for INCDS
from pyo import *
import global_var

class INCDSUtils(object):

	@staticmethod
	def calc_in_out(dev_input, dev_output):
		if not (dev_input == 'macbook' || dev_input == 'jawbone' || dev_input == 'yeti'):
			print "Could not find supported device"
			raise
		
		if not (dev_output == 'macbook' || dev_output == 'jawbone'):
			print "Could not find supported device"
			raise

		temp_var = pa_list_devices()
		print temp_var

