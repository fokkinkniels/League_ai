import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt


class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    ATTACKING = 3


class LeagueBot:
    
    # Constants
    INITIALIZING_SECONDS = 2
    MOVEMENT_STOPPED_THRESHOLD = [0.92, 1]
    INFO_THRESHOLD = 0.7
    ATTACK_SPEED = 1.5
    WINDOW_OFFSET = None
    WINDOW_SIZE = None

    # Threading properties
    stopped = True
    lock = None

    # Properties
    state = None
    targets = []
    screenshot = None
    movement_screenshot = None
    is_update_screenshot = None
    caster_info = None
    timestamp = None
    click_history = []


    def __init__(self, window_offset, window_size):
        self.lock = Lock()

        self.WINDOW_OFFSET = window_offset
        self.WINDOW_SIZE = window_size

        self.caster_info = cv.imread(r'img\caster_info_new.png')

        self.state = BotState.INITIALIZING
        self.timestamp = time()


    def have_stopped_moving(self):
        if self.movement_screenshot is None:
            self.movement_screenshot = self.screenshot.copy()
            return False
        
        result = cv.matchTemplate(self.screenshot, self.movement_screenshot, cv.TM_CCOEFF_NORMED)
        
        similarity = result[0][0]
        print('Movement detection similarity {}'.format(similarity))

        if similarity > self.MOVEMENT_STOPPED_THRESHOLD[0] and similarity < self.MOVEMENT_STOPPED_THRESHOLD[1]:
            print('Movement detected stop')
            return True
        
        self.movement_screenshot = self.screenshot.copy()
        return False
                    

    
    def confirm_minion(self):
     
        result1 = cv.matchTemplate(self.caster_info, self.screenshot, cv.TM_CCOEFF_NORMED)
        result2 = cv.matchTemplate(self.caster_info, self.screenshot, cv.TM_CCOEFF_NORMED)
        result3 = cv.matchTemplate(self.caster_info, self.screenshot, cv.TM_CCOEFF_NORMED)
        result4 = cv.matchTemplate(self.caster_info, self.screenshot, cv.TM_CCOEFF_NORMED)

        min_val, max_val1, min_loc, max_loc = cv.minMaxLoc(result1)
        min_val, max_val2, min_loc, max_loc = cv.minMaxLoc(result2)
        min_val, max_val3, min_loc, max_loc = cv.minMaxLoc(result3)
        min_val, max_val4, min_loc, max_loc = cv.minMaxLoc(result4)

        max_vals = [max_val1, max_val2, max_val3, max_val4]
        max_val = max(max_vals)

        print(max_vals)
        print(max_val)

        if max_val >= self.INFO_THRESHOLD:
            return True
        
        return False



    def click_next_target(self):
    
        #targets = self.targets_ordered_by_distance()
        found_minion = False
        target_i = 0

        try:

            print('found {} targets'.format(len(self.targets)))

            while not found_minion and target_i < len(self.targets):

                if self.stopped:
                    break

                target_pos = self.targets[target_i]
                screen_x, screen_y = self.get_screen_position(target_pos)
                print('Moving mouse to x:{} y:{}'.format(screen_x, screen_y))

                pyautogui.moveTo(x = screen_x, y = screen_y)
                pyautogui.mouseDown(button=pyautogui.PRIMARY)
                pyautogui.mouseUp(button=pyautogui.PRIMARY)

                sleep(0.4)
                
                if self.confirm_minion():
                    pyautogui.mouseDown(button=pyautogui.SECONDARY)
                    pyautogui.mouseUp(button=pyautogui.SECONDARY)
                    found_minion = True
                    self.click_history.append(target_pos)

                target_i += 1
            return found_minion

        except Exception as e:
            pass

        


    def get_screen_position(self, pos):
        return (pos[0] + self.WINDOW_OFFSET[0], pos[1] + self.WINDOW_OFFSET[1])


    def targets_ordered_by_distance(self, targets):
        my_pos = (self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[1] / 2)

        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        return targets

        
    # Threading Functions
   
    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()  

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    # Main controller function     

    def run(self):
        while not self.stopped:

            if self.state == BotState.INITIALIZING:
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()


            elif self.state == BotState.SEARCHING:
                print('Searching')

                succes = self.click_next_target()

                if not succes:
                    succes = self.click_next_target()

                if succes:
                    self.lock.acquire()
                    self.state =  BotState.MOVING
                    self.lock.release()
                else:
                    pass


            elif self.state == BotState.MOVING:
                if self.have_stopped_moving():
                    self.lock.acquire()
                    self.timestamp = time()
                    self.state = BotState.ATTACKING
                    self.lock.release()
                else:
                    sleep(0.04)  # One Frame


            elif self.state == BotState.ATTACKING:
                if time() > self.timestamp + self.ATTACK_SPEED:
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()