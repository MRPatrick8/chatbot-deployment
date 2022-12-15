from flask import Flask, render_template, request,jsonify
from chat import get_response
import re

app = Flask(__name__)

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
    #check if text is valid (I let it for you)
    response = preprocessing(text)
    # we jsonify our response
    response = get_response(response)
    message = {"answer":response}

    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
