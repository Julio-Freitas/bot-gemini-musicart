from flask import Flask, render_template, request, Response
from bot import bot
import os
import uuid
import config

app = Flask(__name__)
app.secret_key = "alura"
UPLOAD_FOLDER = "imagens_temporarias"


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    response = bot(prompt)
    return response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload_imagem", methods=["POST"])
def upload_imagem():
    global path_img
    if "imagem" in request.files:
        path_img = request.files["imagem"]
        file_name = str(uuid.uuid4()) + os.path.splitext(path_img.filename)[1]
        path_file = os.path.join(UPLOAD_FOLDER, file_name)
        path_img.save(path_file)
        path_img = path_file
        config.path_img = path_file
        return "Imagem enviada com sucesso", 200
    return "Nenhum arquivo enviado", 400


if __name__ == "__main__":
    app.run(debug=True)
