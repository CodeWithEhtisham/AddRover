import sys
import cv2
import numpy as np

def calculate_distance(face_width, focal_length, actual_width):
    return (actual_width * focal_length) / face_width

def read_cam():
    # On versions of L4T previous to L4T 28.1, flip-method=2
    # Use the Jetson onboard camera
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
    if cap.isOpened():
        windowName = "Face Detection"
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, 640, 360)
        cv2.moveWindow(windowName, 0, 0)
        cv2.setWindowTitle(windowName, "Face Detection")

        showHelp = True
        font = cv2.FONT_HERSHEY_PLAIN
        helpText = "Face Detection"
        focal_length = 615  # Adjust this value based on your setup and camera focal length
        actual_face_width = 14  # Actual width of the face in centimeters

        while True:
            if cv2.getWindowProperty(windowName, 0) < 0:  # Check to see if the user closed the window
                # This will fail if the user closed the window; Nasties get printed to the console
                break
            ret_val, frame = cap.read()
            # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            grayRs = cv2.resize(frame, (640, 360))
            # grayRs = cv2.resize(gray_frame, (640, 360))
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            ### Change grayRs to frameRs if you need the face detector to work on RGB.
            faces = face_cascade.detectMultiScale(grayRs, 1.3, 5)
            for (x, y, w, h) in faces:
                grayRs = cv2.rectangle(grayRs, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Calculate the distance from the camera using face size and focal length
                face_width = w
                distance = calculate_distance(face_width, focal_length, actual_face_width)

                # Display the distance on the frame
                if distance < 50:  # You can adjust this threshold for when to display green or red text
                    color = (0, 255, 0)  # Green color for closer distance
                else:
                    color = (0, 0, 255)  # Red color for farther distance

                distance_text = f"Distance: {distance:.2f} cm"
                cv2.putText(grayRs, distance_text, (x, y - 10), font, 1.0, color, 2)

            displayBuf = grayRs

            if showHelp:
                cv2.putText(displayBuf, helpText, (11, 20), font, 1.0, (32, 32, 32), 4, cv2.LINE_AA)
                cv2.putText(displayBuf, helpText, (10, 20), font, 1.0, (240, 240, 240), 1, cv2.LINE_AA)
            cv2.imshow(windowName, displayBuf)
            key = cv2.waitKey(10)
            if key == 27:  # Check for ESC key
                cv2.destroyAllWindows()
                break

    else:
        print("Camera open failed")

if __name__ == '__main__':
    read_cam()
