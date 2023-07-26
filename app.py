import cv2
import os
from threading import Thread
import time
from deepface import DeepFace

class ShowAds(Thread):
    def __init__(self, path):
        Thread.__init__(self)
        self.path = path

    def run(self):
        print("Ads Thread started")
        while True:
            ad_files = os.listdir(self.path)
            if len(ad_files) == 0:
                print("No ads found in the folder. Please add ads and try again.")
                break

            for file in ad_files:
                print(file)
                cap_ad = cv2.VideoCapture(os.path.join(self.path, file))
                while True:
                    ret, frame = cap_ad.read()
                    if ret:
                        # Adjust frame size to full screen resolution
                        cv2.imshow("Frame", frame)
                        time.sleep(0.1)

                        if cv2.waitKey(1) & 0xFF == ord("q") or not self.repeat:
                            break
                    else:
                        break
                cap_ad.release()
                cv2.destroyAllWindows()

class FaceDetection(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.window_name = "Face Detection"
        self.focal_length = 615  # Adjust this value based on your setup and camera focal length
        self.actual_face_width = 14  # Actual width of the face in centimeters

    def calculate_distance(self, face_width):
        return (self.actual_face_width * self.focal_length) / face_width

    def run(self):
        print("Face Detection Thread started")
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                try:
                    result = DeepFace.extract_faces(frame, detector_backend='ssd', align=True, enforce_detection=False)
                except KeyError:
                    result = None

                if result:
                    data = result[0]['facial_area']
                    x, y, w, h = data['x'], data['y'], data['w'], data['h']
                    face_width = w
                    distance = self.calculate_distance(face_width)

                    if distance < 50:  # You can adjust this threshold for when to stop the ads
                        ads_thread.repeat = False
                    else:
                        ads_thread.repeat = True

                    if x and y:
                        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    else:
                        print("Face not detected")

                    distance_text = f"Distance: {distance:.2f} cm"
                    cv2.putText(frame, distance_text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2)

                cv2.imshow(self.window_name, frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    path = r"ads/"
    ads_thread = ShowAds(path)
    face_thread = FaceDetection()

    ads_thread.start()
    face_thread.start()
