import discord
import os
import requests
import random
from replit import db
from keep_alive import keep_alive
from random_word import RandomWords
my_secret = os.environ['TOKEN']
r = RandomWords()
client = discord.Client()

def get_noun():
  return r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun")

def valid_link(link):
  
  request = requests.get(link)
  if request.status_code == 200:
    return True
  else:
    return False

def choose_word():
  word = get_noun()
  while word == None:
    word = get_noun()
  link = 'https://en.wikipedia.org/wiki/' + word

  while valid_link(link) == False:
    word = get_noun()
    while word == None:
      word = get_noun()
    link = 'https://en.wikipedia.org/wiki/' + word

  return word, link

# def print_message(message, start_word, start_link, end_word, end_link):

#     start = '**Start Word: **' + start_word
#     end = '**End Word: **' + end_word
#     message.channel.send(start)
#     message.channel.send(start_link)
#     message.channel.send('====================================================================================')
#     message.channel.send(end)
#     message.channel.send(end_link)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$Wiki'):
    start_word, start_link = choose_word()
    end_word, end_link = choose_word()
    start = '**Start Word: **' + start_word
    end = '**End Word: **' + end_word
    await message.channel.send(start)
    await message.channel.send(start_link)
    await message.channel.send('====================================================================================')
    await message.channel.send(end)
    await message.channel.send(end_link)

client.run(my_secret)

 # if db["responding"]:
  #   options = starter_encouragements
  #   if "encouragements" in db.keys():
  #     options = options + db["encouragements"]

  #   if any(word in msg for word in sad_words):
  #     await message.channel.send(random.choice(options))

  # if msg.startswith("$new"):
  #   encouraging_message = msg.split("$new ",1)[1]
  #   update_encouragements(encouraging_message)
  #   await message.channel.send("New encouraging message added.")

  # if msg.startswith("$del"):
  #   encouragements = []
  #   if "encouragements" in db.keys():
  #     index = int(msg.split("$del",1)[1])
  #     delete_encouragment(index)
  #     encouragements = db["encouragements"]
  #   await message.channel.send(encouragements)

  # if msg.startswith("$list"):
  #   encouragements = []
  #   if "encouragements" in db.keys():
  #     encouragements = db["encouragements"]
  #   await message.channel.send(encouragements)

  # if msg.startswith("$responding"):
  #   value = msg.split("$responding ",1)[1]

  #   if value.lower() == "true":
  #     db["responding"] = True
  #     await message.channel.send("Responding is on.")
  #   else:
  #     db["responding"] = False
  #     await message.channel.send("Responding is off.")
