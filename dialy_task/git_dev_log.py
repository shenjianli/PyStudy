#!/usr/bin/python3
# -*- coding:utf-8 -*-

from loguru import logger
import os
import time

class GitDevLog:
    def __init__(self):
        self.tag = "GitDevLog"
        logger.add("logger.txt")
        self.is_dev = True
        # self.dev_path = "/Users/jerry/Desktop/oxford/code/dev/Oxford-FF"
        self.dev_path = "/Users/jerry/Desktop/oxford/code/dev/Module-OxfordAndroid"

    def log(self, log):
        if self.is_dev:
            logger.debug(f'{self.tag} : {log}')

    def out_git_log(self):
        origin_path = os.getcwd()
        print("当前目录：", os.getcwd())
        os.chdir(self.dev_path)
        print("切换目录：", os.getcwd())
        # git_log = 'git log --author="jerry" --after="2023-03-27 00:00:00" --before="2023-04-04 15:00:00"'
        git_log = f'git log --since=2.weeks --author="jerry" --author="Jerry" --oneline > {origin_path}/log.txt'
        os.system(git_log)
        os.chdir(origin_path)
    def out_week_log(self):
        result = []
        with open("log.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                for line in lines:
                    if not "Merge" in line and not "发布" in line \
                            and not "BD" in line and not "合并" in line:
                        log_text = line.replace("\n", "")
                        start_index = log_text.find(" ")
                        final_text = log_text[start_index:]
                        self.log(final_text)
                        if not final_text in result:
                            result.append(final_text)
            f.close()
        new_logs = result[::-1]
        self.log(result[::-1])
        # new_logs = new_logs[:12]
        final_logs = []
        diff = 0
        if len(new_logs) > 0:
            sentence_num = int(len(new_logs) / 5)
            index = 0
            log_content = ""
            if len(new_logs) % 5 == 0:
                diff = 1
            for log in new_logs:
                if len(log_content) > 0:
                    log_content = log_content + ";" + log
                else:
                    log_content = log
                index = index + 1
                if index < (len(new_logs) + diff - sentence_num):
                    if index % sentence_num == 0:
                        final_logs.append(log_content)
                        log_content = ""
            final_logs.append(log_content)
            self.log(final_logs)
            total_str = ""
            today_str = time.strftime("%Y.%m.%d", time.localtime())
            last_str = time.strftime("%Y.%m.%d", time.localtime(time.time() - 24 * 60 * 60 * 11))
            logger.info(f"{last_str}-{today_str}")
            total_str = f'{total_str}\n{last_str}-{today_str}'
            with open("final_log.txt","w") as f:
                f.write(f"{last_str}-{today_str}\n")
                index = 1
                for log in final_logs:
                    logger.info(f'{index}.{log}')
                    if index < 5:
                        f.write(f'{index}.{log}\n')
                    else:
                        f.write(f'{index}.{log}')
                    total_str = f'{total_str}\n{index}.{log}'
                    index = index + 1
                f.close()
            logger.info(total_str)
    def start(self):
        self.log("start")
        self.out_git_log()
        self.out_week_log()
        self.log("end")

if __name__ == '__main__':
    gitDevLog = GitDevLog()
    gitDevLog.start()