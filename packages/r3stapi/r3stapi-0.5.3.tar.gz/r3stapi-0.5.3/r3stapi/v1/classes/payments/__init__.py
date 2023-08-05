#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3stapi.v1.classes.config import *

# the payments object class.
class Payments(object):
	def __init__(self,
		# the restapi.stripe object.
		stripe=None,
		# the restapi.firebase object.
		firebase=None
	):
		self.stripe = stripe
		self.firebase = firebase	
		#
	def get_subscriptions(self):
		try:

			# iterate.
			subscriptions = {}
			for subscription in self.stripe.Subscription.list()['data']:
				
				customer = subscription["customer"]
				email = self.stripe.Customer.retrieve(customer)["email"]					
				subscriptions[email] = {
					"email":email,
					"customer_id" : customer,
					"plans":{},
				}
				#	-	subscription plan summary:
				subscription_plans = subscription['items']['data']
				for subscription_plan in subscription_plans:
					id = subscription_plan['plan']['id']
					try: subscriptions[email]["plans"][id]
					except KeyError: subscriptions[email]["plans"][id] = {}
					active = subscription_plan['plan']['active']
					if active in [True, "true", "True", "TRUE"]: active = True
					else: active = False
					subscriptions[email]["plans"][id]["subscription_id"] = subscription_plan['id']
					subscriptions[email]["plans"][id]["plan_id"] = subscription_plan['plan']['id']
					subscriptions[email]["plans"][id]["plan_nickname"] = subscription_plan['plan']['nickname']
					subscriptions[email]["plans"][id]["plan_active_status"] = active

			# success.
			print(json.dumps(subscriptions, indent=4))
			return r3sponse.success_response("Successfully retrieved the subscriptions.", {
				"subscriptions":subscriptions,
			})

		# error.
		except Exception as e:
			return r3sponse.error_response(f"Failed to retrieve the subscriptions, error: {e}.")

		#
	def create_subscription(self,
		# the user's uid.
		uid=None,
		# the plan name.
		plan=None,
	):
		# js:
		# (https://stripe.com/docs/sources/cards)
		# python:
		# (https://stripe.com/docs/api/cards/create?lang=python
		a=1
	def cancel_subscription(self, 
		# the user's uid.
		uid=None,
		# the plan name.
		plan=None,
		# the users plans (to increase speed) (optional)
		plans={},
	):

		# get plans.
		if plans == {}:
			response = self.get_subscriptions()
			if response["error"] != None: return response
			try:
				plans = response["subscriptions"][uid]
			except KeyError:
				return r3sponse.error_response(f"Unable to find any subscriptions for user [{uid}].")	

		# get subscription id.
		try:
			subscription_id = plans[plan]["subscription_id"]
		except KeyError:
			return r3sponse.error_response(f"Unable to find any subscriptions for user [{uid}] from plan [{plan}].")	

		# delete.
		try:
			r = self.stripe.Subscription.delete(subscription_id)
			success = r["status"] = "canceled"
		except KeyError: success = False

		# handle success.
		if success:
			return r3sponse.success_response(f"Successfully canceled the subscription for user [{uid}] from plan [{plan}].")
		else:
			return r3sponse.error_response(f"Failed to cancel the subscription for user [{uid}] from plan [{plan}].")

		#
	def get_sources(self, 
		# the user's uid.
		uid=None,
	):


