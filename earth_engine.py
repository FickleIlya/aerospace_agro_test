import ee
import geojson
import folium


def get_coords(content) -> list:

    coords = content['features'][0]['geometry']['coordinates']

    return coords


def get_geometry(coords: list):
    geometry = ee.Geometry.Polygon(coords)
    return geometry


def getNDVI(image):
    return image.normalizedDifference(['SR_B5', 'SR_B4'])


def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
      tiles=map_id_dict['tile_fetcher'].url_format,
      attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
      name=name,
      overlay=True,
      control=True
  ).add_to(self)


def get_data(content, date_start="2015-01-01", date_end="2022-01-01"):
    ee.Initialize()

    collection = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")

    coords = get_coords(content)
    image = collection.filterBounds(get_geometry(coords)).filterDate(date_start, date_end).first()\
        .clip(get_geometry(coords))
    ndvi = getNDVI(image)

    ndviParams = {'palette': ['blue', 'white', 'green']}

    folium.Map.add_ee_layer = add_ee_layer

    location = sorted(get_coords(content)[0][0], reverse=True)
    my_map = folium.Map(location=location, max_zoom=10)

    my_map.add_ee_layer(ndvi, ndviParams, "NDVI")

    my_map.add_child(folium.LayerControl())

    my_map.save("map.html")