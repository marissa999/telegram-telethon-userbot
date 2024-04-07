#!/usr/bin/env python3

import sys
from random import random
import asyncio
from asyncio import sleep
from telethon import TelegramClient,events
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# Import settings
import env


# Frames for animations
animation = [
	[ ".. _ .",		". _ .",	"._  .",	". _ .",	".  _."],
	[ "..-.",		".-.",		"._.",		".-.",		"._."],
	[ ".p.p",		"p.p",		"q.q",		"p.p",		"q.q"],
	[ ".;_;",		";_;",		"⁏_⁏",		";_;",		"⁏_⁏"]
]

# parse account from cli
if len(sys.argv) != 3:
	print("You need to specify an account name and a phone number!")
	exit()

account_file = sys.argv[1]
telephone_number = sys.argv[2]

client = TelegramClient(account_file, env.api_id, env.api_hash)

@client.on(events.NewMessage(outgoing=True))
async def self(event):
	message_string = event.text
			
	if "@all" in message_string:
		await event.delete()
		all_participants = await client.get_participants(event.message.chat_id)
		mention_string = "[@all](tg://need_update_for_some_feature)"
		for user in all_participants:
			mention_string += "[⁣](tg://user?id=" + str(user.id) + ")"
		message_string = message_string.replace("@all", mention_string)
		await client.send_message(event.message.chat_id, message_string)
		return

	if ".. _ ." in message_string or "..-." in message_string or ".p.p" in message_string:
		str_orig = message_string
		new_message = (str_orig
			.replace(".. _ .", ". _ .")
			.replace("..-.", ".–.")
			.replace(".p.p", "p.p")
			.replace(".;_;", ";_;")
		)
		await event.edit(new_message)
		for _ in range(20):			   
			await sleep(0.5)
			await event.edit(str_orig
				.replace(".. _ .", "._  .")
				.replace("..-.", "._.")
				.replace(".p.p", "q.q")
				.replace(".;_;", "⁏_⁏")
			)
			await sleep(0.5)
			await event.edit(str_orig
				.replace(".. _ .", ". _ .")
				.replace("..-.", ".–.")
				.replace(".p.p", "p.p")
				.replace(".;_;", ";_;")
			)
			await sleep(0.5)
			await event.edit(str_orig
				.replace(".. _ .", ".  _.")
				.replace("..-.", "._.")
				.replace(".p.p", "q.q")
				.replace(".;_;", "⁏_⁏")
			)
			await sleep(0.5)
			await event.edit(str_orig
				.replace(".. _ .", ". _ .")
				.replace("..-.", ".–.")
				.replace(".p.p", "p.p")
				.replace(".;_;", ";_;")
			)

client.start(phone=telephone_number)
client.run_until_disconnected()
