import discord
import os
import requests
import random
import csv
import wikipediaapi
from keep_alive import keep_alive
from random_word import RandomWords

my_secret = os.environ['TOKEN']

r = RandomWords()

wiki_wiki = wikipediaapi.Wikipedia('en')

client = discord.Client()

with open('Data/anime.csv', newline='') as f:
    reader = csv.reader(f)
    anime = list(reader)

with open('Data/FamousPeople.csv', newline='') as f:
    reader = csv.reader(f)
    famous_people = list(reader)

with open('Data/medical.csv', newline='') as f:
    reader = csv.reader(f)
    medical = list(reader)

def get_noun():
  return r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun, verb")

def get_anime():
  return random.choice(anime)[1]

def get_famous_person():
  return random.choice(famous_people)[0]

def get_medical():
  return random.choice(medical)[0]

def valid_link(link):
  
  request = requests.get(link)
  if request.status_code == 200:
    return True
  else:
    return False

def get_word(num):
  if num < 4:
    return get_noun()
  elif num < 7:
    return get_anime()
  elif num < 9:
    return get_famous_person()
  else:
    return get_medical()

def choose_word():
  num = random.randint(0,9)
  enough_data = False
  word = get_word(num)
  while word == None:
    word = get_word(num)
  page_py = wiki_wiki.page(word)
  enough_data = get_text(page_py)

  while page_py.exists() == False and enough_data == False:
    num = random.randint(0,9)
    word = get_word(num)
    while word == None:
      word = get_word(num)
    page_py = wiki_wiki.page(word)
    enough_data = get_text(page_py)

  return word, page_py.fullurl

def get_text(page_py):
  print(len(page_py.text))
  return len(page_py.text) > 50000

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='$WHelp'))
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
    await client.send_message("  ")
    if before.voice_channel is None and after.voice_channel is not None:
      for channel in before.server.channels:
          if channel.name == '///':
              await client.send_message(channel, "Howdy")

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
    await message.channel.send('=============================================================')
    await message.channel.send(end)
    await message.channel.send(end_link)
    await message.channel.send('------------------------------------------------------------')
    await message.channel.send("$Rules - **To View Rules**")

  if msg.startswith('$Rules'):
    await message.channel.send("Kyle")

  if msg.startswith('$WHelp'):
    await message.channel.send("U Stupid?")

  if msg.startswith('$Random'):
    msg = msg.split(',')
    choices = [msg[0].split()[1]]
    
    if len(msg) > 1:
        choices += msg[1:]
        
    choice = start = '**Choice :) **' + str(random.choice(choices))
    await message.channel.send(choice)

  if msg.startswith('$Rope'):
    await message.channel.send("same brother")

  if msg.startswith('$RIP'):
    await message.channel.send("same brother")
  
  if msg.startswith('$Valorant'):
    await message.channel.send("@OrangeChicken#1754 Val?")
    await message.channel.send("@ps Val?")
    await message.channel.send("Cyrus Sux")


keep_alive()
client.run(my_secret)
