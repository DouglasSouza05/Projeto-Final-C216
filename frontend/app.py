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