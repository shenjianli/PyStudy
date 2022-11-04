from datetime import datetime
from playsound import playsound


class AlertHint(object):
    def __init__(self):
        self.tag = "AlertHint"

    def log(self, log):
        print(self.tag, log)

    def start(self):
        alert_time = input('Enter the time of alarm to be set: HH:MM:SS \n')
        alert_hour = alert_time[:2]
        alert_minute = alert_time[3:5]
        alert_seconds = alert_time[6:8]
        self.log("Setting up alarm")
        while True:
            now = datetime.now()
            self.log(now)
            # %H	以24小时制表示当前小时
            # %I	以12小时制表示当前小时
            current_hour = now.strftime("%H")
            current_minute = now.strftime("%M")
            current_seconds = now.strftime("%S")
            if alert_hour == current_hour:
                if alert_minute == current_minute:
                    if alert_seconds == current_seconds:
                        self.log("Wake Up!")
                        playsound("audio.mp3")
                        break


if __name__ == '__main__':
    alert = AlertHint()
    alert.log('start')

    now = datetime.now()
    alert.log(now)
    # %H	以24小时制表示当前小时
    # %I	以12小时制表示当前小时
    current_hour = now.strftime("%H")
    current_minute = now.strftime("%M")
    current_seconds = now.strftime("%S")
    alert.log(f"hour {current_hour}")
    alert.log(f"minute {current_minute}")
    alert.log(f"second {current_seconds}")
    alert.start()
    # playsound("audio.mp3")
    alert.log("end")
