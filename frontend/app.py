from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL base da API do backend
API_BASE_URL = "http://backend:8000"


# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")


# Rota para exibir o formulário de cadastro de cartas
@app.route("/add-card-form", methods=["GET"])
def add_card_form():
    return render_template("add_card.html")


@app.route("/add-card", methods=["POST"])
def add_card():
    name = request.form["name"]
    cost = request.form["cost"]
    rarity = request.form["rarity"]
    type_ = request.form["type"]
    description = request.form["description"]
    quantity = int(request.form["quantity"])
    price = float(request.form["price"])

    payload = {
        "name": name,
        "cost": cost,
        "rarity": rarity,
        "type": type_,
        "description": description,
        "quantity": quantity,
        "price": price,
    }

    response = requests.post(f"{API_BASE_URL}/api/v1/addCard/", json=payload)

    if response.status_code == 201:
        return redirect(url_for("list_cards"))
    else:
        return "Erro ao adicionar carta", 500


@app.route("/list-cards", methods=["GET"])
def list_cards():
    response = requests.get(f"{API_BASE_URL}/api/v1/listCards/")
    try:
        cards = response.json()
    except:
        cards = []
    return render_template("list_cards.html", cards=cards)


@app.route("/update-card/<int:card_id>", methods=["GET"])
def update_card_form(card_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/listCards/")
    cards = [card for card in response.json() if card["id"] == card_id]
    if len(cards) == 0:
        return "Carta não encontrada", 404
    card = cards[0]
    return render_template("update_card.html", card=card)


@app.route("/update-card/<int:card_id>", methods=["POST"])
def update_card(card_id):
    rarity = request.form["rarity"]
    quantity = int(request.form["quantity"])
    price = float(request.form["price"])

    payload = {"rarity": rarity, "quantity": quantity, "price": price}

    response = requests.patch(
        f"{API_BASE_URL}/api/v1/updateCard/{card_id}", json=payload
    )

    if response.status_code == 200:
        return redirect(url_for("list_cards"))
    else:
        return "Erro ao atualizar carta", 500


@app.route("/sell-card/<int:card_id>", methods=["GET"])
def sell_card_form(card_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/listCards/")
    cards = [card for card in response.json() if card["id"] == card_id]
    if len(cards) == 0:
        return "Carta não encontrada", 404
    card = cards[0]
    return render_template("sell_card.html", card=card)


@app.route("/sell-card/<int:card_id>", methods=["POST"])
def sell_card(card_id):
    quantity = int(request.form["quantity"])

    payload = {"quantity": quantity}

    response = requests.put(f"{API_BASE_URL}/api/v1/sellCard/{card_id}", json=payload)

    if response.status_code == 200:
        return redirect(url_for("list_cards"))
    else:
        return "Erro ao vender carta", 500


@app.route("/list-sales", methods=["GET"])
def list_sales():
    response = requests.get(f"{API_BASE_URL}/api/v1/listSales/")
    try:
        sales = response.json()
    except:
        sales = []
    total_sales = sum(float(sale["sale_value"]) for sale in sales)
    return render_template("list_sales.html", sales=sales, total_sales=total_sales)


@app.route("/delete-card/<int:card_id>", methods=["POST"])
def delete_card(card_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/deleteCard/{card_id}")

    if response.status_code == 200:
        return redirect(url_for("list_cards"))
    else:
        return "Erro ao excluir carta", 500


@app.route("/reset-database", methods=["GET"])
def reset_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/resetDatabase/")

    if response.status_code == 200:
        return render_template("reset.html")
    else:
        return "Erro ao resetar o banco de dados", 500


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")
