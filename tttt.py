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
import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)




if __name__ == "__main__":
    app = App()
    app.mainloop()