from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from gdsfactory.simulation.gmsh.parse_component import bufferize
from gdsfactory.simulation.gmsh.parse_gds import cleanup_component
from gdsfactory.simulation.gmsh.parse_layerstack import order_layerstack
from gdsfactory.technology import LayerStack
from gdsfactory.typings import ComponentOrReference

from meshwell.prism import Prism
from meshwell.model import Model

from collections import OrderedDict
import gmsh


def define_prisms(layer_polygons_dict, layerstack, model):
    """Define meshwell prism dimtags from gdsfactory information."""
    prisms_dict = OrderedDict()
    buffered_layerstack = bufferize(layerstack)
    ordered_layerstack = order_layerstack(layerstack)

    for layername in ordered_layerstack:
        coords = np.array(buffered_layerstack.layers[layername].z_to_bias[0])
        zs = (
            coords * buffered_layerstack.layers[layername].thickness
            + buffered_layerstack.layers[layername].zmin
        )
        buffers = buffered_layerstack.layers[layername].z_to_bias[1]

        buffer_dict = dict(zip(zs, buffers))

        prisms_dict[layername] = Prism(
            polygons=layer_polygons_dict[layername],
            buffers=buffer_dict,
            model=model,
        )

    return prisms_dict


def xyz_mesh(
    component: ComponentOrReference,
    layerstack: LayerStack,
    resolutions: Optional[Dict] = None,
    default_characteristic_length: float = 0.5,
    filename: Optional[str] = None,
    verbosity: Optional[int] = 0,
    round_tol: int = 3,
    simplify_tol: float = 1e-3,
) -> bool:
    """Full 3D mesh of component.

    Args:
        component (Component): gdsfactory component to mesh
        layerstack (LayerStack): gdsfactory LayerStack to parse
        resolutions (Dict): Pairs {"layername": {"resolution": float, "distance": "float}} to roughly control mesh refinement
        default_resolution_min (float): gmsh minimal edge length
        default_resolution_max (float): gmsh maximal edge length
        filename (str, path): where to save the .msh file
        round_tol: during gds --> mesh conversion cleanup, number of decimal points at which to round the gdsfactory/shapely points before introducing to gmsh
        simplify_tol: during gds --> mesh conversion cleanup, shapely "simplify" tolerance (make it so all points are at least separated by this amount)

    """
    # Fuse and cleanup polygons of same layer in case user overlapped them
    layer_polygons_dict = cleanup_component(
        component, layerstack, round_tol, simplify_tol
    )

    # Meshwell Prisms from gdsfactory polygons and layerstack
    model = Model()
    prisms_dict = define_prisms(layer_polygons_dict, layerstack, model)

    gmsh.option.setNumber("Mesh.ScalingFactor", 1e-6)

    # Mesh
    mesh_out = model.mesh(
        entities_dict=prisms_dict,
        resolutions=resolutions,
        default_characteristic_length=0.5,
        filename=filename,
        verbosity=verbosity,
    )

    return mesh_out


if __name__ == "__main__":
    import gdsfactory as gf

    from gdsfactory.pdk import get_layer_stack
    from gdsfactory.generic_tech import LAYER

    c = gf.Component()

    # waveguide = c << gf.get_component(gf.components.straight_pin(length=5, taper=None))
    waveguide = c << gf.get_component(gf.components.straight_heater_metal(length=50))
    # waveguide = c << gf.get_component(gf.components.ring_single_heater())
    wafer = c << gf.components.bbox(bbox=waveguide.bbox, layer=LAYER.WAFER)

    filtered_layerstack = LayerStack(
        layers={
            k: get_layer_stack().layers[k]
            for k in (
                "core",
                "box",
                "clad",
                "heater",
                # "metal2",
                # "metal3",
                # "via1",
                "via2",
            )
        }
    )

    filtered_layerstack.layers["core"].info["mesh_order"] = 1
    filtered_layerstack.layers["box"].info["mesh_order"] = 4
    filtered_layerstack.layers["clad"].info["mesh_order"] = 5
    filtered_layerstack.layers["heater"].info["mesh_order"] = 2
    filtered_layerstack.layers["via2"].info["mesh_order"] = 1
    filtered_layerstack.layers["via2"].zmin = (
        filtered_layerstack.layers["heater"].zmin
        + filtered_layerstack.layers["heater"].thickness
    )

    resolutions = {
        "core": {"resolution": 0.2},
        "slab90": {"resolution": 0.8},
        "via_contact": {"resolution": 1},
    }
    geometry = xyz_mesh(
        component=c,
        layerstack=filtered_layerstack,
        resolutions=resolutions,
        filename="mesh.msh",
        default_characteristic_length=2,
        verbosity=5,
    )
