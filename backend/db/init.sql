DROP TABLE IF EXISTS "sales";
DROP TABLE IF EXISTS "cardgames";

CREATE TABLE "cardgames" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "cost" VARCHAR(25) NOT NULL,
    "rarity" VARCHAR(25) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255),
    "quantity" INTEGER NOT NULL,
    "price" FLOAT NOT NULL
);

CREATE TABLE "sales" (
    "id" SERIAL PRIMARY KEY,
    "card_id" INTEGER REFERENCES cardgames(id) ON DELETE CASCADE,
    "quantity_sold" INTEGER NOT NULL,
    "sale_value" FLOAT NOT NULL,
    "sale_date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "cardgames" ("name", "cost", "rarity", "type", "description", "quantity", "price") 
VALUES ('Lightning Bolt', '{R}', 'Incomum', 'Instant', 'Lightning Bolt deals 3 damage to any target.', 45, 13.05);

INSERT INTO "cardgames" ("name", "cost", "rarity", "type", "description", "quantity", "price") 
VALUES ('Giant Growth', '{G}', 'Comum', 'Instant', 'Target creature gets +3/+3 until end of turn.', 128, 0.32);

INSERT INTO "cardgames" ("name", "cost", "rarity", "type", "description", "quantity", "price") 
VALUES ('Ashnod''s Altar', '{3}', 'Incomum', 'Artifact', 'Sacrifice a creature: Add {C}{C}', 10, 43.71);
