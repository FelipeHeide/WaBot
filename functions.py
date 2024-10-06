import requests
from groq import Groq
from googlesearch import search
from heyoo import WhatsApp
from deep_translator import GoogleTranslator




def sendMessage(message, type):
    token = 'EAACcosEiDGcBO2eJ6Fs63DCk2rswYKvAs4XZCXW2EU54A2ZAyetBhH5ZAlgXZAbgEZCbpfeCJcDqdYCYs75Nu2zxfLEHelUZC91cTukqm81ZCZBOZCNkbXqbgAaooO99xJqAqdEpb8H9n03qsKxeQK0X7e5KMJmQ9V957okEL2TPCuwxkZALOZBp0w34x3rmzPXouSokFHBjWulCzkGzblsAvlOqUP7nakIkMzWUjjQBZC3ioX1umabt8E0o'
    idNumeroTeléfono = '108450905597878'
    mensajeWa = WhatsApp(token, idNumeroTeléfono)
    if type == "text":
      mensajeWa.send_message(message, "54111524612307")
    elif type == "image":
      mensajeWa.send_image(message, "54111524612307")
    elif type == "audio": 
       mensajeWa.send_audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", "54111524612307")


client = Groq(api_key="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")

def grok_functionality(message):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",    
                "content": "You will receive a message from a WhatsApp user. Identify the user's need and respond with one of the specific tasks listed below in capital letters, followed by the relevant prompt. Do not translate any words or phrases; keep them in their original language. /n- If the user wants a word or phrase translated, respond with 'TRANSLATION_LANGUAGE: <Original Word/Phrase>'./n- If the user wants to search for an image online, and uses words like search image, find image, respond with 'IMAGE_SEARCH: <Image Search Prompt>'./n- If the user wants a definition and uses words like 'define' or 'definition', respond with 'DEFINITION: <Word>'./n- If the user requests a list of possible functions, respond with 'FUNCTIONS'./n- If the user wants a chat completion (e.g., searching for information, or chatting, or needs a text, asking a question for specific information), respond with 'CHAT_COMPLETION: <Exact User Prompt Chat>'./n- If the user wants to listen to a song, respond with 'SONG: <Song Title>'./n- If the user wants to search for information on Google (e.g., searching for links, sites), inthe case that user uses words like search, links, or specific site respond with 'GOOGLE_SEARCH: <Search Prompt For User Necessities>'./n/nRespond only with the task and prompt, nothing else. For example, if the user wants to translate 'Cat' to French, respond with 'TRANSLATION_FR: Cat'. If the user wants an image search, respond with 'IMAGE_Search: <Image Search Prompt>', and do not put in the image prompt the Exact User Prompt Chat, you should do the prompt for that specific image search. Do not mistake if the user wnats a CHAT_COMPLETION or GOOGLE_SEARCH, if user exact prompt contains words likes search, links or online then he wants a GOOGLE_SEARCH, if he just wants to talk or have a specific information then it is CHAT_COMPLETION. When writting the Search Prompt For User Necessities do not write the specific Exact User Prompt Chat, write only what he wants to search./nExact User Prompt Chat:\n" + message,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def grok_chat(message):
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",    
                "content": message,
                }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def google_search(prompt):
    search_results = search(prompt, lang="en", advanced=True, num_results=5)
    message = "Google Search Results for: '{}'\n\n".format(prompt)
    for result in search_results:
        message += "Title: {}\n".format(result.title)
        message += "URL: {}\n".format(result.url)
        message += "Description: {}\n\n".format(result.description)

    return message

def get_definition(palabra):
  url = "https://api.wordnik.com/v4/word.json/"
  endpoint = f"{url}{palabra}/definitions"
  params = {
    "limit": 1,
    "includeRelated": "false",
    "useCanonical": "false",
    "api_key": "ir2gi4h02gbswj7oxdv2qr81srt7y16fo1cx0ajyfo9htx7fy"
  }

  response = requests.get(endpoint, params=params)

  definition = response.json()[0]["text"]

  return palabra + ": "+definition

def img(mens):
  url = 'https://google.serper.dev/images'
  headers = {
    'X-API-KEY': '<x api key>',
    'Content-Type': 'application/json'
  }
  data = {'q': mens, 'hl': 'es'}

  response = requests.post(url, headers=headers, json=data)
  result = response.json()
  images = result['images']
  first_image_url = images[0]['imageUrl']
  return first_image_url

def trans(mensaje, lang):
    lengua = lang.lower()
    translated = GoogleTranslator(source='auto', target=lengua).translate(mensaje)
    textoMensaje = f"{mensaje}\n\n{lang}: {translated}"
    return textoMensaje

