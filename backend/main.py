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


app = FastAPI()


class Card(BaseModel):
    name: str
    cost: str
    rarity: str
    type: str
    description: str
    quantity: int
    price: float


class SoldCard(BaseModel):
    name: str
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

@app.patch("/api/v1/updateCard/{id}", status_code=200)
async def updateCard(id: int, card_update: UpdatedCard):
    conn = await database()
    try:
        # Verificar se a carta existe
        query = "SELECT * FROM cardgames WHERE id = $1"
        card = await conn.fetchrow(query, id)
        if not card:
            raise HTTPException(status_code=404, detail=f"Carta com ID {id} não encontrada!")

        # Atualizar os campos fornecidos
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
            id
        )
        return {"message": f"Carta com ID {id} atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha ao atualizar a carta: {str(e)}"
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

