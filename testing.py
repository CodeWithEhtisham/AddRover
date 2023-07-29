
# Schedule Library imported
import schedule
import time
thread = True
# Functions setup
def sudo_placement():
    global thread
    print("Get ready for Sudo Placement at Geeksforgeeks")
    thread = False

schedule.every(0.2).seconds.do(sudo_placement)

def good_luck():
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
        if not thread:
            print("thread is running")
            break
schedule.every(0.2).seconds.do(good_luck)
if schedule.run_pending():
    print("schedule is running")
    good_luck()