from tkinter import *
import tkinter as tk
import threading
# import time

import cv2
import mediapipe as mp
#import logging#removable
from controller import GestureManager




loop_active = False
stop_signal = threading.Event()

new_width=170
new_height=150
manager = GestureManager()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
# static_image_mode=False,
#     model_complexity=1,
#     min_detection_confidence=0.80,
#     min_tracking_confidence=0.80,
#     max_num_hands=1)
cap = cv2.VideoCapture(0)




def while_loop():
    print("Loop is active")
    

    while not stop_signal.is_set():
        # Your loop logic here
        #print("Loop is active")


        ret, frame = cap.read()

        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        #resized_frame = cv2.resize(frame,(new_width,new_height))
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgbFrame)

        if results.multi_hand_landmarks:
            if len(results.multi_hand_landmarks) == 1:
                manager.hand_Landmarks = results.multi_hand_landmarks[0]

            manager.cursor_moving()
            manager.detect_scrolling()
            #manager.detect_zoomming()
            manager.detect_clicking()
            # manager.detect_dragging()
        # cv2.imshow("resized frame", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break


#user Interface


def toggle_loop():
    global loop_active
    loop_active = not loop_active
    if loop_active:
        # Start a new thread for the while loop
        stop_signal.clear()  # Clear the stop signal
        loop_thread = threading.Thread(target=while_loop)
        loop_thread.start()
    else:
        stop_signal.set()  # Set the stop signal to request thread termination



def close_app():
    stop_signal.set()  # Set the stop signal to stop the thread
    app.quit()



app = tk.Tk()
app.geometry("400x700")
app.title("Toggle While Loop")

bg_colour="#DCDCDC"


logo_image = tk.PhotoImage(file="logo.png")

logo_label = tk.Label(app, image=logo_image,height=100,width=100)
logo_label.pack(side=TOP, anchor="w") 


title=Label(app,text="Virtual mouse",border=0.4,relief=RAISED,font=("times new roman",30,"bold")).pack(side="top",anchor='n',fill=X)




#Start button
start_button = tk.Button(app, text="Start V.M.", command=toggle_loop)
start_button.pack()

# stop_button = tk.Button(app, text="Stop Loop", command=toggle_loop)
# stop_button.pack()

exit_button = tk.Button(app, text="Exit", command=close_app)
exit_button.pack()

title2=Label(app,pady=6).pack(fill=X)

#slider for sensitivity at slow hand movement
sen_at_slow = tk.Scale(app, from_=1, to=10, orient='horizontal', label='Sensitivity at slow speed:')
sen_at_slow.set(4)
manager.senatslow = sen_at_slow.get()
sen_at_slow.pack(fill=X)


title1=Label(app,pady=10).pack(fill=X)


#slider for sensitivity at high hand movement
sen_at_high = tk.Scale(app, from_=1, to=20, orient='horizontal', label='Sensitivity at high speed:')
sen_at_high.set(15)
manager.senathigh = sen_at_high.get()
sen_at_high.pack(fill=X)

title3=Label(app,pady=10).pack(fill=X)

#speed threshold
spthreshold = tk.Scale(app, from_=1, to=1000, orient='horizontal', label='Minimun speed count:')
spthreshold.set(700)
manager.hand_speed_threshold = spthreshold.get()
spthreshold.pack(fill=X)


try:
    icon = tk.PhotoImage(file="logo.png")  # Use PhotoImage for image files other than .ico
    app.call('wm', 'iconphoto', app._w, icon)
except tk.TclError:
    # If loading as PhotoImage fails, try setting as an icon (for .ico files)
    app.iconbitmap(default="logo.png")



app.mainloop()
