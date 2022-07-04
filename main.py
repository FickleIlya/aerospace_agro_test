import geojson
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response

import db_manager
from db import metadata, database, engine
from earth_engine import get_data
from models import GeoJSON

metadata.create_all(engine)

app = FastAPI()


@app.post("/load_data", status_code=201)
async def load_data(field_name: str, file: UploadFile = File(...)):

    data = geojson.load(file.file)
    string_data = geojson.dumps(data)

    await database.connect()

    field = GeoJSON(name=field_name, data=string_data)

    field_id = await db_manager.add_field(field)

    await database.disconnect()

    response = {
        "id": field_id,
        "field": field.data
    }

    return response


@app.get('/{field_name}')
async def get_field_map(field_name: str, date_start: str = None, date_end: str = None):
    await database.connect()
    field = await db_manager.get_field(field_name)
    await database.disconnect()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    field_in_db = GeoJSON(**field)

    content = geojson.loads(field_in_db.data)
    if date_start and date_end:
        get_data(content, date_start, date_end)
    else:
        get_data(content)

    with open("map.html", "r") as f:
        page = f.read()

    return Response(page, media_type="text/html")


@app.delete('/{field_name}')
async def delete_field(field_name: str):
    await database.connect()
    field = await db_manager.get_field(field_name)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    await db_manager.delete_field(field_name)
    await database.disconnect()
    return {"data": "field deleted"}
