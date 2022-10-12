import csv
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DATA_SRC="app/data/Miesieczne_wskazniki_cen_towarow_i_uslug_konsumpcyjnych_od_1982_roku.csv"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/items")
async def root():
    keys_ = ['rok', 'miesiac', 'wartosc']
    data = []
    with open(DATA_SRC) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data =  [
            {key_: row.get(key_) for key_ in keys_} for row in csv_reader
            ]
    return data