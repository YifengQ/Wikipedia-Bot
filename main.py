import discord
import os
import requests
import random
import csv
from keep_alive import keep_alive
from random_word import RandomWords
my_secret = os.environ['TOKEN']
r = RandomWords()
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
  word = get_word(num).join('_')
  link = 'https://en.wikipedia.org/wiki/' + word

  while valid_link(link) == False:
    num = random.randint(0,9)
    word = get_word(num).join('_')
    link = 'https://en.wikipedia.org/wiki/' + word

  return word, link


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
    await message.channel.send('=============================================================')
    await message.channel.send(end)
    await message.channel.send(end_link)
    await message.channel.send("$Rules - **To View Rules**")
    print(get_anime())
    print(get_famous_person())
    print(get_medical())

    if msg.startswith('$Rules'):
      await message.channel.send("Kyle")

client.run(my_secret)
