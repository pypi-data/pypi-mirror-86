#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3stapi.v1.classes.config import *
from r3stapi.v1.classes import payments

# the api object class.
class RestAPI(object):
	"""
	1:	Do not forget to fill the self api keys variables!
		Requires variable [firebase] to be set:
			
			firebase = Firebase(...)
	"""
	def __init__(self,
		# remove subscriptions when a user is subscribed to more then subscription.
		remove_double_subscriptions=True,
		# Pass either the firebase credentials or initialzed firebase object.
		# 	the firebase credentials.
		firebase_credentials=None,
		# 	the fir3base.FireBase object (optional).
		firebase=None,
		# Pass the stripe keys.
		# 	the stripe secret key.
		stripe_secret_key=None,
		# 	the stripe publishable key.
		stripe_publishable_key=None,
	):
		"""
		The users will be stored in firestore with the following structure:
			users/
				$uid/
					api_key: null
					membership: $plan_id
					requests: 0
					timestamp: null
					... your additional data ...
		Define your additional user data in the __default_user_data__ variable.
		"""
		self.__default_user_data__ = {
			"api_key":None,
			"membership":"free",
			"requests":0,
			"timestamp":None,
		}

		"""
		The plans.
			the "rate_limit" is total requests per "rate_reset"
			the "rate_reset" is the total days before rate limit reset.
			the "plan_id" is the price id from your stripe plan.
		"""
		self.__plans__ = {
			"developer": {
				"plan_id":None,
				"rate_limit":None,
				"rate_reset":None,
				"api_keys":[],
				"rank":None,
			},
			"free": {
				"plan_id":None,
				"rate_limit":3,
				"rate_reset":1, # in days.
				"api_keys":[],
				"rank":1,
			},
			"premium": {
				"plan_id":"price_1Hp9g.....", # price id from stripe plan.
				"rate_limit":10000,
				"rate_reset":30, # in days.
				"api_keys":[],
				"rank":2,
			},
			"pro": {
				"plan_id":"price_1HTnI.....", # price id from stripe plan.
				"rate_limit":25000,
				"rate_reset":30, # in days.
				"api_keys":[],
				"rank":3,
			},
		}

		# system variables.
		self.uid_api_keys = {
			"$uid":"$api_key..."
		}

		# stripe.
		if not isinstance(stripe_secret_key, str):
			raise ValueError("Define the parameter [stripe_secret_key].")
		self.stripe_secret_key = stripe_secret_key
		self.stripe_publishable_key = stripe_publishable_key
		self.stripe = stripe
		self.stripe.api_key = stripe_secret_key

		# firebase.
		if not isinstance(firebase, object) and  not isinstance(firebase_credentials, str):
			raise ValueError("Pass the either the firebase credentials (str/dict) or the initialized Firebase object from library fir3base. [from fir3base import FireBase]")
		if isinstance(firebase, object):
			self.firebase = firebase
		else:
			self.firebase = Firebase(firebase_credentials)

		# objects.
		self.payments = payments.Payments(
			stripe=self.stripe,
			firebase=self.firebase,)
		self.users = users.Users(
			# remove subscriptions when a user is subscribed to more then subscription.
			remove_double_subscriptions=remove_double_subscriptions,
			# the restapi.uid_api_keys variable.
			uid_api_keys=self.uid_api_keys,
			# the restapi.__default_user_data__ variable.
			__default_user_data__=self.__default_user_data__,
			# the restapi.__default_user_data__ variable.
			__plans__=self.__plans__,
			# the restapi.firebase object.
			firebase=self.firebase,
			# the restapi.stripe object.
			stripe=self.stripe,)

		#



