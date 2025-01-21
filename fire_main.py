from ultralytics import YOLO
import cvzone
import cv2
import math
import playsound
import threading

find = None
level = 0
Alarm_Status = False
Fire_Reported = 0
alarm_event = threading.Event()


def play_alarm_sound_function():
    while alarm_event.is_set():
        playsound.playsound(r"E:\YOUTUBE-TUTORIAL-CODES\Fire Detector Course\1.wav", True)

# Running real time from webcam
# cap = cv2.VideoCapture("fire2.mp4")
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("rtsp://admin:SANDY123@192.168.1.100:554")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

model = YOLO('fire.pt')


# Reading the classes
classnames = ['fire']

while True:
    ret, frame = cap.read()
    
    frame = cv2.resize(frame, (640, 480))
    result = model(frame, stream=True)

    # Getting bbox, confidence, and class names information to work with
    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 50:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],
                                   scale=1.5, thickness=2)
                
                # Corrected: assign 'find' as a string
                find = classnames[Class]
                level = confidence
                print(find, level)

                # Correct condition: Compare `find` as a string and `confidence` as a number
                if (find == "fire" or find == "fires") and confidence > 75:
                    # Trigger the alarm
                    Alarm_Status = True
                    alarm_event.set()  # Start the alarm sound thread
                    threading.Thread(target=play_alarm_sound_function).start()

        if Fire_Reported == 0 and Alarm_Status:
            # Stop the alarm if fire is no longer detected
            Alarm_Status = False
            alarm_event.clear()  # Stop the alarm sound      

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    # cv2.waitKey(1)
