#!/usr/bin/env python3

import pyautogui
import math
import cv2


class GestureManager:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.hand_Landmarks = None
        self.prev_hand = None
        self.right_clicked = False
        self.left_clicked = False
        self.double_clicked = False
        self.scrolling = False
        self.dragging = False
        self.little_finger_down = None
        self.little_finger_up = None
        self.index_finger_down = None
        self.index_finger_up = None
        self.index_finger_left=None
        self.middle_finger_down = None
        self.middle_finger_up = None
        self.ring_finger_down = None
        self.ring_finger_up = None
        self.Thump_finger_down = None
        self.Thump_finger_up = None
        self.all_fingers_down = None
        self.all_fingers_up = None
        self.index_finger_within_Thumb_finger = None
        self.middle_finger_within_Thumb_finger = None
        self.little_finger_within_Thumb_finger = None
        self.ring_finger_within_Thumb_finger = None
        self.fist_detect= False
        self.previous_time = None
        self.speed = 1
        self.hand_speed_threshold=700
        self.ratio=1
        self.senatslow=1
        self.senathigh=1
        self.cursor_move=False

    # def update_fingers_status(self):
        
    #     self.little_finger_down = self.hand_Landmarks.landmark[20].y > self.hand_Landmarks.landmark[17].y
    #     self.little_finger_up = self.hand_Landmarks.landmark[20].y < self.hand_Landmarks.landmark[5].y
    #     self.index_finger_left = self.hand_Landmarks.landmark[8].x < self.hand_Landmarks.landmark[6].x and self.hand_Landmarks.landmark[8].y > self.hand_Landmarks.landmark[4].y
    #     self.index_finger_down = self.hand_Landmarks.landmark[8].y > self.hand_Landmarks.landmark[5].y
    #     # self.index_finger_up = self.hand_Landmarks.landmark[8].y < self.hand_Landmarks.landmark[5].y
    #     self.middle_finger_down = self.hand_Landmarks.landmark[12].y > self.hand_Landmarks.landmark[10].y
    #     # self.middle_finger_up = self.hand_Landmarks.landmark[12].y < self.hand_Landmarks.landmark[9].y
    #     self.ring_finger_down = self.hand_Landmarks.landmark[16].y > self.hand_Landmarks.landmark[13].y
    #     # self.ring_finger_up = self.hand_Landmarks.landmark[16].y < self.hand_Landmarks.landmark[13].y
    #     self.Thump_finger_down = self.hand_Landmarks.landmark[4].y > self.hand_Landmarks.landmark[13].y
    #     self.Thump_finger_up = self.hand_Landmarks.landmark[4].y < self.hand_Landmarks.landmark[5].y
        
    #     self.all_fingers_down = self.index_finger_down and self.middle_finger_down and self.ring_finger_down and self.little_finger_down
        
    def get_position(self, hand_x_position, hand_y_position):
        #slow threshold
        
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * self.screen_width)
        current_y = int(hand_y_position * self.screen_height)
        
        self.prev_hand = (current_x, current_y) if self.prev_hand is None else self.prev_hand
        delta_x = current_x - self.prev_hand[0]
        delta_y = current_y - self.prev_hand[1]
        displacement = math.sqrt(delta_x ** 2 + delta_y ** 2)  # Displacement magnitude
        current_time = cv2.getTickCount()
        if self.previous_time != None:
            elapsed_time = (current_time - self.previous_time) / cv2.getTickFrequency()  # Time in seconds
            self.speed = displacement / elapsed_time  # Speed in pixels per second
            # print(self.speed)
            if self.speed > self.hand_speed_threshold:
                self.ratio = self.senathigh    # sensitivity at high hand speed
            else:
                self.ratio = self.senatslow   # sensitivity at low hand speed
            
            
        self.prev_hand = [current_x, current_y]
        self.previous_time = cv2.getTickCount()
        current_x , current_y = old_x + delta_x * self.ratio , old_y + delta_y * self.ratio

        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > self.screen_width - threshold:
            current_x = self.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > self.screen_height - threshold:
            current_y = self.screen_height - threshold

        return (current_x,current_y)
    
    
    def detect_clicking(self):
        threshold = 0.1
        left_click_condition = (math.sqrt((self.hand_Landmarks.landmark[4].x - self.hand_Landmarks.landmark[8].x) ** 2 + (self.hand_Landmarks.landmark[4].y - self.hand_Landmarks.landmark[8].y) ** 2) < threshold)
        if  not self.left_clicked and left_click_condition and self.speed<self.hand_speed_threshold and not self.scrolling:#and not self.left_clicked
            pyautogui.click()
            self.left_clicked = True
            # print("Left Clicking")
        else:
            self.left_clicked = False
        # elif not self.index_finger_within_Thumb_finger:
        #     self.left_clicked = False
        right_click_condition = (math.sqrt((self.hand_Landmarks.landmark[2].x - self.hand_Landmarks.landmark[8].x) ** 2 + (self.hand_Landmarks.landmark[2].y - self.hand_Landmarks.landmark[8].y) ** 2) < threshold)
        if not self.right_clicked and right_click_condition and self.speed<self.hand_speed_threshold and not self.scrolling:#not self.right_clicked and
            pyautogui.rightClick()
            self.right_clicked = True
            # print("Right Clicking")
        else:
            self.right_clicked = False
        # elif not self.middle_finger_within_Thumb_finger:
        #     self.right_clicked = False

        # double_click_condition = self.ring_finger_within_Thumb_finger and self.index_finger_up and self.middle_finger_up and self.little_finger_up and not self.index_finger_within_Thumb_finger and not self.middle_finger_within_Thumb_finger and not self.little_finger_within_Thumb_finger
        # if not self.double_clicked and  double_click_condition:
        #     pyautogui.doubleClick()
        #     self.double_clicked = True
        # print("Double Clicking")
        # elif not self.ring_finger_within_Thumb_finger:
        #     self.double_clicked = False
    def cursor_moving(self):
        point = 12
        current_x, current_y = self.hand_Landmarks.landmark[point].x ,self.hand_Landmarks.landmark[point].y
        x, y = self.get_position(current_x, current_y)
        
        if self.speed > self.hand_speed_threshold:
            duration = 0
        else :
            duration=0.2
        cursor_freezed = self.little_finger_up #and self.Thump_finger_down
        #if not cursor_freezed and self.index_finger_left:
        if not self.left_clicked and not self.right_clicked and  not self.middle_finger_down and not self.scrolling and self.speed > 200:
            pyautogui.moveTo(x, y, duration )
            self.cursor_move=True
        else :
            self.cursor_move=False
        # print("Moving")

    def detect_scrolling(self):
        mindis = 0.1
        scrolling_up =  self.hand_Landmarks.landmark[16].y > self.hand_Landmarks.landmark[14].y and self.hand_Landmarks.landmark[20].y > self.hand_Landmarks.landmark[18].y
        if scrolling_up and not self.left_clicked and not self.right_clicked  and (math.sqrt((self.hand_Landmarks.landmark[4].x - self.hand_Landmarks.landmark[16].x) ** 2 + (self.hand_Landmarks.landmark[4].y - self.hand_Landmarks.landmark[20].y) ** 2) > mindis):
            pyautogui.scroll(120)
            # print("Scrolling UP")
            self.scrolling = True
        else:
            self.scrolling = False

        scrolling_down = self.hand_Landmarks.landmark[16].y > self.hand_Landmarks.landmark[14].y and not self.hand_Landmarks.landmark[20].y > self.hand_Landmarks.landmark[18].y
        if scrolling_down and not self.dragging and (math.sqrt((self.hand_Landmarks.landmark[4].x - self.hand_Landmarks.landmark[16].x) ** 2 + (self.hand_Landmarks.landmark[4].y - self.hand_Landmarks.landmark[20].y) ** 2) > mindis):
            pyautogui.scroll(-120)
            # print("Scrolling DOWN")
            self.scrolling = True
        else:
            self.scrolling= False
    

    # def detect_zoomming(self):
    #     zoomming = self.index_finger_up and self.middle_finger_up and self.ring_finger_down and self.little_finger_down
    #     window = .05
    #     index_touches_middle = abs(self.hand_Landmarks.landmark[8].x - self.hand_Landmarks.landmark[12].x) <= window
    #     zoomming_out = zoomming and index_touches_middle
    #     zoomming_in = zoomming and not index_touches_middle
        
    #     if zoomming_out:
    #         pyautogui.keyDown('ctrl')
    #         pyautogui.scroll(-50)
    #         pyautogui.keyUp('ctrl')
            # print("Zooming Out")

    #     if zoomming_in:
    #         pyautogui.keyDown('ctrl')
    #         pyautogui.scroll(50)
    #         pyautogui.keyUp('ctrl')
            # print("Zooming In")

    
    
    def detect_dragging(self):
        mindis=0.1
        if not self.dragging and (math.sqrt((self.hand_Landmarks.landmark[4].x - self.hand_Landmarks.landmark[16].x) ** 2 + (self.hand_Landmarks.landmark[4].y - self.hand_Landmarks.landmark[20].y) ** 2) < mindis):
            pyautogui.mouseDown(button = "left")
            self.dragging = True
            # print("Dragging")
        elif (math.sqrt((self.hand_Landmarks.landmark[4].x - self.hand_Landmarks.landmark[16].x) ** 2 + (self.hand_Landmarks.landmark[4].y - self.hand_Landmarks.landmark[20].y) ** 2) > mindis) and self.hand_Landmarks.landmark[20].y < self.hand_Landmarks.landmark[18].y:
            pyautogui.mouseUp(button = "left")
            self.dragging = False

    