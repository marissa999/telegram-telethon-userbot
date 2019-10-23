import sys
import re
import random
from random import random
import asyncio
from asyncio import sleep
from telethon import *
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from urlextract import URLExtract

# Import settings
import env

########################

def probability(percent):
	outcome = random() < percent
	return outcome

# parse account from cli
if len(sys.argv) != 3:
	print("You need to specify an account name and a phone number!")
	exit()

account_file = sys.argv[1]
telephone_number = sys.argv[2]
	
client = TelegramClient(account_file, env.api_id, env.api_hash)

# Initialise extractor
extractor = URLExtract()

@client.on(events.NewMessage(outgoing=True))
async def self(event):
	message_string = event.text
	
	# Update TLD list when list is 120 days old
	extractor.update_when_older(120)
		
	if "@all" in message_string:
		await event.delete()
		all_participants = await client.get_participants(event.message.chat_id)
		mention_string = "[@all](tg://need_update_for_some_feature)"
		for user in all_participants:
			mention_string += "[⁣](tg://user?id=" + str(user.id) + ")"
		message_string = message_string.replace("@all", mention_string)
		await client.send_message(event.message.chat_id, message_string)
		return

	words = message_string.split()
	mirrored_letters = ['o', 'u']
	for letter in mirrored_letters:
		for wordnumber, word in enumerate(words):
			if extractor.has_urls(word):
				continue
			elif letter in word:
				for i, c in enumerate(word):
					if word[i] == letter and probability(0.002):
						words[wordnumber] = word[:i] + letter + "w" + letter + word[i + 1:]
	message_string = " ".join(words)

	if message_string != event.text:
		await event.edit(message_string)

	if ".. _ ." in message_string or "..-." in message_string:
		str_orig = message_string
		new_message = str_orig.replace(".. _ .", ". _ .").replace("..-.", ".–.")
		await event.edit(new_message)
		for _ in range(10):			   
			await sleep(0.5)
			await event.edit(str_orig.replace(".. _ .", "._  .").replace("..-.", "._."))
			await sleep(0.5)
			await event.edit(str_orig.replace(".. _ .", ". _ .").replace("..-.", ".–."))
			await sleep(0.5)
			await event.edit(str_orig.replace(".. _ .", ".  _.").replace("..-.", "._."))
			await sleep(0.5)
			await event.edit(str_orig.replace(".. _ .", ". _ .").replace("..-.", ".–."))
						
client.start(phone=telephone_number)
client.run_until_disconnected()
