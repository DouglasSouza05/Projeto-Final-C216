from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL base da API do backend
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro de cartas
@app.route('/add-card', methods=['GET'])
def add_card_form():
    return render_template('add_card.html')

@app.route('/add-card', methods=['POST'])
def add_card():
    name = request.form['name']
    cost = request.form['cost']
    rarity = request.form['rarity']
    type_ = request.form['type']
    description = request.form['description']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])

    payload = {
        'name': name,
        'cost': cost,
        'rarity': rarity,
        'type': type_,
        'description': description,
        'quantity': quantity,
        'price': price
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/addCard/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('list_cards'))
    else:
        return "Erro ao adicionar carta", 500
    

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')