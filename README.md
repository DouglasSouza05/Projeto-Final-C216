# Loja de Card Games - Projeto Final

Este é o repositório do projeto **Loja de Card Games**, desenvolvido como parte do projeto final da disciplina de C216. A aplicação foi criada utilizando **Flask** para o frontend e **API RESTful** para o backend, com integração Docker para fácil execução. 

## Objetivo do Projeto

O objetivo deste projeto é criar uma aplicação que permita:
- Cadastrar cartas de jogos de card games.
- Visualizar o estoque de cartas cadastradas.
- Atualizar informações das cartas.
- Realizar vendas de cartas.
- Consultar o histórico de vendas.
- Resetar o banco de dados.

## Funcionalidades

- Interface gráfica estilizada utilizando **Bootstrap** e CSS customizado.
- Integração com um backend para persistência dos dados.
- Navegação intuitiva com barra lateral e animações.

---

## Como Rodar o Projeto

Certifique-se de que você tem o **Docker** e o **Docker Compose** instalados na sua máquina.

### 1. Clone o Repositório

Faça o clone do repositório para sua máquina local:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Build e Inicialização do Projeto com Docker

No diretório raiz do projeto, execute os seguintes comandos:

```bash
docker-compose up --build
```

## Testes de API com Postman

### Etapas para Testar a API

1. Abra o **Postman**.
2. Importe a **collection** do Postman localizada no diretório `/postman/collection.json`.
3. Configure o ambiente no Postman para apontar para o endereço local onde o Docker está rodando (por exemplo, `http://localhost:8000`).
4. Execute os testes disponíveis na coleção.

### Export dos Resultados

Os resultados dos testes realizados podem ser encontrados no diretório `/postman`.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
PROJETO-FINAL-C216/
├── backend/
│   ├── db/
│   │   ├── init.sql
│   ├── Dockerfile
│   ├── main.py
├── frontend/
│   ├── static/
│   │   ├── add_card.css
│   │   ├── index.css
│   │   ├── list_cards.css
│   │   ├── list_sales.css
│   │   ├── reset.css
│   │   ├── sell_card.css
│   │   ├── styles.css
│   │   ├── update_card.css
│   ├── templates/
│   │   ├── add_card.html
│   │   ├── index.html
│   │   ├── list_cards.html
│   │   ├── list_sales.html
│   │   ├── reset.html
│   │   ├── sell_card.html
│   │   ├── update_card.html
│   ├── app.py
│   ├── Dockerfile
├── postman/
│   ├── Projeto-Final-C216.postman_collection.json
├── .gitignore
├── docker-compose.yaml
├── LICENSE
├── README.md
```
### Descrição dos Diretórios

- **backend/**: Contém os arquivos do backend, incluindo o banco de dados e o arquivo `main.py` para inicialização do servidor.
- **frontend/**: Diretório do frontend, dividido em:
  - **static/**: Estilos em CSS para as diferentes páginas da aplicação.
  - **templates/**: Arquivos HTML para renderização das páginas.
  - `app.py`: Arquivo principal que gerencia as rotas e lógica do frontend.
- **postman/**: Diretório que contém a coleção de testes do Postman.
- `docker-compose.yaml`: Arquivo de configuração para subir os containers Docker.
- `LICENSE`: Licença do projeto.
- `README.md`: Documentação explicando o projeto, como rodar, e outras informações relevantes.

## Funcionalidades do Frontend

- **Página Inicial**: Apresenta uma mensagem de boas-vindas e links para as principais funcionalidades.
- **Cadastro de Cartas**: Permite cadastrar novas cartas com campos como nome, custo convertido, raridade, tipo, descrição, quantidade e preço.
- **Estoque de Cartas**: Lista todas as cartas cadastradas, com opções para atualizar, excluir ou vender cartas.
- **Histórico de Vendas**: Mostra o histórico de todas as vendas realizadas, com informações como valor e data.
- **Resetar Banco de Dados**: Opção para resetar todo o banco de dados.

## Tecnologias Utilizadas

- **Frontend**: Flask, Bootstrap, CSS
- **Backend**: Flask RESTful API
- **Banco de Dados**: PostgreSQL
- **Testes de Rotas**: Postman
- **Docker**: Containers para facilitar o desenvolvimento e execução

## Padrões de Commits

Esta organização segue uma convenção de commits para manter um histórico claro e consistente. Abaixo está uma tabela com os tipos de commits e suas descrições.

| Tipo de Commit | Descrição                                                                           |
|-----------------|-----------------------------------------------------------------------------------|
| `feat`          | Adição de uma nova funcionalidade                                                |
| `fix`           | Correção de um bug                                                              |
| `docs`          | Mudanças na documentação                                                        |
| `style`         | Alterações que não afetam o significado do código (espaços em branco, formatação, etc.) |
| `merge`         | Integração de branches                                                          |

# Rotas da API

## 1. Adicionar Cartas
**POST /api/v1/addCard/**  
Adiciona uma nova carta ao banco de dados ou atualiza a quantidade de uma carta já existente.

## 2. Listar Cartas
**GET /api/v1/listCards/**  
Retorna a lista de todas as cartas cadastradas no banco de dados.

## 3. Buscar Cartas pelo ID
**GET /api/v1/searchCard/{id}**  
Busca e retorna os detalhes de uma carta específica pelo seu ID.

## 4. Atualizar uma Carta
**PATCH /api/v1/updateCard/{id}**  
Atualiza os dados de uma carta (raridade, quantidade ou preço) pelo ID.

## 5. Vender uma Carta
**PUT /api/v1/sellCard/{id}**  
Reduz a quantidade de uma carta no estoque ao registrar uma venda e cria um registro da venda.

## 6. Listar Vendas
**GET /api/v1/listSales/**  
Retorna uma lista de todas as vendas realizadas, com informações detalhadas.

## 7. Remover Cartas
**DELETE /api/v1/deleteCard/{id}**  
Remove uma carta específica do banco de dados pelo seu ID.

## 8. Resetar Banco de Dados
**DELETE /api/v1/resetDatabase/**  
Restaura o banco de dados ao estado inicial definido no arquivo `init.sql`.

## Integrantes do Projeto

| Nome Completo   | Matrícula  | E-mail             |
|------------------|------------|--------------------|
| Douglas Brandão de Souza   | 1730  |  douglas.brandao@gec.inatel.br |
| Eduardo Costa Resende   | 200  | eduardo.costa@ges.inatel.br  |

