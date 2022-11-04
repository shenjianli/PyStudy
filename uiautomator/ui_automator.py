import uiautomator2 as u2
import time
import datetime

class UIAutomatorDemo(object):
    def __init__(self, package_name):
        self.d = u2.connect()
        self.tag = "uiautomator"
        self.package_name = package_name

    def log(self, log):
        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print(self.tag, "{}-{}".format(timestr, log))

    def start(self):
        self.log(self.d.info)

    def start_app_by_package_name(self):
        self.d.app_start(self.package_name)

    def stop_app_by_package_name(self):
        self.d.app_stop(self.package_name)

    def get_app_info(self):
        info = self.d.app_info(self.package_name)
        self.log(info)

    def save_app_icon(self):
        img = self.d.app_icon(self.package_name)
        img.save("app_{}_icon.png".format(self.package_name))

    def list_running_app(self):
        info = self.d.app_list_running()
        self.log(info)

    def wait_app(self):
        pid = self.d.app_wait(self.package_name, front=True, timeout=20.0)
        if not pid:
            self.log(self.package_name + "is not running")
        else:
            self.log("{} pid is %d".format(self.package_name) % pid)

    def check(self):
        check = self.d.healthcheck()
        self.log(check)

    def device_info(self):
        self.log("window size {}".format(self.d.window_size()))
        self.log("serial {}".format(self.d.serial))
        self.log("wlan ip {}".format(self.d.wlan_ip))
        self.log("current {}".format(self.d.app_current()))
        self.log("device info {}".format(self.d.device_info))

    def unlock(self):
        self.d.unlock()
        self.d.click(128, 1354)
        self.d.click(440, 1354)
        self.d.click(852, 1454)
        self.d.click(128, 1567)
        self.d.click(440, 1567)
        self.d.click(852, 1567)

    def dump_hierarchy(self):
        xml = self.d.dump_hierarchy()
        self.log(xml)

    def screen_record(self, video_name):
        self.d.screenrecord("{}.mp4".format(video_name))

    def stop_record(self):
        self.d.screenrecord.stop()

    def find_img(self, image_name):
        point_info = self.d.image(image_name)
        self.d.image.click(image_name, timeout=20)


if __name__ == '__main__':
    uiautomator2 = UIAutomatorDemo("com.ihumand.oxford.staging")
    uiautomator2.start()
    uiautomator2.unlock()
    uiautomator2.start_app_by_package_name()
    # uiautomator2.stop_app_by_package_name("com.ihumand.oxford.staging")
    uiautomator2.get_app_info()
    # uiautomator2.save_app_icon()
    uiautomator2.list_running_app()
    uiautomator2.wait_app()
    uiautomator2.check()
    uiautomator2.device_info()
    uiautomator2.dump_hierarchy()
    # uiautomator2.find_img("app_com.ihumand.oxford.staging_icon.png")



