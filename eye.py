import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import speech_recognition as sr
import threading

pyautogui.FAILSAFE = False

print("Program started")

last_click = 0
smooth_x = 0
smooth_y = 0

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]

LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145

cam = cv2.VideoCapture(0)

def get_landmark_coords(landmarks,index,w,h):
    x = int(landmarks[index].x * w)
    y = int(landmarks[index].y * h)
    return np.array([x,y])

# ---------------- VOICE CONTROL ----------------

def voice_control():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Voice control started")

        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=3)
                command = recognizer.recognize_google(audio).lower()

                print("Voice:", command)

                if "click" in command:
                    pyautogui.click()

                elif "scroll down" in command:
                    pyautogui.scroll(-200)

                elif "scroll up" in command:
                    pyautogui.scroll(200)

                elif "stop" in command:
                    print("Stopping program")
                    exit()

            except:
                pass


voice_thread = threading.Thread(target=voice_control)
voice_thread.daemon = True
voice_thread.start()

# ---------------- CALIBRATION ----------------

print("Look straight at the screen for calibration")

center_samples = []

for i in range(50):

    ret, frame = cam.read()
    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:

        mesh_points = result.multi_face_landmarks[0].landmark

        left_iris = np.mean(
            [get_landmark_coords(mesh_points,i,frame.shape[1],frame.shape[0]) for i in LEFT_IRIS],
            axis=0)

        right_iris = np.mean(
            [get_landmark_coords(mesh_points,i,frame.shape[1],frame.shape[0]) for i in RIGHT_IRIS],
            axis=0)

        iris_center = (left_iris + right_iris) / 2
        center_samples.append(iris_center)

    cv2.putText(frame,"Calibrating...",(30,50),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Calibration",frame)
    cv2.waitKey(1)

center_point = np.mean(center_samples,axis=0)

print("Calibration complete")

# ---------------- MAIN LOOP ----------------

while True:

    ret,frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame,1)
    h,w,_ = frame.shape

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:

        mesh_points = result.multi_face_landmarks[0].landmark

        left_iris = np.mean(
            [get_landmark_coords(mesh_points,i,w,h) for i in LEFT_IRIS],
            axis=0)

        right_iris = np.mean(
            [get_landmark_coords(mesh_points,i,w,h) for i in RIGHT_IRIS],
            axis=0)

        iris_center = (left_iris + right_iris) / 2

        dx = iris_center[0] - center_point[0]
        dy = iris_center[1] - center_point[1]

        move_x = dx * 0.2
        move_y = dy * 0.2

        smooth_x = smooth_x * 0.7 + move_x * 0.3
        smooth_y = smooth_y * 0.7 + move_y * 0.3

        pyautogui.moveRel(int(smooth_x), int(smooth_y))

        cv2.circle(frame,tuple(left_iris.astype(int)),3,(0,255,0),-1)
        cv2.circle(frame,tuple(right_iris.astype(int)),3,(0,255,0),-1)

        # ---------- BLINK DETECTION ----------

        top = get_landmark_coords(mesh_points,LEFT_EYE_TOP,w,h)
        bottom = get_landmark_coords(mesh_points,LEFT_EYE_BOTTOM,w,h)

        blink_distance = np.linalg.norm(top-bottom)

        cv2.circle(frame,tuple(top.astype(int)),3,(255,0,0),-1)
        cv2.circle(frame,tuple(bottom.astype(int)),3,(255,0,0),-1)

        if blink_distance < 8 and time.time()-last_click > 1:
            pyautogui.click()
            last_click = time.time()

        # ---------- SCROLL ----------

        if dy > 40:
            pyautogui.scroll(-80)

        elif dy < -40:
            pyautogui.scroll(80)

    cv2.imshow("Eye + Voice Controlled Mouse",frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27 or key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()