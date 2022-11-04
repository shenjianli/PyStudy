import subprocess


class AdbPhone(object):
    def __init__(self):
        self.tag = "AdbPhone"

    def log(self, log):
        print(self.tag, log)

    def main_adb(self, cm):
        p = subprocess.Popen(cm, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        (output, err_output) = p.communicate()
        self.log(output.decode("utf-8"))
        return output.decode("utf-8")

    def adb_devices(self):
        cmd = "adb devices"
        return self.main_adb(cmd)

    def screen_shot_pic(self, pic_name):
        cmd = "adb shell screencap -p /sdcard/{}.png".format(pic_name)
        return self.main_adb(cmd)

    # 无法使用了
    def screen_shot_video(self, video_name):
        cmd = "adb shell screenrecord --time-limit 15 --size 1280x720 --bit-rate 6000000 /mnt/sdcard/{}.mp4".format(video_name)
        return self.main_adb(cmd)

    def download_file(self, filename):
        cmd = "adb pull /sdcard/{}".format(filename)
        return self.main_adb(cmd)

    def swipe(self, x1, y1, x2, y2, duration):
        cmd = "adb shell input swipe {} {} {} {} {}".format(x1, y1, x2, y2, duration)
        return self.main_adb(cmd)

    def tap(self, x, y):
        cmd = "adb shell input tap {} {}".format(x, y)
        return self.main_adb(cmd)

    def key_event(self, keycode):
        cmd = "adb shell input keyevent {}".format(keycode)
        return self.main_adb(cmd)


if __name__ == '__main__':
    adbPhone = AdbPhone()
    adbPhone.log("start")
    # adbPhone.adb_devices()
    # adbPhone.screen_shot_pic("test")
    # adbPhone.download_file("test.png")
    # adbPhone.swipe(500, 1200, 500, 100, 1000)
    # adbPhone.tap(500, 1000)
    # adbPhone.screen_shot_video("test")
    # adbPhone.download_file("test.mp4")
    # 224 点亮屏幕  3 HOME键  26 电源键
    adbPhone.key_event(224)