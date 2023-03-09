#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   tools.py
@Time    :   2023/3/510:10
@Author  :   Hu RunYang
@Version :   1.0
@Contact :   hurunyang@zxcsec.com
@License :   (C)Copyright 2017-2018, Liu group-NLP-CASA
@Desc    :   None
"""
import customtkinter
from tkinter import *
import SM3
import time
from tkinter import filedialog
from xml.etree import ElementTree as ET
from decimal import Decimal
from tksheet import Sheet

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("MuTool")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="工具箱", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="性能提取", command=self.init_showperf)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="SM3算法", command=self.SM3)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def init_showperf(self):
        self.perf_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color='#EEEEEE')
        self.perf_frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
        self.perf_name = customtkinter.CTkTextbox(self)
        self.perf_name.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.perf_source = customtkinter.CTkTextbox(self)
        self.perf_source.grid(row=0, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.perf_result = customtkinter.CTkTextbox(self)
        self.perf_result.grid(row=0, column=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.file_path = customtkinter.CTkTextbox(self, width=250, height=20)
        self.file_path.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), command=self.showperf, text='选择文件')
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


    def showperf(self):
        path = filedialog.askopenfilename(filetypes=[("日志文件", [".xml"])])
        self.file_path.insert(END, path)
        self.perf_name.delete(1.0, END)
        self.perf_source.delete(1.0, END)
        self.perf_result.delete(1.0, END)
        if path:
            try:
                tree = ET.parse(path)
                root = tree.getroot()
                perf = []
                for child in root:
                    for son in child:
                        if son.tag == 'cipherPerformance':
                            for grchild in son:
                                if 'SM3' in grchild.tag:
                                    perf.append(grchild)
                                else:
                                    for grson in grchild:
                                        perf.append(grson)
                        if son.tag == 'devicePerformance':
                            for grchild in son:
                                if 'con' not in child.tag:
                                    perf.append(grchild)
                                else:
                                    for grson in grchild:
                                        perf.append(grson)
                prename = ''
                name = 'non'
                for item in perf:
                    prename = name[:3]
                    res = '0'
                    for re in item:
                        if re.tag == 'performanceResult':
                            res = re.text
                        if (re.tag == 'usecaseName') & (type(re.text) == type('str')):
                            name = re.text.split(': ')[1]
                    if res != '0':
                        if (prename != 'non') & (prename != name[:3]):
                            self.perf_name.insert(END, '\n')
                            self.perf_source.insert(END, '\n')
                            self.perf_result.insert(END, '\n')
                        if name[2] not in ['1', '3', '4', '7']:
                            if ("加密" in name) | ("解密" in name):
                                res = res + "Kbps"
                            if ("签名" in name) | ("验签" in name):
                                res = res + "次/秒"
                            if "密钥" in name:
                                res = res + "对/秒"
                            if name == "随机数性能":
                                res = res + "Mbps"
                            if name == "对称密钥产生性能":
                                res = res + "组/秒"
                            if name == "非对称密钥产生性能":
                                res = res + "对/秒"
                            if "连接数" in name:
                                res = res + "条"
                            self.perf_name.insert(END, name + '\n')
                            self.perf_source.insert(END, res + '\n')
                            self.perf_result.insert(END, res + '\n')

                        else:
                            self.perf_name.insert(END, name + '\n')
                            self.perf_source.insert(END, res + 'Kbps' +'\n')
                            res = str(Decimal(str(float(res) / 1024)).quantize(Decimal("0.01"),
                                                                               rounding="ROUND_HALF_UP")) + 'Mbps'
                            self.perf_result.insert(END, res + '\n')
            except:
                self.perf_name.delete(1.0, END)
                self.perf_name.insert(1.0, "export performance failed")
        else:
            self.perf_name.delete(1.0, END)
            self.perf_name.insert(1.0, "ERROR:export performance failed")



    def SM3(self):
        self.sm3_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color='#EEEEEE')
        self.sm3_frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
        self.sm3source = customtkinter.CTkTextbox(self.sm3_frame, width=250)
        print('SM3_Hash')


if __name__ == "__main__":
    app = App()
    app.mainloop()