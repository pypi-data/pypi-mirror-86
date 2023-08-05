#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3stapi.v1.classes.config import *

# the api object class.
class RestAPI(object):
	"""
	1:	Do not forget to fill the self api keys variables!
		Requires variable [firebase] to be set:
			
			firebase = Firebase(...)
	"""
	def __init__(self,
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
			the "plan_id" is the stripe plan id.
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
				"plan_id":"prod_I41OYB42aGgfNJ",
				"rate_limit":10000,
				"rate_reset":30, # in days.
				"api_keys":[],
				"rank":2,
			},
			"pro": {
				"plan_id":"prod_IPiu7aUFXgz53f",
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

		#
	def generate_key(self):
		for attempt in range(101):
			key = Formats.String("").generate(length=68, capitalize=True, digits=True)
			if key not in self.__plans__["developer"]["api_keys"]:
				new = True
				for plan, info in self.__plans__.items():
					if key in info["api_keys"]: 
						new = False 
						break
				if new:
					return r3sponse.success_response("Successfully generated a new unique api key.", {
						"api_key":key
					})
		return r3sponse.error_response("Failed to generate a new unique api key.")
	def identify_key(self, api_key=None):

		# check developer success.
		plan = None
		if str(api_key) in self.__plans__["developer"]["api_keys"]:
			plan = "developer"

		# check api key.
		else:
			for _plan_, info in self.__plans__.items():
				if api_key in info["api_keys"]:
					plan = _plan_
					break

		# get uid.
		response = self.get_uid_by_key(api_key)
		if response["error"] != None: return response
		uid = response["uid"]

		# return success.
		return r3sponse.success_response(f"Successfully identified API Key [{api_key}].", {
			"plan":plan,
			"uid":uid,
		})

		#
	def verify_key(self, api_key=None, plan=None):

		# check developer success.
		try:
			if str(api_key) in self.__plans__["developer"]["api_keys"]:
				return r3sponse.success_response(f"Successfully authorized API Key [{api_key}].") 
		except KeyError: a=1

		# check api key.
		try: 
			if api_key in self.__plans__[plan]["api_keys"]:
				return r3sponse.success_response(f"Successfully authorized API Key [{api_key}].")
			else:
				return r3sponse.error_response(f"API Key [{api_key}] is not authorized.")	
		except KeyError:
			return r3sponse.error_response(f"API Key [{api_key}] is not authorized.")

		#
	def verify_rate_limit(self, 
		# required.
		api_key=None, 
		# optional to increase speed.
		# the uid from the api key.
		uid=None,
		# the plan from the api key.
		plan=None,
	):

		# check info.
		if plan == None or uid == None:
			response = self.identify_key(api_key)
			if response["error"] != None: return response
			plan = response["plan"]
			uid = response["uid"]

		# pro / developer.
		if self.__plans__[plan]["rate_limit"] in [None, False]:
			return r3sponse.success_response("Successfully verified the rate limit.")

		# load data.
		response = self.firebase.users.load_data(uid)
		if response["error"] != None: return response
		data = response["data"]
		timestamp = response["data"]["timestamp"]

		# check timestamp.
		date = Formats.Date()
		success = False
		if timestamp == None:
			success = True
			data["timestamp"] = date.date
			data["requests"] = 0
		else:
			altered = date.increase(timestamp, days=self.__plans__[plan]["rate_reset"], format="%d-%m-%y")
			#decreased_timestamp = date.from_seconds(decreased)
			if date.compare(altered, date.date, format="%d-%m-%y") in ["present", "past"]:
				success = True
				data["timestamp"] = date.date
				data["requests"] = 0

			# check rate limit.
			if not success and int(data["requests"]) <= self.__plans__[plan]["rate_limit"]: 
				success = True

		# response.
		if success:
			data["requests"] += 1
			response = self.firebase.users.save_data(uid, data)
			if response["error"] != None: return response
			return r3sponse.success_response("Successfully verified the rate limit.")
		else:
			if plan in ["free"]:
				return r3sponse.error_response("You have exhausted your monthly rate limit. Upgrade your membership to premium or pro for more requests.")
			elif plan in ["premium"]:
				return r3sponse.error_response("You have exhausted your monthly rate limit. Upgrade your membership to pro for unlimited requests.")
			else:
				return r3sponse.error_response("You have exhausted your monthly rate limit.")

		# 
	def get_key_by_uid(self, uid):
		api_key = None
		try:
			api_key = self.uid_api_keys[uid]
		except KeyError:
			api_key == None
		if api_key != None:
			return r3sponse.success_response(f"Successfully found the uid for the specified user [{uid}].", {"api_key":self.uid_api_keys[uid]})
		else:
			return r3sponse.error_response(f"Failed to find the uid for the specified user [{uid}].")
	def get_uid_by_key(self, api_key):
		for uid, _api_key_ in self.uid_api_keys.items():
			if str(_api_key_) == str(api_key):
				return r3sponse.success_response("Successfully found the uid for the specified api key.", {"uid":uid})
		return r3sponse.error_response("Failed to find the uid for the specified api key.")
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
					except KeyError: subscriptions[email][email]["plans"][id] = {}
					subscriptions[email]["plans"][id]["subscription_id"] = subscription_plan['id'],
					subscriptions[email]["plans"][id]["plan_id"] = subscription_plan['plan']['id'],
					subscriptions[email]["plans"][id]["plan_nickname"] = subscription_plan['plan']['nickname'],
					subscriptions[email]["plans"][id]["plan_active_status"] = subscription_plan['plan']['active'],

			# success.
			return r3sponse.success_response("Successfully retrieved the subscriptions.", {
				"subscriptions":subscriptions,
			})

		# error.
		except Exception as e:
			return r3sponse.error_response("Failed to retrieve the subscriptions.")

		#
	def create_subscription(self):
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
	def synchronize_users(self):
		"""
			Checks all users & inserts new data.
			Maps the api keys per subscription per plan.
		"""

		# get subs.
		response = self.get_subscriptions()
		if response["error"] != None: return response
		subscriptions = response["subscriptions"]

		# check-remove double subscriptions.
		rank, plan, cancel_subs = None, None, {}
		for uid, plans in subscriptions.items():
			for plan, info in plans.items():
				if info["plan_active_status"]:
					response = self.__get_plan_by_plan_id__(info["plan_id"])
					if response["error"] != None: return response
					l_plan = response["plan"]
					l_rank = self.__plans__[l_plan]["rank"]
					if plan == None:
						rank, plan = int(l_rank), str(l_plan)
					else:
						if int(l_rank) > int(rank):
							try:cancel_subs[uid]
							except KeyError: cancel_subs[uid] = []
							if plan not in ["free"]:
								cancel_subs[uid].append(plan)
							rank, plan = int(l_rank), str(l_plan)
		for uid, plans in cancel_subs.items():
			for plan in plans:
				response = self.cancel_subscription(uid=uid, plan=plan)
				if response["error"] != None: return response
		# reset.
		for plan in list(self.__plans__.keys()):
			self.__plans__[plan]["api_keys"] = []
		self.uid_api_keys = {}

		# iterate users.
		for user in self.firebase.users.iterate():

			# load data.
			uid = user.email # <-- NOTE THE CHANGE OF SAVING USERS BY (email) INSTEAD OF BY (uid).
			reference = f"users/{uid}"
			response = self.firebase.firestore.load(reference)

			# get plans.
			try: plans = subscriptions[uid]["plans"]
			except KeyError: plans = {}

			# handle new data.
			data = None
			if response["error"] != None:
				response = self.__save_new_user__(uid)
				if response["error"] != None: return response
				data = response["data"]

			# handle existing data.
			else: 
				response = self.__check_existing_user__(uid, response["document"], plans=plans)
				if response["error"] != None: return response
				data = response["data"]

			# map api keys.
			plan = data["membership"]
			api_key = data["api_key"]
			try: self.__plans__[plan]
			except KeyError: 
				return r3sponse.error_response(f"Failed to synchronize the users, user [{uid}] has an unknown membership [{plan}].")
			self.__plans__[plan]["api_keys"].append(api_key)

			# map uid api key.
			self.uid_api_keys[uid] = api_key

		# success response.
		return r3sponse.success_response("Successfully synchronized the users.")

		#
	# system functions.
	def __save_new_user__(self, uid):
		
		# set to default data.
		reference = f"users/{uid}"
		data = ast.literal_eval(str(self.__default_user_data__))

		# generate api key.
		response = self.generate_key()
		if response["error"] != None: return response
		data["api_key"] = response["api_key"]

		# save new data.
		response = self.firebase.firestore.save(reference, data) 
		if response["error"] != None: return response
		return r3sponse.success_response(f"Successfully saved new user [{uid}].", {"data":data})
		#
	def __check_existing_user__(self, uid, data, plans={}):
		edits = 0
		reference = f"users/{uid}"

		# check defaults.
		clone = ast.literal_eval(str(data))
		dict = Files.Dictionary(path=False, dictionary=data)
		data = dict.check(default=self.__default_user_data__)
		if data != clone:
			edits += 1

		# test api key.
		try: data["api_key"]
		except KeyError: 
			response = self.generate_key()
			if response["error"] != None: return response
			data["api_key"] = response["api_key"]
			edits += 1

		# check stripe subsription status.
		rank, membership = None, "free"
		for plan, info in plans.items():
			if info["plan_active_status"]:
				response = self.__get_plan_by_plan_id__(info["plan_id"])
				if response["error"] != None: return response
				l_membership = response["plan"]
				l_rank = self.__plans__[l_membership]["rank"]
				if rank == None: 
					rank = int(l_rank)
					membership = str(l_membership)
				elif int(l_rank) > int(rank): 
					rank = int(l_rank)
					membership = str(l_membership)
		if membership != data["membership"]:
			data["membership"] = membership
			edits += 1

		# ...

		# RESET RATES FOR TESTING.
		data["requests"] = 0
		edits += 1

		# save edits.
		if edits > 0:
			response = self.firebase.firestore.save(reference, data)
			if response["error"] != None: return response

		# response.
		return r3sponse.success_response(f"Successfully checked user [{uid}].", {"data":data})

		#
	def __get_plan_by_plan_id__(self, plan_id):
		for key, value in self.__plans__.items():
			if plan_id == value["plan_id"]: 
				return r3sponse.success_response("Successfully retrieved the plan.". {
					"plan":value["plan_id"],
				})
		return r3sponse.error_response(f"Failed to rerieve the plan name for stripe plan id [{plan_id}].")

