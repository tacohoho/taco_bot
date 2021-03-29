import discord
import os
import requests
# if the data returned is in json
import json
import random
from keep_alive import keep_alive
import time

# create instance of Client | this is the connection to Discord
client = discord.Client()

# Urbana Dictionary API stuff
UD_KEY = os.getenv("UD_KEY")
UD_URL = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
querystring = {"term": "word"}
headers = {
    'x-rapidapi-key': UD_KEY,
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }


sad_words = ["sad", "depress", "unhappy", "miserable"]
roles = ["ADC", "TOP", "MID", "SUP", "JG"]

starter_encouragements = [
  "HEY! Don't be sad. Don't make me beat you up >:(",
  "If you cry, I'mma slap you! DON'T DO IT!!!",
  "Well, it sucks that you're sad, but at least you have a big schlong"
]

champions = {
  "TOP": ["Malphite", "Darius", "Renekton", "Maokai", "Gnar", "Aatrox", "Volibear", "Fiora", "Shen", "Jayce", "Sylas", "Poppy", "Garen", "Sion", "Viego", "Nasus", "Camille", "Wukong", "Pantheon", "Riven", "Nocturne", "Urgot", "Kled", "Ornn", "Rengar", "Sett", "Viktor", "Gangplank", "Quinn", "Yasuo", "Irelia", "Kayle", "Cho'Gath", "Jax", "Teemo", "Akali", "Singed", "Mordekaiser", "Heimerdinger", "Gragas", "Tryndamere", "Vayne", "Cassiopeia", "Kennen", "Lucian", "Zac", "Vladmir", "Yone", "Ryze", "Rumble", "Illaoi", "Sejuani", "Warwick", "Kalista"],
  "JG": ["Hecarim", "Elise", "Karthus", "Shaco", "Udyr", "Fiddlesticks", "Poppy", "Rek'sai", "Nidalee", "Lee Sin", "Eveylynn", "Dr. Mundo", "Taliyah", "Nunu & Willump", "Volibear", "Viego", "Warwick", "Kha'Zix", "Rammus", "Xin Zhao", "Skarner", "Olaf", "Gragas", "Graves", "Vi", "Wukong", "Ekko", "Kayn", "Nocturne", "Kindred", "Master Yi", "Ivern", "Lillia", "Zac", "Rengar", "Jarvan IV", "Sejuani", "Shyvana", "Jax", "Trundle"],
  "MID": ["Talon", "Zed", "Katarina", "Anivia", "Galio", "Pantheon", "Twisted Fate", "Ahri", "Veigo", "Qiyana", "Kassadin", "Sylas", "Yone", "Fizz", "Yasuo", "LeBlanc", "Renekton", "Zoe", "Akali", "Annie", "Ekko", "Seraphine", "Aurelion Sol", "Neeko", "Tristana", "Cassiopeia", "Nocturne", "Kled", "Garen", "Veigar", "Zilean", "Viktor", "Malzahar", "Rumble", "Jayce", "Orianna", "Xerath", "Malphite", "Diana", "Corki", "Lucian", "Irelia", "Syndra", "Cho'Gath", "Azir", "Lissandra", "Ryze", "Aatrox", "Sett", "Vladmir", "Lux", "Nunu & Willump", "Xin Zhao"],
  "ADC": ["Kai'sa", "Jinx", "Samira", "Tristana", "Sivir", "Swain", "Ezreal", "Vayne", "Caitlyn", "Jhin", "Lucian", "Kalista", "Xayah", "Draven", "Ashe", "Miss Fortune", "Twitch", "Aphelios", "Senna", "Varus", "Kog'Maw"],
  "SUP": ["Leona", "Thresh", "Alistar", "Blitzcrank", "Maokai", "Lulu", "Senna", "Rell", "Morgana", "Nautilus", "Zilean", "Shaco", "Galio", "Bard", "Pyke", "Seraphine", "Yuumi", "Janna", "Zyra", "Rakan", "Pantheon", "Swain", "Gragas", "Xerath", "Soraka", "Anivia", "Karma", "Poppy", "Brand", "Braum", "Taric", "Sett", "Neeko", "Nami", "Lux", "Zac", "Vel'Koz", "Veigar", "Shen", "Fiddlesticks", "Sona"]
}

# anime, character, quote
anime_info = []
game_ongoing = False
start_time = time.time()
end_time = time.time()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def get_animes():
  response = requests.get("https://animechan.vercel.app/api/available/anime")
  json_data = json.loads(response.text)
  print(json_data)
  return json_data

def get_anime_quote(message):
  # split command and anime argument
  anime = message.split(" ", 1)

  # changes spaces to +
  anime_url = anime[1].replace(" ", "+")

  response = requests.get("https://animechan.vercel.app/api/quotes/anime?title=" + anime_url)
  json_data = json.loads(response.text)

  if "error" in json_data:
    return False
  else:
    rand = random.randint(0, len(json_data) - 1)
    anime_info.append(json_data[rand]['anime'])
    anime_info.append(json_data[rand]['character'])
    anime_info.append(json_data[rand]['quote'])
    return True

def anime_quiz(message):
  global game_ongoing
  names = anime_info[1].split()

  # if the whole name is correct
  if message.content.lower() == anime_info[1]:
    game_ongoing = False
    return "{} got the character right!".format(message.author)

  # if part of the name is correct
  for name in names:
    if message.content.lower() == name.lower():
      game_ongoing = False
      return "{} got the character right!".format(message.author)

  global end_time
  end_time = time.time()

  # if run out of time
  if end_time - start_time > 15.0 and game_ongoing:
    game_ongoing = False
    return "The character was {} from the anime {}".format(anime_info[1], anime_info[0])

  return "WRONG!"

def random_role():
  if len(roles) == 0:
    roles.append("ADC")
    roles.append("TOP")
    roles.append("MID")
    roles.append("SUP")
    roles.append("JG")
    
  rand = random.randint(0, len(roles) - 1)
  role = roles[rand]
  roles.pop(rand)
  return role

# $champ adc
def get_champ(message):
  commands = message.split()
  role = ""

  if commands[0] != "$champ" or len(commands) > 2:
    return "Please submit a valid command. Provide no roles for a random champion\nEx) $champ\n Or provide a role for a random champion in the specified role\nEx) $champ mid"

  if len(commands) == 1:
    role = random_role()

  elif len(commands) == 2:
    role = commands[1].upper()

    if not role in champions:
      return "Please give a valid role: top, mid, jg, adc, sup"

  champs = champions[role]
  rand = random.randint(0, len(champs) - 1)
  return champs[rand]

def get_image(message):
  category = message.replace('$', '')
  if category == "catgirl":
    category = "neko"

  response = requests.get("https://waifu.pics/api/sfw/" + category)
  json_data = json.loads(response.text)
  return json_data["url"]

"""
def find_top_def(json_data):
  index = 0
  size = len(json_data["list"])

  for i in range(size):
    new_list = json_data["list"][i]
    top_list = json_data["list"][index]

    if new_list["thumbs_up"] - new_list["thumbs_down"] > top_list["thumbs_up"] - top_list["thumbs_down"]:
      index = i
  
  return index
"""
def find_random_def(json_data):
  rand = random.randint(0, len(json_data["list"]) - 1)
  return rand

def get_definition(message):
  commands = message.split(' ', 1)

  if len(commands) == 1:
    return "Please provide a word to define\nEx) $define hobo"

  word = commands[1]
  querystring["term"] = word
  response = requests.getresponse = requests.request("GET", UD_URL, headers=headers, params=querystring)
  json_data = json.loads(response.text)
  
  if len(json_data["list"]) == 0:
    return "Word not found on Urban Dictionary"

  index = find_random_def(json_data)
  definition = json_data["list"][index]["definition"].replace('[', '').replace(']', '')
  example = json_data["list"][index]["example"].replace('[', '').replace(']', '')
  return "**Definition**: " + definition + "\n**Example**:\n" + example

# register event
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.change_presence(activity=discord.Game('$help'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  global game_ongoing

  if game_ongoing:
    await message.channel.send(anime_quiz(message))
  else:
    anime_info.clear()

  if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith("$"):
    if msg == "$quote":
      quote = get_quote()
      await message.channel.send(quote)

    elif msg.startswith("$role"):
      role = random_role()
      await message.channel.send(role)
    
    elif msg.startswith("$animequiz"):
      commands = msg.split()

      if len(commands) > 1:

        if get_anime_quote(msg):
          await message.channel.send(anime_info[2])
          global start_time
          start_time = time.time()
          game_ongoing = True
        
        else:
          await message.channel.send("This anime is not in the database")

      else:
        await message.channel.send("Please give an anime you would like a quote for.\n Ex) $animequiz one piece")

    elif msg.startswith("$animes"):
      animes = get_animes()
    #  for anime in animes:
    #    await message.channel.send(anime)

    elif msg.startswith("$game?"):
      rand = random.randint(0, 1)
      
      if rand == 0:
        await message.channel.send("Valorant")
      else:
        await message.channel.send("League of Legends") 

    elif msg.startswith("$champ"):
      await message.channel.send(get_champ(msg))

    elif msg.startswith("$define"):
      await message.channel.send(get_definition(msg))

    elif msg.startswith("$catgirl") or msg.startswith("$megumin") or msg.startswith("$shinobu") or msg.startswith("$cry") or msg.startswith("$cringe") or msg.startswith("$blush") or msg.startswith("$waifu") or msg.startswith("$bully") or msg.startswith("$cuddle") or msg.startswith("$hug") or msg.startswith("$awoo") or msg.startswith("$kiss") or msg.startswith("$lick") or msg.startswith("$pat") or msg.startswith("$smug") or msg.startswith("$bonk") or msg.startswith("$yeet") or msg.startswith("$smile") or msg.startswith("$wave") or msg.startswith("$highfive") or msg.startswith("$handhold") or msg.startswith("$nom") or msg.startswith("$bite") or msg.startswith("$glomp") or msg.startswith("$kill") or msg.startswith("$slap") or msg.startswith("$happy") or msg.startswith("$wink") or msg.startswith("$poke") or msg.startswith("$dance"):
      await message.channel.send(get_image(msg))

    elif msg.startswith("$help"):
      commands = msg.split()
      if len(commands) == 1:
        await message.channel.send("**$quote** is for some zen quotes\n" 
        "**$role** is for random league roles so we don't have to pick some random shit last second\n"
        "**$champ** gives a random champion from League of Legends. You can also add a role at the end to get a champion from that specific role\n"
        "**$animequiz** is where you give an anime and given a random quote from that anime. Try and guess who said it!\n"
        "**$game?** Chooses between League of Legends and Valorant\n"
        "**$define** Finds a defintion and example from Urban Dictionary\n"
        "**$help images** to see commands to send images\n")

      if msg.startswith("$help images"):
        await message.channel.send("**$catgirl**\n**$shinobu**\n**$megumin**\n**$cry**\n**$cringe**\n**$blush**\n**$waifu**\n**$bully**\n**$cuddle**\n**$hug**\n**$awoo**\n**$kiss**\n**$lick**\n**$pat**\n**$smug**\n**$bonk**\n**$yeet**\n**$smile**\n**$wave**\n**$highfive**\n**$handhold**\n**$nom**\n**$bite**\n**$glomp**\n**$kill**\n**$slap**\n**$happy**\n**$wink**\n**$poke**\n**$dance**\n")

    else:
      await message.channel.send("Please submit a valid command. You can type **$help** to see the list of commands")    

keep_alive()
client.run(os.getenv("TOKEN"))