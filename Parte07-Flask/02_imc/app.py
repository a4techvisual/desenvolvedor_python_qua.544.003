from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/imc", methods=["GET", "POST"])
def calcular_imc():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()

        try:
            massa = float(request.form.get("massa", ""))
            altura = float(request.form.get("altura", ""))
        except ValueError:
            return render_template("index.html", erro="Informe valores numéricos válidos.")

        if massa <= 0 or altura <= 0:
            return render_template("index.html", erro="Massa e altura devem ser maiores que zero.")

        imc = massa / (altura ** 2)

        if imc < 18.5:
            classificacao = "Abaixo do peso"
            gif = "baixo-peso.gif"
        elif imc < 25:
            classificacao = "Peso normal"
            gif = "peso-normal.gif"
        elif imc < 30:
            classificacao = "Acima do peso"
            gif = "acima-peso.gif"
        elif imc < 35:
            classificacao = "Obesidade grau I"
            gif = "obesidade-grau-1.gif"
        elif imc < 40:
            classificacao = "Obesidade grau II"
            gif = "obesidade-grau-2.gif"
        else:
            classificacao = "Obesidade grau III"
            gif = "obesidade-grau-3.gif"

        result = f"{nome}, seu IMC é {imc:.2f} — {classificacao}."

        return render_template(
            "index.html",
            result=result,
            gif=gif,
            classificacao=classificacao,
            imc=imc
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
