from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["Warrior"]
warrior_data = db["Warrior_coll"]

app = FastAPI()

class warriordata(BaseModel):
    name: str
    phone: int
    city: str
    course: str

@app.post("/warrior/insert")
async def warrior_data_insert_helper(data:warriordata):
    result = await warrior_data.insert_one(data.dict())
    return str(result.inserted_id)

def warrior_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/warrior/getdata")
async def get_warrior_data():
    items = []
    cursor = warrior_data.find({})
    async for document in cursor:
        items.append(warrior_helper(document))
    return items



          