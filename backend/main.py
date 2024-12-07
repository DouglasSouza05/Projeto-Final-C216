from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import time, asyncpg, os


# Conexão PostGreSQL
async def database():
    DATABASE_URL = os.environ.get(
        "PGURL", "postgres://postgres:postgres@db:5432/cardgames"
    )
    return await asyncpg.connect(DATABASE_URL)


text = "Documentação do Repositório do Projeto Loja de Card Games, Desenvolvido para o Projeto Final da Disciplina de C216 Lab. A Aplicação foi Criada Utilizando Flask para o Frontend e API RESTful para o Backend, com Integração Docker Proporcionando uma Fácil Execução. O Objetivo foi Desenvolver uma Aplicação que Permitisse aos Usuários Cadastrar Cartas de Card Games, Visualizar o Estoque, Atualizar suas Informações, Realizar Vendas de Cartas, Consultar Histórico de Vendas e, por fim, Resetar o Banco de Dados."

app = FastAPI(
    title="Card Games Store API",
    description=text,
    version="0.0.1",
    douglas_contact={
            "name": "Douglas Souza",
            "email": "douglas.brandao@gec.inatel.br",
        },
    eduardo_contact={
            "name": "Eduardo Resende",
            "email": "eduardo.costa@ges.inatel.br",
        },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
        "identifier": "MIT",
    },
    docs_url="/docs",
    redoc_url=None,
)


class Card(BaseModel):
    name: str
    cost: str
    rarity: str
    type: str
    description: str
    quantity: int
    price: float


class SoldCard(BaseModel):
    quantity: int


class UpdatedCard(BaseModel):
    rarity: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None


# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s"
    )
    return response


async def cardsExists(conn: asyncpg.Connection, name: str):
    try:
        query = "SELECT * FROM cardgames WHERE LOWER(name) = LOWER($1)"
        result = await conn.fetchval(query, name)
        return result is not None
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha na verificação da Carta: {str(e)}"
        )


# 1. Adicionar Cartas
@app.post("/api/v1/addCard/", status_code=201)
async def registerCards(card: Card):

    conn = await database()
    if await cardsExists(conn, card.name):
        query = """
                UPDATE cardgames
                SET quantity = quantity + $1
                WHERE LOWER(name) = LOWER($2)
                RETURNING quantity;
            """
        newQuantity = await conn.fetchval(query, card.quantity, card.name)
        return {
            "message": f"Carta existente: {card.name}. Quantidade atualizada para {newQuantity}!"
        }

    try:
        query = "INSERT INTO cardgames (name, cost, rarity, type, description, quantity, price) VALUES ($1, $2, $3, $4, $5, $6, $7)"
        async with conn.transaction():
            await conn.execute(
                query,
                card.name,
                card.cost,
                card.rarity,
                card.type,
                card.description,
                card.quantity,
                card.price,
            )
        return {"message": f"Carta cadastrada com sucesso!", "value": card}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha no cadastramento das Cartas: {str(e)}"
        )
    finally:
        await conn.close()


# 2. Listar Cartas
@app.get("/api/v1/listCards/", status_code=200)
async def getCards():

    conn = await database()
    try:
        query = "SELECT * FROM cardgames"
        rows = await conn.fetch(query)
        cards = [dict(row) for row in rows]

        if cards:
            return cards
        else:
            return {"message": f"Estoque de Cartas vazio: {cards}"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha na listagem das Cartas: {str(e)}"
        )
    finally:
        await conn.close()


# 3. Buscar Cartas pelo ID
@app.get("/api/v1/searchCard/{id}", status_code=302)
async def checkCards(id: int):

    conn = await database()
    try:
        query = "SELECT * FROM cardgames WHERE id = $1"
        card = await conn.fetchrow(query, id)
        if card is None:
            return {"message": f"Carta com ID {id} não encontrada!"}
        return dict(card)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha na busca das Cartas: {str(e)}"
        )
    finally:
        await conn.close()


# 4. Atualizar uma carta
@app.patch("/api/v1/updateCard/{id}", status_code=200)
async def updateCard(id: int, card_update: UpdatedCard):
    conn = await database()
    try:
        query = "SELECT * FROM cardgames WHERE id = $1"
        card = await conn.fetchrow(query, id)
        if not card:
            raise HTTPException(
                status_code=404, detail=f"Carta com ID {id} não encontrada!"
            )

        update_query = """
            UPDATE cardgames
            SET rarity = COALESCE($1, rarity),
                quantity = COALESCE($2, quantity),
                price = COALESCE($3, price)
            WHERE id = $4
        """
        await conn.execute(
            update_query,
            card_update.rarity,
            card_update.quantity,
            card_update.price,
            id,
        )
        return {"message": f"Carta atualizada com sucesso!", "value": card_update}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha ao atualizar a carta: {str(e)}"
        )
    finally:
        await conn.close()


# 5. Vender uma carta e reduzir a quantidade no estoque
@app.put("/api/v1/sellCard/{id}", status_code=200)
async def sellCard(id: int, sale: SoldCard):
    conn = await database()
    try:
        query = "SELECT * FROM cardgames WHERE id = $1"
        card = await conn.fetchrow(query, id)
        if not card:
            raise HTTPException(
                status_code=404, detail=f"Carta com ID {id} não encontrada!"
            )

        if card["quantity"] < sale.quantity:
            raise HTTPException(
                status_code=400, detail="Quantidade insuficiente no estoque!"
            )

        new_quantity = card["quantity"] - sale.quantity
        update_query = "UPDATE cardgames SET quantity = $1 WHERE id = $2"
        await conn.execute(update_query, new_quantity, id)

        sale_query = """
            INSERT INTO sales (card_id, quantity_sold, sale_value)
            VALUES ($1, $2, $3)
        """
        sale_value = sale.quantity * card["price"]
        await conn.execute(sale_query, id, sale.quantity, sale_value)

        return {
            "message": f"Venda realizada com sucesso!",
            "card": card["name"],
            "quantity_sold": sale.quantity,
            "remaining_stock": new_quantity,
            "sale_value": sale_value,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha ao registrar a venda: {str(e)}"
        )
    finally:
        await conn.close()


# 6 . Listar vendas
@app.get("/api/v1/listSales/", status_code=200)
async def listSales():
    conn = await database()
    try:
        query = """
            SELECT sales.id AS sale_id, cardgames.name AS card_name, 
                   sales.quantity_sold, sales.sale_value, sales.sale_date
            FROM sales
            JOIN cardgames ON sales.card_id = cardgames.id
            ORDER BY sales.sale_date DESC
        """
        rows = await conn.fetch(query)
        sales = [dict(row) for row in rows]

        return sales
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha ao listar as vendas: {str(e)}"
        )
    finally:
        await conn.close()


# 7. Remover Cartas
@app.delete("/api/v1/deleteCard/{id}", status_code=200)
async def deleteCard(id: int):

    conn = await database()

    try:
        query = "SELECT * FROM cardgames WHERE id = $1"
        card = await conn.fetchrow(query, id)

        if card is None:
            return {"message": f"Carta com ID {id} não encontrada!"}

        deleteQuery = "DELETE FROM cardgames WHERE id = $1"
        await conn.execute(deleteQuery, id)

        return {"message": f"Carta removida com sucesso!", "value": card}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha na remoção das Cartas: {str(e)}"
        )
    finally:
        await conn.close()


# 8. Resetar Banco de Dados
@app.delete("/api/v1/resetDatabase/", status_code=200)
async def resetDatabase():
    init_sql = "db/init.sql"
    conn = await database()
    try:
        with open(init_sql, "r") as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "Banco de dados resetado com sucesso!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha ao resetar o banco de dados: {str(e)}"
        )
    finally:
        await conn.close()
