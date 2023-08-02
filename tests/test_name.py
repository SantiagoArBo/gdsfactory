from __future__ import annotations

from functools import partial

import gdsfactory as gf


@gf.cell
def rectangles(widths: gf.typings.Floats) -> gf.Component:
    c = gf.Component()
    for width in widths:
        c << gf.components.rectangle(size=(width, width))

    c.distribute()
    return c


def test_name_partial_functions() -> None:
    s1 = partial(gf.components.straight)
    s2 = partial(gf.components.straight, length=5)
    s3 = partial(gf.components.straight, 5)

    m1 = partial(gf.components.mzi, straight=s1)()
    m2 = partial(gf.components.mzi, straight=s2)()
    m3 = partial(gf.components.mzi, straight=s3)()

    assert (
        m2.name == m3.name
    ), f"{m2.name} different from {m2.name} while they are the same function"
    assert (
        m1.name != m2.name
    ), f"{m1.name} is the same {m2.name} while they are different functions"
    assert (
        m1.name != m3.name
    ), f"{m1.name} is the same {m3.name} while they are different functions"


def test_name_iterators() -> None:
    c1 = rectangles(list(range(5)))
    c2 = rectangles(list(range(6)))
    assert c1.name != c2.name


def test_float_point_errors() -> None:
    c1 = gf.components.straight(length=5.0 + 1e-20)  # any unit below pm disappears
    c2 = gf.components.straight(length=5.0)
    assert c1.name == c2.name, f"{c1.name} does not match {c2.name}"


# def test_name_different_signatures():

#     @gf.cell
#     def compass(layer=(2, 0)):


if __name__ == "__main__":
    test_name_iterators()

    # @gf.cell
    # def compass(layer=(2, 0)):
