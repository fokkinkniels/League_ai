import cv2 as cv
import numpy as np

class Vision:

    


    def get_click_points(rectangles):
        points = []

        for (x, y, _x, _y) in rectangles:
            center_x = x + (_x-x)/2
            center_y = y + (_y-y)/2
            points.append((int(center_x), int(center_y)))

        return points


    def draw_rectangles(haystack_img, rectangles, confs, names):

        names_ = ['Tower', 'Canon_Minion', 'caster_minion', 'Melee_Minion',  'Ezreal']

        for (rect, conf, name )in zip(rectangles, confs, names):

            line_type = cv.LINE_4
            top_left, bottom_right = (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3]))
            line_color = (0, 255, 0)
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
            cv.putText(haystack_img, names_[int(name)] + ' ' + str(conf), (int(top_left[0]), int(top_left[1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
            
        return haystack_img

    def draw_crosshairs(haystack_img, points):

        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:

            cv.drawMarker(haystack_img, (int(center_x),  int(center_y)), (0, 255, 0), marker_type)
        
        return haystack_img