#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import time
import zipfile

import xlwings as xw
import json
class Excel2Json:
    def __init__(self):
        self.tag = "Excel2Json"
        self.dev = True
        self.project_root_path = os.getcwd()
    def log(self, log):
        if self.dev:
            print(log)

    def start(self, file_path):
        self.log("11")
        app = xw.App(visible=False,add_book=False)
        app.display_alerts = False
        app.screen_updating = False

        wb = app.books.open(file_path)
        self.log(len(wb.sheets))
        for index in range(0,len(wb.sheets)):
            self.log(index)
            work_sheet = wb.sheets[index]
            self.handle_sheet(work_sheet)
            self.log(work_sheet.name)
        wb.close()
        app.quit()
        self.generate_zip(self.project_root_path,"book.zip")

    def handle_sheet(self, work_sheet):
        titles = work_sheet.range('A1').expand('right').value
        nums = work_sheet.range('A2').expand('down').value
        self.log(titles)
        data = {}
        data_table = work_sheet.range('A2').expand('table').value
        self.log(data_table)
        datas = []
        if data_table is not None:
            for index in range(0, len(data_table)):
                temp_data = {}
                for sub_index in range(0, len(data_table[index])):
                    if data_table[index][sub_index] is None:
                        temp_data[titles[sub_index]] = ""
                    else:
                        temp_data[titles[sub_index]] = data_table[index][sub_index]
                datas.append(temp_data)
        data["datas"] = datas
        self.log(data)
        self.out_json_file(work_sheet.name,data)
        # self.log(nums)
        #
        # if nums is not None:
        #     for index in range(0, len(nums)):
        #         values = work_sheet.range('A' + str(index + 2)).expand('right').value
        #         self.log(values)

    def out_json_file(self,sheet_name,data):
        json_str = json.dumps(data)
        self.log(json_str)
        try:
            with open('{}.json'.format(sheet_name), 'w') as f:
                f.write(json_str)
        except Exception as ex:
            print(f'Error:{str(ex)}')

    def generate_zip(self,dist_dir, dist_name):
        zip_name = os.path.join(dist_dir, dist_name)
        zip = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
        time.sleep(2)
        for dir_path,dir_names,filenames in os.walk(dist_dir):
            fpath = dir_path.replace(dist_dir,"")
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                zip.write(os.path.join(dir_path,filename), fpath + filename)
                self.log("{}压缩中...".format(filename))
        self.log('{}压缩成功'.format(zip_name))
        zip.close()
if __name__ == '__main__':
    excel = Excel2Json()
    excel.log("start")
    excel.start("test.xlsx")
    excel.log("end")