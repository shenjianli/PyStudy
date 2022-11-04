from pynput.keyboard import Controller, Listener, Key


class KeyBoardRecorder(object):
    def __init__(self):
        self.tag = "KeyBoardRecorder"
        self.keys = []
        self.keyboard = Controller()

    def log(self, log):
        print(self.tag, log)

    def on_press(self,key):
        string = str(key).replace("'","")
        self.keys.append(string)
        main_string = " ".join(self.keys)
        self.log(f"已经输入 {main_string}")
        if len(main_string) > 150:
            with open('keys.txt', 'a') as f:
                self.log(f"写入文件 {main_string}")
                f.write(main_string + '\n')
                self.keys = []

    def on_release(self, key):
        if key == Key.esc:
            self.log("退出")
            return False

    def start(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == '__main__':
    keyboard = KeyBoardRecorder()
    keyboard.start()