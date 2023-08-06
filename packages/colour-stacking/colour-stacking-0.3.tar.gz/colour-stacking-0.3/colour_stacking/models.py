from typing import List

import pydantic
import shapely.geometry as geo


class FeatureProperties(pydantic.BaseModel):
    colours: List[str]


class MyPolygon(geo.Polygon):

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            poly = geo.shape(v)
        except Exception as e:
            raise pydantic.ValidationError(f"bad geometry: {e}") from e
        if poly.geom_type != 'Polygon':
            raise pydantic.ValidationError(f"Expected a polygon, got {poly.geom_type}")
        return poly


class Feature(pydantic.BaseModel):
    geometry: MyPolygon
    properties: FeatureProperties


class GeoJsonInputProperties(pydantic.BaseModel):
    ordered_colours: List[str]
    buffer_size: float = 0.1
    opposite_share_thickness: bool = False


class GeoJsonInput(pydantic.BaseModel):
    properties: GeoJsonInputProperties
    features: List[Feature]
