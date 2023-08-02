from __future__ import annotations

import jsondiff

import gdsfactory as gf


def test_read_gds_hash() -> None:
    gdspath = gf.PATH.gdsdir / "straight.gds"
    c = gf.import_gds(gdspath)
    h = "c956390621a5322a185cd20b0072a778fc613195"
    assert c.hash_geometry() == h, f"h = {c.hash_geometry()!r}"


# def test_read_gds_with_settings(data_regression: DataRegressionFixture) -> None:


def test_read_gds_equivalent() -> None:
    """Ensures Component from GDS + YAML loads same component settings."""
    c1 = gf.components.straight(length=1.234)
    gdspath = gf.PATH.gdsdir / "straight.gds"

    c2 = gf.import_gds(gdspath, read_metadata=True)
    d1 = c1.to_dict()
    d2 = c2.to_dict()
    d = jsondiff.diff(d1, d2)

    assert len(d) == 0, d


def test_mix_cells_from_gds_and_from_function() -> None:
    """Ensures not duplicated cell names.

    when cells loaded from GDS and have the same name as a function with
    @cell decorator
    """
    gdspath = gf.PATH.gdsdir / "straight.gds"
    c = gf.Component("test_mix_cells_from_gds_and_from_function")
    c << gf.components.straight(length=1.234)
    c << gf.import_gds(gdspath)
    c.write_gds()


def _write() -> None:
    c1 = gf.components.straight(length=1.234)
    gdspath = gf.PATH.gdsdir / "straight.gds"
    c1.write_gds(gdspath=gdspath, with_metadata=True)
    c1.show()
    c1.pprint()


if __name__ == "__main__":
    _write()  # run this in case you want to regenerate the tests

    test_read_gds_equivalent()
