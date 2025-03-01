from fastapi import FastAPI
from pydantic import BaseModel
import os
import pandas as pd

app = FastAPI()

class UserCreate(BaseModel):
    user_id: int
    username: str

user_data_list = []

# CSV file path
csv_file = "user_data.csv"

# Function to export data to CSV using pandas
def export_to_csv(data_list):
    # Convert list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data_list)

    # Export to CSV (if file exists, it will append, otherwise it will create a new file)
    df.to_csv(csv_file, index=False, mode='w', header=not os.path.isfile(csv_file))

# Function to read CSV and convert to list of dictionaries
def read_csv_to_dict():
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file)
        return df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
    else:
        return []  # Return an empty list if the file doesn't exist

@app.post("/create_user/")
async def create_user(user_data: UserCreate):
    # Add the received user data to the list
    user_dict = {"user_id": user_data.user_id, "username": user_data.username}
    user_data_list.append(user_dict)

    # Export the updated list to the CSV file
    export_to_csv(user_data_list)

    return {
        "msg": "SYBAU!",
        "user_id": user_data.user_id,
        "username": user_data.username,
    }

@app.get("/users/")
async def get_users():
    # Read the CSV content and return it as a list of dictionaries
    users = read_csv_to_dict()
    return {"users": users}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# practice again