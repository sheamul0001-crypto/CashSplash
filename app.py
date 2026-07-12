from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_rates(base_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"]

@app.route("/", methods=["GET", "POST"])
def home():
    currencies = ["GBP", "USD", "EUR", "JPY", "CAD", "AUD", "CHF"]
    result = None
    amount = None
    from_currency = "GBP"
    to_currency = "USD"

    if request.method == "POST":
        amount = float(request.form["amount"])
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        rates = get_rates(from_currency)
        rate = rates[to_currency]
        result = round(amount * rate, 2)

    return render_template(
        "index.html",
        result=result,
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency,
        currencies=currencies
    )

if __name__ == "__main__":
    app.run(debug=True)