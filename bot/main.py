from os import stat_result
import cv2 as cv
from time import time

from window_capture import WindowCapture
from vision import Vision
from Detection import Detection
from bot import LeagueBot, BotState

# Global variables
debug = False    
is_bot_in_action = False

# Initialize the Window Capture Class
wincap = WindowCapture(None)
vision_caster = Vision
detector = Detection()
bot = LeagueBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))

wincap.start()
detector.start()
bot.start()

loop_time = time()
# Main Loop
while(True):

    if wincap.screenshot is None:
        continue

    scr = wincap.screenshot

    detector.update(scr)

    if bot.state == BotState.INITIALIZING:
        targets = vision_caster.get_click_points(detector.rectangles)
        bot.update_targets(targets)

    elif bot.state == BotState.SEARCHING:
        targets = vision_caster.get_click_points(detector.rectangles)
        bot.update_screenshot(scr)
        bot.update_targets(targets)

    elif bot.state == BotState.MOVING:
        targets = vision_caster.get_click_points(detector.rectangles)
        bot.update_screenshot(scr)

    elif bot.state == BotState.ATTACKING:
        targets = vision_caster.get_click_points(detector.rectangles)
        bot.update_screenshot(scr)
        bot.update_targets(targets) 


    if debug:
        
        vision_caster.draw_rectangles(scr, detector.rectangles, detector.conf, detector.classes)
        cv.imshow('result', scr)

    ## Press Q to stop the application
    #print('FPS {}       {}'.format(int(1 / (time() - loop_time)), bot.state))
    loop_time = time()
    key = cv.waitKey(1)
    if key == ord('q'):
        detector.stop()
        wincap.stop()
        bot.stop()
        cv.destroyAllWindows()
        break