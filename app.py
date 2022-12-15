from flask import Flask, render_template, request,jsonify
from chat import get_response
import re
import requests
import json
from langdetect import detect

app = Flask(__name__)


class translator:
    api_url = "https://translate.googleapis.com/translate_a/single"
    client = "?client=gtx&dt=t"
    dt = "&dt=t"

    #fROM English to Kinyarwanda
    def translate(text : str , target_lang : str, source_lang : str):
        sl = f"&sl={source_lang}"
        tl = f"&tl={target_lang}"
        r = requests.get(translator.api_url+ translator.client + translator.dt + sl + tl + "&q=" + text)
        return json.loads(r.text)[0][0][0]


def process_question(text : str):

  source_lang = detect(text)
  resp = translator.translate(text=text, target_lang='en', source_lang=source_lang)
  return resp, source_lang

def process_answer(text : str, source_lang):
  resp = translator.translate(text=text, target_lang=source_lang, source_lang='en')
  return resp

# create two routes
def preprocessing(text):
    text = text.lower()
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    html_pattern = re.compile('<.*?>')
    text = url_pattern.sub(r'', text)
    text = html_pattern.sub(r'', text)
    text = re.sub(r"[^\w\d'\s]+", ' ', text)

    return text



@app.route("/",  methods=["GET"])
def index_get():
    return render_template("base.html")

@app.route("/predict",methods=["POST"])


def predict():
    text = request.get_json().get("message")
    text, SL = process_question(text)
    #check if text is valid (I let it for you)
    texte = preprocessing(text)
    response = get_response(texte)
    # we jsonify our response
    # response = get_response(response)
    response = process_answer(response, SL)
    message = {"answer":response}

    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
