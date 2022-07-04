import os

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, Text)

from databases import Database
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


DATABASE_URL = f'postgresql://{os.environ["NAME"]}:{os.environ["PASSWORD"]}@localhost/{os.environ["DATABASE_NAME"]}'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

geojsons = Table(
    'geojsons',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('data', Text),
)

database = Database(DATABASE_URL)
