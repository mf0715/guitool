#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import SM3
import time
from tkinter import filedialog
from xml.etree import ElementTree as ET
from decimal import Decimal

LOG_LINE_NUM = 0


def get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time


class MY_GUI:
    def __init__(self, init_window_name):
        self.str_trans_to_md5_button = None
        self.log_data_Text = None
        self.result_data_Text = None
        self.init_data_Text = None
        self.log_label = None
        self.result_data_label = None
        self.init_data_label = None
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("MuTools")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高 标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="SM3杂凑", bg="lightblue", width=10,
                                              command=self.hex_str_sm3)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=11)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="性能提取", bg="lightblue", width=10,
                                              command=self.str_export_perf)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=2, column=11)

    # 功能函数
    # SM3杂凑运算
    def hex_str_sm3(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "")
        if src:
            try:
                res = SM3.SM3_Hash(src)
                # 输出到界面
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, res)
                self.write_log_to_Text("INFO:SM3_Hash success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "ERROR:SM3_Hash failed")
        else:
            self.write_log_to_Text("ERROR:SM3_Hash failed")

    # 从密码机及密码卡日志中提取算法性能数据
    def str_export_perf(self):
        self.init_data_Text.delete(1.0, END)
        path = filedialog.askopenfilename(filetypes=[("日志文件",[".xml"])])
        if path:
            try:
                self.result_data_Text.delete(1.0, END)
                tree = ET.parse(path)
                root = tree.getroot()
                for child in root:
                    for son in child:
                        if son.tag == 'cipherPerformance':
                            tem = son
                perf = []
                for child in tem:
                    if 'SM3' in child.tag:
                        perf.append(child)
                    else:
                        for son in child:
                            perf.append(son)
                prename = ''
                name = 'non'
                for item in perf:
                    prename = name[:3]
                    for re in item:
                        if re.tag == 'performanceResult':
                            res = re.text
                        if (re.tag == 'usecaseName') & (type(re.text) == type('str')):
                            name = re.text.split(': ')[1]
                    if res != '0':
                        if (prename != 'non') & (prename != name[:3]):
                            self.init_data_Text.insert(END, '\n')
                            self.result_data_Text.insert(END, '\n')
                        if ('SM2' in name) | ('RSA' in name):
                            if ("加密" in name) | ("解密" in name):
                                res = res + "Kbps"
                            if ("签名" in name) | ("验签" in name):
                                res = res + "次/秒"
                            if "密钥" in name:
                                res = res + "对/秒"
                            self.init_data_Text.insert(END, name + " " + res + '\n')
                            self.result_data_Text.insert(END, res + '\n')
                        else:
                            self.init_data_Text.insert(END, name + " " + res + "Kbps" + '\n')
                            res = str(Decimal(str(float(res) / 1024)).quantize(Decimal("0.01"),
                                                                               rounding="ROUND_HALF_UP")) + 'Mbps'
                            self.result_data_Text.insert(END, res + '\n')


                devperf = []
                self.init_data_Text.insert(END, '\n')
                self.result_data_Text.insert(END, '\n')
                for child in root:
                    for son in child:
                        if son.tag == 'devicePerformance':
                            tem = son
                for child in tem:
                    if 'con' not in child.tag:
                        devperf.append(child)
                    else:
                        for son in child:
                            devperf.append(son)
                for item in devperf:
                    for re in item:
                        if re.tag == 'performanceResult':
                            res = re.text
                        if (re.tag == 'usecaseName') & (type(re.text) == type('str')):
                            name = re.text.split(': ')[1]
                    if res != '0':
                        if name == "随机数性能":
                            res = res + "Mbps"
                        if name == "对称密钥产生性能":
                            res = res + "组/秒"
                        if name == "非对称密钥产生性能":
                            res = res + "对/秒"
                        if "连接数" in name:
                            res = res + "条"
                        self.init_data_Text.insert(END, name + " " + res + '\n')
                        self.result_data_Text.insert(END, res + '\n')
                self.write_log_to_Text("INFO:export performance from " + path + " success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "export performance failed")
        else:
            self.write_log_to_Text("ERROR:export performance failed")

    # 获取当前时间

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
