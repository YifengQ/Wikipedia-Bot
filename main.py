import discord
import os
import requests
import random
import fileinput
from keep_alive import keep_alive
from random_word import RandomWords
my_secret = os.environ['TOKEN']
r = RandomWords()
client = discord.Client()

def get_noun():
  return r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun, verb")

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
    await message.channel.send("$Rules - **To View Rules**")
    if msg.startswith('$Rules'):
      await message.channel.send("Kyle")

client.run(my_secret)
