from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
import random

app = FastAPI()

CSV_FILE = "characters.csv"

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["id", "name", "role", "netWorth"])
    df.to_csv(CSV_FILE, index=False)


class Character(BaseModel):
    name: str
    role: str
    netWorth: str  # Include netWorth in the model


# GET characters from CSV
@app.get("/characters")
async def get_characters():
    df = pd.read_csv(CSV_FILE)
    characters = df.to_dict(orient="records")
    return {"characters": characters}

# GET specific character
@app.get("/characters/{id}")
async def get_character(id: int):
    df = pd.read_csv(CSV_FILE)

    # Ensure 'id' column is treated as numeric
    df["id"] = pd.to_numeric(df["id"], errors="coerce")

    char = df[df["id"] == id]

    if char.empty:
        return {"error": "Character not found"}

    return {"character": char.to_dict(orient="records")[0]}

# Add new character
@app.post("/characters")
async def add_character(character: Character):
    df = pd.read_csv(CSV_FILE)
    if not df.empty:
        df["id"] = pd.to_numeric(df["id"], errors="coerce")
        new_id = int(df["id"].max() + 1)
    else:
        new_id = 1

    # Fix: Add correct field names (name, role, netWorth)
    new_character = pd.DataFrame([[new_id, character.name, character.role, character.netWorth]],
                                 columns=["id", "name", "role", "netWorth"])

    df = pd.concat([df, new_character], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    return {"message": "Character added", "character": {"id": new_id, "name": character.name, "role": character.role, "netWorth": character.netWorth}}

# GET random quote
@app.get("/quote")
async def get_quote():
    try:
        if not os.path.exists("quote.csv"):
            return {"error": "Quotes file not found"}
        
        df = pd.read_csv("quote.csv")
        
        if df.empty:
            return {"error": "No quotes found"}
        
        random_quote = df.sample(1).to_dict(orient="records")[0]
        return {"quote": random_quote["quote"]}
    
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
