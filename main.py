import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

reply_words = ["ok", "Ok", "pong", "Pong", "test", "Test"]

starter_replies = ["ok", "why", "no"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_replies(reply_message):
  if "replies" in db.keys():
    replies = db["replies"]
    replies.append(reply_message)
    db["replies"] = replies
  else:
    db["replies"] = [reply_message]

def delete_reply(index):
  replies = db["replies"] 
  if len(replies) > index:
    del replies[index]
    db["replies"] = replies

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
      return

    msg = message.content

    if message.content.startswith('$ping'):
      await message.channel.send('Pong!')

    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)
    
    if db["responding"]:
      options = starter_replies
      if "replies" in db.keys():
        options = options + db["replies"]
      
      if any(word in msg for word in reply_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$newreply"):
      reply_message = msg.split("$newreply ",1)[1]
      update_replies(reply_message)
      await message.channel.send("New reply added!")

    if msg.startswith("$delreply"):
      replies = []
      if "replies" in db.keys():
        index = int(msg.split("$delreply",1)[1])
        delete_reply(index)
        replies = db["replies"]
        await message.channel.send(replies)

    if msg.startswith("$listreplies"):
      replies =[]
      if "replies" in db.keys():
        replies = db["replies"]
        await message.channel.send(replies)

    if msg.startswith("$responding"):
      value = msg.split("$responding ",1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))

