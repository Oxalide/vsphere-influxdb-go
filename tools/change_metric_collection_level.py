#!/usr/bin/python
#============================================
# Script: change_metric_collection_level.py 
# Description: Change the metric collection level of an interval in a vCenter
# Copyright 2017 Adrian Todorov, Oxalide ato@oxalide.com
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#============================================

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit
import sys
import requests
import argparse
import getpass
import linecache

requests.packages.urllib3.disable_warnings()

def PrintException():
	 exc_type, exc_obj, tb = sys.exc_info()
	 f = tb.tb_frame
	 lineno = tb.tb_lineno
	 filename = f.f_code.co_filename
	 linecache.checkcache(filename)
	 line = linecache.getline(filename, lineno, f.f_globals)
	 print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def get_args():
    parser = argparse.ArgumentParser(description='Arguments for talking to vCenter and modifying a PerfManager collection interval')

    parser.add_argument('-s', '--host', required=True,action='store',help='vSpehre service to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store', help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store', help='User name to use')
    parser.add_argument('-p', '--password', required=False, action='store', help='Password to use')
    parser.add_argument('--interval-name', required=False, action='store', dest='intervalName', help='The name of the interval to modify')
    parser.add_argument('--interval-key', required=False, action='store', dest='intervalKey', help='The key of the interval to modify')
    parser.add_argument('--interval-level', type=int, required=True, default=4, action='store', dest='intervalLevel', help='The collection level wanted for the interval')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass(prompt='Enter password:\n')
	if not args.intervalName and not args.intervalKey:
		print "An interval name or key is needed"
		exit(2)
	
	return args

def change_level(host, user, pwd, port, level, key, name):
	try:
		print user
		print pwd
		print host
		serviceInstance = SmartConnect(host=host,user=user,pwd=pwd,port=port)
		atexit.register(Disconnect, serviceInstance)
		content = serviceInstance.RetrieveContent()
		pm  = content.perfManager

		for hi in pm.historicalInterval:
			if (key and int(hi.key) == int(key)) or (name and str(hi.name) == str(name)):
				print "Changing interval '"  + str(hi.name) + "'"
				newobj = hi
				newobj.level = level
				pm.UpdatePerfInterval(newobj)

		print "Intervals are now configured as follows: "
		print "Name | Level"
		pm2  = content.perfManager
		for hi2 in  pm2.historicalInterval:
			print hi2.name + " | " + str(hi2.level)

	except Exception, e:
		print "Error: %s " % (e)
		PrintException()
		exit(2)


if __name__ == "__main__":
	args = get_args()
	change_level(args.host, args.user, args.password, args.port, args.intervalLevel, args.intervalKey, args.intervalName)


