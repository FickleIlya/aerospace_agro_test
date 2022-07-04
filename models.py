from pydantic import BaseModel


class GeoJSON(BaseModel):
    name: str
    data: str
