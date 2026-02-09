from __future__ import annotations

import gdsfactory as gf

import numpy as np

import gfelib as gl


@gl.utils.default_cell
def comb_angular(
    radius_inner: float,
    radius_outer: float,
    angles: tuple[float, float],
    overlap: float,
    gap: float,
    count: int,
    geometry_layer: gf.typings.LayerSpec,
    angle_resolution: float,
    release_spec_a: gl.datatypes.ReleaseSpec | None,
    release_spec_b: gl.datatypes.ReleaseSpec | None,
) -> gf.Component:
    """Returns an angular comb

    Args:
        radius_inner: comb inner radius
        radius_outer: comb outer radius
        angles: comb start and end angles
        overlap: comb finger overlap (unit: degrees)
        gap: comb finger gap
        count: comb count, finger count is `count + 1`
        geometry_layer: comb polygon layer
        angle_resolution: degrees per point for circular geometries
        release_spec_a: release specifications for lower angle combs, `None` for no release
        release_spec_b: release specifications for higher angle combs, `None` for no release
    """
    c = gf.Component()

    angles = sorted(angles)

    finger_span = 0.5 * (angles[1] - angles[0] + overlap)
    finger_width = (radius_outer - radius_inner - gap * count) / (count + 1)

    for i in range(count + 1):
        r = radius_inner + i * (finger_width + gap)
        ring = gl.basic.ring(
            radius_inner=r,
            radius_outer=r + finger_width,
            angles=(
                angles[0] if (i % 2 == 0) else angles[1] - finger_span,
                angles[0] + finger_span if (i % 2 == 0) else angles[1],
            ),
            geometry_layer=geometry_layer,
            angle_resolution=angle_resolution,
            release_spec=release_spec_a if (i % 2 == 0) else release_spec_b,
        )
        _ = c << ring

    return c
