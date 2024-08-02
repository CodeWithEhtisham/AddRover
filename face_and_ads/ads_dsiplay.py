import cv2
import os
from threading import Thread
import time

class ShowAds(Thread):
    def __init__(self, path):
        Thread.__init__(self)
        self.path = path
        self.window_name = "Frame"
        self.repeat = True

    def run(self):
        print("Thread started")
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:  # Loop to keep the ads running endlessly
            if not self.repeat:
                print("Ads list is empty. Waiting for new ads...")
                self.repeat = True

            ad_files = os.listdir(self.path)
            if len(ad_files) == 0:
                print("No ads found in the folder. Please add ads and try again.")
                break

            for file in ad_files:
                print(file)
                cap = cv2.VideoCapture(os.path.join(self.path, file))
                while True:
                    ret, frame = cap.read()
                    if ret:
                        # Adjust frame size to full screen resolution
                        cv2.imshow("Frame", frame)
                        time.sleep(0.1)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            break
                    else:
                        break
                cap.release()
                cv2.destroyAllWindows()
                self.repeat = False

if __name__ == "__main__":
    path = r"ads/"
    thread = ShowAds(path)
    thread.start()
