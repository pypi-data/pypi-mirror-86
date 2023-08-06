import ezdxf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import more_itertools as mit
import cv2 as cv


def white_pixels(img):
    """Given a binary image, it returns the coordinates of the white pixels."""
    white_pixels_x = []
    white_pixels_y = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            cordinate = i, j
            if (img.getpixel(cordinate) == 255):
                white_pixels_x = np.append(white_pixels_x, i) # numpy.ndarray
                white_pixels_y = np.append(white_pixels_y, j) # numpy.ndarray
    return(white_pixels_x, white_pixels_y)

def common_member(a, b):
    """Given two lists of concecutive numbers, it tells if they have any member in common."""
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return(True)
    return(False)

def square_coordinates(i, j, delta):
    """Given the coordinates of the top left corner and the length of the sides,
    it returns the list of coordinates of all points in a square moving clockwise."""
    coordinates = [(i, j), (i + delta, j), (i + delta, j - delta), (i, j - delta), (i, j)]
    return coordinates

def test_square_coordinates_example():
    coordinates = square_coordinates(0, 0, 1)

    assert coordinates == [(1, 0), (1, 0), (1, -1), (0, -1), (0, 0)]


def main():

    ## Load image
    origin_path = '/Users/elisakhourichalouhi/Desktop/Hackathon/toronto/annotations/roads'
    png_filename = '15778900_15'
    filename = origin_path + '/' + png_filename + '.png'
    saving_path = '/Users/elisakhourichalouhi/Desktop/Hackathon/Generated_dxf_files'

    im = Image.open(filename)
    im.show()

    ## Find white pixels
    white_pixels_x, white_pixels_y = white_pixels(im)

    '''
    ## Identify roads
    # Start at the lowest value of x and identify the first roads
    x_road_min = int(np.min(white_pixels_x))
    x_road_max = int(np.max(white_pixels_x))
    pixels_y = white_pixels_y[np.where(white_pixels_x==x_road_min)]
    subgroups_y = [list(group) for group in mit.consecutive_groups(pixels_y)]
    streets_y_1 = []
    streets_x_1 = []
    streets_y_2 = []
    streets_x_2 = []
    for j in range(len(subgroups_y)): # Go through all pixel groups belonging to roads at x = x_value
        a = subgroups_y[j]
        if len(a) == 1:
            streets_y_1.append([a[0]])
            streets_y_2.append([a[0]])
            streets_x_1.append([x_road_min])
            streets_x_2.append([x_road_min])
        else:
            streets_y_1.append([a[0]])
            streets_y_2.append([a[-1]])
            streets_x_1.append([x_road_min])
            streets_x_2.append([x_road_min])
    # Go through all x values > x_road_min and identify to which roads they belong
    previous_subgroups_y = subgroups_y
    previous_subgroups_road_indices = list(range(len(previous_subgroups_y)))
    for x_value in range(x_road_min+1,x_road_max): 
        pixels_y = white_pixels_y[np.where(white_pixels_x==x_value)]
        subgroups_y = [list(group) for group in mit.consecutive_groups(pixels_y)]
        road_indices = []
        road_n = None
        for j in range(len(subgroups_y)): # Go through all pixel groups at x = x_value
            found_road = 0
            a = subgroups_y[j]
            for k in range(len(previous_subgroups_y)): # Go through all pixel groups at x = x_value-1
                b = previous_subgroups_y[k]
                isSameRoad = common_member(a, b)
                if isSameRoad == True: # It is the continuation of the road which previous_subgroups_y[k] belongs to
                    found_road = 1
                    road_n = previous_subgroups_road_indices[k]
                    road_indices.append(road_n)
                    if len(a) == 1:
                        streets_y_1[road_n].extend([a[0]])
                        streets_x_1[road_n].extend([x_value])
                        streets_y_2[road_n].extend([a[0]])
                        streets_x_2[road_n].extend([x_value])
                    else:
                        streets_y_1[road_n].extend([a[0]])
                        streets_x_1[road_n].extend([x_value])
                        streets_y_2[road_n].extend([a[-1]])
                        streets_x_2[road_n].extend([x_value])
                    del previous_subgroups_y[k] # Avoid befurcations
                    del previous_subgroups_road_indices[k] # Avoid befurcations
                    break
            if found_road == 0: # It is a new road
                road_n = int(len(streets_y_1))
                road_indices.append(road_n)
                if len(a) == 1:
                    streets_y_1.append([a[0]])
                    streets_x_1.append([x_value])
                    streets_y_2.append([a[0]])
                    streets_x_2.append([x_value])
                else:
                    streets_y_1.append([a[0]])
                    streets_x_1.append([x_value])
                    streets_y_2.append([a[-1]])
                    streets_x_2.append([x_value])
        previous_subgroups_road_indices = road_indices
        previous_subgroups_y = subgroups_y
        '''

    ## Creat new dxf file 
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    doc.layers.new(name='RoadContours', dxfattribs={'linetype': 'CONTINUOUS', 'color': 7})
    doc.layers.new(name='ImageEdges', dxfattribs={'linetype': 'CONTINUOUS', 'color': 13})
    doc.layers.new(name='RoadContours_cv2', dxfattribs={'linetype': 'CONTINUOUS', 'color': 13})

    # Draw image edges
    msp.add_lwpolyline([(0,0), (im.size[0],0), (im.size[0],-im.size[1]), (0,-im.size[1]), (0,0)], dxfattribs={'layer': 'ImageEdges'})
    '''
    # Draw roads Elisa
    for i in range(len(streets_x_1)):
        street_y_1_dxf = [ -y for y in streets_y_1[i]] 
        street_y_2_dxf = [ -y for y in streets_y_2[i]]
        points_1 = list(zip(streets_x_1[i], street_y_1_dxf))
        points_2 = list(zip(streets_x_2[i], street_y_2_dxf))
        msp.add_lwpolyline(points_1, dxfattribs={'layer': 'RoadContours'})
        msp.add_lwpolyline(points_2, dxfattribs={'layer': 'RoadContours'})
        '''
    # Draw roads cv contours
    im = cv.imread(filename)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        points_x = []
        points_y = []
        for j in range(len(contours[i])):
            x = contours[i][j][0][0]
            y = -contours[i][j][0][1]
            points_x.append(x)
            points_y.append(y)
        points_x.append(contours[i][0][0][0]) # Close contours
        points_y.append(-contours[i][0][0][1])
        points = list(zip(points_x, points_y))
        msp.add_lwpolyline(points, dxfattribs={'layer': 'RoadContours_cv2'})
    '''
    # Draw pixels
    pixel_dimention = 0.5 # In m.
    white_pixels_x = white_pixels_x*pixel_dimention
    white_pixels_y = white_pixels_y*pixel_dimention
    for i in range(len(white_pixels_x)):
        points = square_coordinates(white_pixels_x[i],-white_pixels_y[i],pixel_dimention)
        msp.add_lwpolyline(points, dxfattribs={'layer': 'RoadArea'})
    '''
    '''
    ## Insert image
    my_image_def = doc.add_image_def(filename=filename, size_in_pixel=(im.size[0], im.size[1]))
    msp.add_image(insert=(2, 1), size_in_units=(im.size[0], im.size[1]), image_def=my_image_def, rotation=0)
    image_defs = doc.objects.query('IMAGEDEF')  # get all image defs in drawing
    '''

    raw_filename = png_filename
    dxf_filename = saving_path + '/' + raw_filename + '_cv2.dxf'
    doc.saveas(dxf_filename)


if __name__ == '__main__':
    main()
