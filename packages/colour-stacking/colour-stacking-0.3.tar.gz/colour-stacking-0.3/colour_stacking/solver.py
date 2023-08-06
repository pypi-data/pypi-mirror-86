from collections import defaultdict
from enum import Enum
import shapely.geometry as geo
from shapely.strtree import STRtree
from typing import List, Tuple, Dict
import z3

from .input_config import InputConfig


class IntersectionType(Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"
    NONE = "none"


def intersection_type(
        p1: geo.Polygon,
        p2: geo.Polygon,
        input_config: InputConfig) -> IntersectionType:

    if p1 == p2:
        return IntersectionType.INSIDE

    p1_buffered = p1.boundary.buffer(input_config.buffer_size)
    if not p1_buffered.intersects(p2.boundary):
        return IntersectionType.NONE
    elif p1.difference(p1_buffered).intersects(p2):
        return IntersectionType.INSIDE
    else:
        return IntersectionType.OUTSIDE


def share_all_colours(solver,
                      polygon_index_1,
                      polygon_index_2,
                      variables,
                      colour_order):

    for p1, c1 in variables.keys():
        for p2, c2 in variables.keys():
            if p1 == polygon_index_1 and p2 == polygon_index_2:
                v1 = variables[(p1, c1)]
                v2 = variables[(p2, c2)]
                if c1 == c2:
                    solver.add(v1 == v2)
                elif colour_order[c1] < colour_order[c2]:
                    solver.add(v1 < v2)
                else:
                    solver.add(v1 > v2)


def share_colours_outside(
        solver,
        polygon_index_1,
        polygon_index_2,
        variables):

    for p1, c1 in variables.keys():
        for p2, c2 in variables.keys():
            if p1 == polygon_index_1 and p2 == polygon_index_2:
                v1 = variables[(p1, c1)]
                v2 = variables[(p2, c2)]
                if c1 == c2:
                    solver.add(v1 == v2)


def ensure_colour_ordering(solver, variables, colour_order):
    for c in variables.keys():
        solver.add(variables[c] > 0)

    vars_per_polygon = defaultdict(list)

    for (pi, colour), var in variables.items():
        vars_per_polygon[pi].append((colour, var))

    for pi, var_list in vars_per_polygon.items():
        for i1, (c1, v1) in enumerate(var_list):
            for (c2, v2) in var_list[i1 + 1:]:
                if c1 == c2:
                    solver.add(v1 == v2)
                elif colour_order[c1] < colour_order[c2]:
                    solver.add(v1 < v2)
                else:
                    solver.add(v1 > v2)


def buffered_query(tree: STRtree,
                   polygon: geo.Polygon,
                   buffer_size: float) -> List[geo.Polygon]:
    bbox = polygon.bounds
    extended = geo.box(
        bbox[0] - buffer_size,
        bbox[1] - buffer_size,
        bbox[2] + buffer_size,
        bbox[3] + buffer_size)

    return tree.query(extended)


def collect(
        solver: z3.Solver,
        polygons_and_colours: List[Tuple[geo.Polygon, str]],
        input_config: InputConfig) -> Dict[Tuple[int, str], z3.Int]:

    colour_order = {
        colour: index
        for index, colour in enumerate(input_config.colour_order)
    }

    variables = {
        (polygon_index, c): z3.Int(f"p{polygon_index}:{c}")
        for polygon_index, (p, cs) in enumerate(polygons_and_colours)
        for c in cs
    }

    ensure_colour_ordering(solver, variables, colour_order)

    for index, (p, c) in enumerate(polygons_and_colours):
        p.polygon_index = index

    tree = STRtree([p for (p, c) in polygons_and_colours])

    for i1, (p1, c1) in enumerate(polygons_and_colours):

        matches = [
            p2 for p2 in buffered_query(tree, p1, input_config.buffer_size)
            if p2.polygon_index > p1.polygon_index
        ]

        for p2 in matches:
            t = intersection_type(p1, p2, input_config)
            if t == IntersectionType.INSIDE:
                share_all_colours(solver, i1, p2.polygon_index,
                                  variables, colour_order)
            elif t == IntersectionType.OUTSIDE:
                if input_config.opposite_share_thickness:
                    share_colours_outside(solver, i1,
                                          p2.polygon_index, variables)

    return variables


def solve(
        polygons_and_colours: List[Tuple[geo.Polygon, str]],
        input_config: InputConfig) -> Dict[Tuple[int, str], z3.Int]:

    solver = z3.Solver()

    variables = collect(solver, polygons_and_colours, input_config)

    if solver.check() != z3.sat:
        raise Exception("Not satisfied")

    sol = solver.model()

    result = [
        dict(polygon_index=index,
             colour=colour,
             thickness=sol[v].as_long())
        for (index, colour), v in variables.items()
    ]

    return result
