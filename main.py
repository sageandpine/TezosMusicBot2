# Tezos_Music_Bot pulls a random music mp3 NFT from hic dex and displays it in discord chat with a link and info when $music is called.

#TO DO: Play music in Voice channel?
#To Do: Add Tunes to database
# To Do: Rate Limiting

import random
import os
import discord
from replit import db
from keep_alive import keep_alive
import requests
import json
import pandas as pd

my_secret = os.environ['BotKey']
client  = discord.Client()


def get_rand_music(number):
  """Returns a Random NFT Music from the HicDex API. exclude burn wallet"""
  query = """query GetAllTrackIds {
  hic_et_nunc_token(where: {mime: {_in: ["audio/ogg", "audio/wav", "audio/mpeg"]}, token_holders: {quantity: {_gt: "0"}, holder_id: {_neq: "tz1burnburnburnburnburnburnburjAYjjX"}}}, limit: 25) {
    id
  }
}

"""
  # post query to hicdex
  url = 'https://api.hicdex.com/v1/graphql'
  r = requests.post(url, json={'query': query})
  json_data = json.loads(r.text)
  # Convert to DataFrame
  df = pd.DataFrame(json_data)
  #Access token number and store in variable
  df_objkt_id = df["data"]["hic_et_nunc_token"][number]["id"]
  # Format into a string to be returned by function
  #link_string = f"https://hen.radio/objkt/{df_objkt_id}"
  link_string = f"https://hic.art/{df_objkt_id}"
  print(link_string)
  return link_string


@client.event
async def on_ready():
  """Send message when bot logs on"""
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  """Defines action in Discord when bot recieves commands"""
  if message.author == client.user:
    return

  if message.content.startswith('$music'):
    num = random.randrange(0,10)
    rand_music = get_rand_music(num)
    #update_objkt_list(rand_music) 
    await message.channel.send(rand_music)

keep_alive()
client.run(my_secret)