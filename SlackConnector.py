from slacker import Slacker
from decimal import Decimal
import ConfigParser
import datetime
import time
import json
import os

class SlackConnector():
	
	slack = None
	_users = []
	_channels = []
	
	# Send a message to #general channel
	#slack.chat.post_message('#general', 'Hello fellow slackers!')

	# Get users list
	#response = slack.users.list()
	#users = response.body['members']

	def _epoch_to_date(self, epoch):
		dateobj = datetime.datetime.fromtimestamp(float(epoch)).date()
		date_str = "%s/%s/%s"%(dateobj.day, dateobj.month, dateobj.year)
		return date_str

	def _find_ids(self, text, substring):
		index = 0
		indices = []
		length_sub = len(substring)
		length = len(text)
		while index < length:# and True if length and (length - index) > length else False:
			index = text.find(substring, index)
			if index == -1:
				break
			indices.append("%s"%text[index+1:index+10])
			index += length_sub
		return indices

	# get channel id
	def get_users(self):
		members = self.slack.users.list().body['members']
		res = {}
		for i, member in enumerate(members):
			res[member['id']] = member['name']
		return res

	def get_channels(self):
		channels = self.slack.channels.list()
		return channels

	def get_filtered_messages(self, selected_channels=[], selected_tags=[]):
		message_return = []
		for channel in self._channels.body['channels']:
			channel_id = channel['id']
			channel_name = channel['name']
			if channel_name in selected_channels:
				messages = self.slack.channels.history(channel_id).body['messages']
				for message in messages:
					for tag in selected_tags:
						# check if "+tag" exists in message text and append it
						if tag != "" and "+%s"%tag in message['text']:
							# convert user and timestamp to human readable values
							message['user'] = self._users[message['user']]
							message['ts'] = datetime.datetime.fromtimestamp(float(message['ts'].decode("utf-8")))
							message['channel_name'] = channel_name
							message_return.append(message)
		return message_return

	def get_messages(self):
		channel_name = 'hdk'
		channels = self.slack.channels.list()
		channel_id = None
		for channel in channels.body['channels']:
			if (channel['name'] == channel_name):
				channel_id = channel['id']

		# get members
		members = {}
		users = self.slack.users.list()
		for user in users.body['members']:
			members[user['id']] = user['name']

		# get channels
		if (channel_id is not None):
			general_channel = self.slack.channels.history(channel_id)
			for message in general_channel.body['messages']:
				text = message['text']
				ids = self._find_ids(text, "@")
				for id in ids:
					try:
						text = text.replace(id, members[id])	
					except Exception:
						pass

				print("%s - %s: %s" % (self._epoch_to_date(message['ts']), members[message['user']],text))

	def __init__(self):
		config = ConfigParser.ConfigParser()
		config.readfp(open('config.cfg'))
		token = config.get("connection_settings", "token")
		self.slack = Slacker(token)
		self._users = self.get_users()
		self._channels = self.get_channels()
