from models import GeoJSON
from db import geojsons, database


async def add_field(payload: GeoJSON):
    query = geojsons.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_field(field_name: str):
    query = geojsons.select(geojsons.c.name == field_name)
    return await database.fetch_one(query=query)


async def delete_field(field_name: str):
    query = geojsons.delete().where(geojsons.c.name == field_name)
    return await database.execute(query=query)
