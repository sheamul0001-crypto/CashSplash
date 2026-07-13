from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_rates(base_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["rates"], None
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to exchange rate service. Check your internet connection."
    except Exception as e:
        return None, "Something went wrong fetching exchange rates. Please try again."

@app.route("/", methods=["GET", "POST"])
def home():
    currencies = ["GBP", "USD", "EUR", "JPY", "CAD", "AUD", "CHF"]
    result = None
    amount = None
    from_currency = "GBP"
    to_currency = "USD"
    error = None
    rate_display = None

    if request.method == "POST":
        amount = float(request.form["amount"])
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        rates, error = get_rates(from_currency)
        if rates:
            rate = rates[to_currency]
            result = round(amount * rate, 2)
            rate_display = round(rate, 4)
        else:
            rate_display = None

    return render_template(
        "index.html",
        result=result,
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency,
        currencies=currencies,
        rate_display=rate_display if result else None,
        error=error if request.method == "POST" and not result else None
    )

if __name__ == "__main__":
    app.run(debug=True)