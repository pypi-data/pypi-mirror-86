import ezdxf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import more_itertools as mit
import cv2 as cv
from pathlib import Path


def common_member(a, b):
    """Given two lists of concecutive numbers, it tells if they have any member in common."""
    return len(set(a) & set(b)) > 0

def segmentation2dxf(png):
    png = Path(png)
    png_directory = png.parent
    png_stem = png.stem
    export_directory = png_directory / 'exported'
    export_directory.mkdir(exist_ok=True)
    dxf = str(export_directory / png_stem) + '.dxf'

    white = 7
    red = 13

    road_contours_color = white
    image_edges_color = red

    ## Creat new dxf file 
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    doc.layers.new(name='RoadContours', dxfattribs={'linetype': 'CONTINUOUS', 'color': road_contours_color})
    doc.layers.new(name='ImageEdges', dxfattribs={'linetype': 'CONTINUOUS', 'color': image_edges_color})

    # 
    # im = cv.frombuffer(...)
    #

    im = cv.imread(str(png))
    height, width, _ = im.shape
    # Draw image edges
    msp.add_lwpolyline([(0, 0), (height, 0), (height, -width), (0, -width), (0, 0)], dxfattribs={'layer': 'ImageEdges'})
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    _, threshold = cv.threshold(imgray, 127, 255, 0)
    contours, _ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for (i, contour) in enumerate(contours):
        points_x = []
        points_y = []
        for (j, point) in enumerate(contour):
            x = point[0][0]
            y = -point[0][1]
            points_x.append(x)
            points_y.append(y)

        # Close the contour
        points_x.append(contour[0][0][0])
        points_y.append(-contour[0][0][1])
        points = list(zip(points_x, points_y))

        # Draw road contour
        msp.add_lwpolyline(points, dxfattribs={'layer': 'RoadContours'})
    
    doc.saveas(dxf)

    # output_stream = io.TextIO()
    # doc.write(output_stream)
    # return output_stream

    return dxf

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Convert segmentation to DXF')
    
    parser.add_argument('filename', help='Filename of the segmentation')

    args = parser.parse_args()
    
    dxf = segmentation2dxf(args.filename)

    print(dxf)