#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3stapi.v1.classes.config import *

# the synchronize users thread (synchs once per hour).
class SynchronizeUsers(threading.Thread):
	def __init__(self, 
		# pass the r3stapi.RestAPI object.
		restapi=None,
		# the synchronize interval in minutes (default: synchronizes once per 60 min).
		synchronize_interval=60,
		# the sleep interval in minutes (default: checks synchronize interval once per 15 min).
		sleep_interval=15,
	):
		threading.Thread.__init__(self)
		self.restapi = restapi
		self.synchronize_interval = synchronize_interval
		self.sleep_interval = sleep_interval
	def run(self):
		last = None
		while True:
			date, new = Formats.Date(), False
			if last == None: new = True
			else:
				increased = date.increase(last, minutes=self.synchronize_interval)
				new = date.compare(increased, date.timestamp) in ["present", "past"]
			if new:
				last = date.timestamp
				response = self.restapi.synchronize_users(silent=True)
				r3sponse.log(response, log_level=-1, save_errors=True)
			time.sleep(self.sleep_interval*60)