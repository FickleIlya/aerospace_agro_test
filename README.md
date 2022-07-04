# aerospace_agro_test

In db.py creating table named geojsons which contains field name and geojson string content as data.
db_manager.py is database manager with methods: add field, delete field, get field

earth_engine.py is business logic. get coords from content -> transformation to ee.Geometry -> get NDVI field -> save map with ndvi field as html file
