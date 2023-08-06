from segmentation_dxf.PNGtoDXF import square_coordinates

def test_square_coordinates_example():
    coordinates = square_coordinates(0, 0, 1)

    assert coordinates == [(0, 0), (1, 0), (1, -1), (0, -1), (0, 0)]