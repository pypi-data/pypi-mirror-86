import sys
from copy import deepcopy

import helpers
import numpy
import pytest

import toughio


@pytest.mark.skipif(sys.version_info < (3,), reason="Order of keys in dictionary")
def test_time_series():
    # Import hybrid mesh
    mesh_ref = deepcopy(helpers.hybrid_mesh)

    # Create random time series
    num_steps = 5
    point_data_ref = [
        {"points": numpy.random.rand(mesh_ref.n_points)} for _ in range(num_steps)
    ]
    cell_data_ref = [
        {"cells": numpy.random.rand(mesh_ref.n_cells)} for i in range(num_steps)
    ]
    time_steps_ref = numpy.sort(numpy.random.rand(num_steps))

    # Write and read back XDMF
    filepath = helpers.tempdir("test.xdmf")
    toughio.write_time_series(
        filepath,
        mesh_ref.points,
        mesh_ref.cells,
        point_data_ref,
        cell_data_ref,
        time_steps_ref,
    )
    mesh = toughio.read_time_series(filepath)
    points, cells, point_data, cell_data, time_steps = mesh

    # Compare with reference data
    assert numpy.allclose(points, mesh_ref.points)

    for cell_ref, cell in zip(mesh_ref.cells, cells):
        assert cell_ref.type == cell.type
        assert numpy.allclose(cell_ref.data, cell.data)

    for t, pdata in enumerate(point_data):
        for k, v in pdata.items():
            assert numpy.allclose(v, point_data_ref[t][k])

    for t, cdata in enumerate(cell_data):
        for k, v in cdata.items():
            assert numpy.allclose(v, cell_data_ref[t][k])

    assert numpy.allclose(time_steps, time_steps_ref)
