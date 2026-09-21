from flask import Flask, render_template, request
import easyocr
from PIL import Image
import numpy as np

app = Flask(__name__)

reader = easyocr.Reader(['pt'], gpu=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/textoExtraido", methods=["GET", "POST"])
def extrair_texto():

    texto = ""

    if request.method == "POST":

        imagem = request.files.get("imagem")

        if imagem and imagem.filename:

            try:
                imagem_pil = Image.open(imagem)
                imagem_array = np.array(imagem_pil)

                resultado = reader.readtext(imagem_array)

                textos = []

                for deteccao in resultado:
                    textos.append(deteccao[1])

                texto = "\n".join(textos)

                if not texto.strip():
                    texto = "Não foi possível encontrar texto na imagem."

            except Exception as erro:
                texto = f"Erro ao processar a imagem: {erro}"

    return render_template("textoExtraido.html", texto=texto)


if __name__ == "__main__":
    app.run(debug=True)