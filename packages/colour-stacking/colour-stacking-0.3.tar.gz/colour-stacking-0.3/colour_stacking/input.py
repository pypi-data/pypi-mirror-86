import json

from .models import GeoJsonInput
from .input_config import InputConfig


def check_colours(polygons_and_colours, ordered_colours):
    polygon_colours = {
        c
        for (p, cs) in polygons_and_colours
        for c in cs
    }

    if not polygon_colours <= set(ordered_colours):
        mismatch = ", ".join(polygon_colours - set(ordered_colours))
        raise Exception(f"Mismatch between polygon colours and ordered "
                        f"colours: {mismatch}")


def read_geojson(path: str):
    return read_input(json.load(open(path)))


def read_input(geojson_dict: dict):
    data = GeoJsonInput(**geojson_dict)
    polygons_and_colours = [
        (x.geometry, x.properties.colours)
        for x in data.features
    ]
    config = InputConfig(data.properties.ordered_colours,
                         data.properties.buffer_size,
                         data.properties.opposite_share_thickness)

    check_colours(polygons_and_colours, config.colour_order)

    return config, polygons_and_colours
