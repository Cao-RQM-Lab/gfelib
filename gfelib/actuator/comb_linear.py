from __future__ import annotations

import gdsfactory as gf

import numpy as np

import gfelib as gl


@gl.utils.default_cell
def comb_linear(
    height: float,
    width: float,
    overlap: float,
    gap: float,
    count: int,
    geometry_layer: gf.typings.LayerSpec,
    release_spec_a: gl.datatypes.ReleaseSpec | None,
    release_spec_b: gl.datatypes.ReleaseSpec | None,
) -> gf.Component:
    """Returns a linear rectangular comb, south-west is (0, 0)

    Args:
        height: comb total height (y), height of each finger is `0.5 * (height + overlap)`
        width: comb total width (x), width of each finger is `(width - gap * count) / (count + 1)`
        overlap: comb finger overlap (y)
        gap: comb finger gap (x)
        count: comb count, finger count is `count + 1`
        geometry_layer: comb polygon layer
        release_spec_a: release specifications for bottom combs, `None` for no release
        release_spec_b: release specifications for top combs, `None` for no release
    """
    c = gf.Component()

    finger_length = 0.5 * (height + overlap)
    finger_width = (width - gap * count) / (count + 1)
    offset = height - finger_length

    for i in range(count + 1):
        finger = gl.basic.rectangle(
            size=(finger_width, finger_length),
            geometry_layer=geometry_layer,
            centered=False,
            release_spec=release_spec_a if (i % 2 == 0) else release_spec_b,
        )
        ref = c << finger
        ref.move(
            (
                i * (finger_width + gap),
                0 if (i % 2 == 0) else offset,
            )
        )

    return c
