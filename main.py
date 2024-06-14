from flask import Flask, request, jsonify
import functions

app = Flask(__name__)



@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == "<webhook password>":
            return request.args.get('hub.challenge')
        else:
            return "Error de autentificacion."

    if request.method == "POST":
        data = request.get_json()
        if data:
            try:
                tipo_msg = data['entry'][0]['changes'][0]['value']['messages'][0]['type']
                data['entry'][0]['changes'][0]['value']['messages'][0]['type']

                if tipo_msg == "text":
                    mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                    func_response = functions.grok_functionality(mensaje)
                    functions.sendMessage(func_response, "text")
                    if func_response.startswith('TRANSLATION_'):
                        parts = func_response.split(': ')
                        language = parts[0].split('_')[1]
                        text = parts[1]
                        functions.sendMessage(functions.trans(text, language), "text")
                    elif func_response.startswith('IMAGE_SEARCH'):
                        query = func_response.split('IMAGE_SEARCH: ')[1]
                        functions.sendMessage(functions.img(query), "image")
                    elif func_response.startswith('DEFINITION'):
                        word = func_response.split('DEFINITION: ')[1]
                        functions.sendMessage(functions.get_definition(word), "text")
                    elif func_response.startswith('CHAT_COMPLETION'):
                        chat_prompt = func_response.split('CHAT_COMPLETION: ')[1]
                        functions.sendMessage(functions.grok_chat(chat_prompt), "text")
                    elif func_response.startswith('GOOGLE_SEARCH'):
                        search_prompt = func_response.split('GOOGLE_SEARCH: ')[1]
                        functions.sendMessage(functions.google_search(search_prompt), "text")
                    elif func_response.startswith('FUNCTIONS'):
                        functions.sendMessage("Our Functions are the following:\n\nTRANSLATION_LANGUAGE: Translate words or text in any language you want.\nIMAGE_SEARCH: Search for any image you want.\nDEFINITION: Get the definition of any word.\nCHAT_COMPLETION: Continue a conversation on any topic.\nGOOGLE_SEARCH: Search Google for any topic and get relevant links.\nSONG: Play any song you want.\nFUNCTIONS: Get a list of all available functions.", "text")
                    elif func_response.startswith('SONG'):
                        song_title = func_response.split('SONG: ')[1]
                        functions.sendMessage(song_title, "audio")
                   


                        
            except KeyError as e:
                print(f"KeyError: {e}")
        
        return "Webhook received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

