# Colour Stacking

We have a set of polygons to represent.

The boundary of these polygons has to be coloured
with given colours.  Some polygon boundaries have
the same colours, other do not.  Some polygons have
a single colour, other have multiple.

![Polygons](tests/data/polygon.png)

We would like to ensure that all colours are
visible by adjusting the thickness of the
coloured line.  If more than one polygon has the
same colour, the thickness for that colour
should be the same if the polygons overlap.  

The thickness associated with each colour is
ordered: e.g. blue cannot be thicker than orange.

In the example above:
- the boundary of A must be coloured red and blue;
- the boundary of B mus be coloured blue;
- the boundary of C must be coloured orange;
- the red must have the highest thickness, followed
  by blue and orange.
  
# Usage

This tool takes GeoJSON files as input (see 
[tests/data/example.geojson](tests/data/example.geojson) for an idea of the format used)

Run the tool as follows
```
python -m colour_stacking tests/data/example.geojson
```

The output should be along the lines of 
```json
[
    { "polygon_index": 0, "colour": "blue",   "thickness": 2 },
    { "polygon_index": 0, "colour": "red",    "thickness": 3 },
    { "polygon_index": 1, "colour": "blue",   "thickness": 2 },
    { "polygon_index": 2, "colour": "orange", "thickness": 1 }
]
```

# More information

This tool is centered around the use of
[Microsoft's Z3 theorem prover](https://github.com/Z3Prover/z3).