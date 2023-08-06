from segmentation_dxf.PNGtoDXF import common_member


def test_common_member():
    a = [1, 2, 3, 4]
    b = [2, 3, 4, 5]

    assert common_member(a, b)
