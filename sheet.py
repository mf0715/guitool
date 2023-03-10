import customtkinter
import tkinter
import tksheet
import getperf
from tkinter import filedialog

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("light")


class SideFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label1 = customtkinter.CTkLabel(self, text="工具箱")
        self.label1.grid(row=0, column=0, padx=20, pady=20)
        self.button1 = customtkinter.CTkButton(self, text="性能提取", command=master.ShowPerf)
        self.button1.grid(row=1, column=0, padx=20, pady=5)
        self.button2 = customtkinter.CTkButton(self, text="随机数检测", command=master.randomtest)
        self.button2.grid(row=2, column=0, padx=20, pady=5)
        self.button3 = customtkinter.CTkButton(self, text="SM3算法")
        self.button3.grid(row=3, column=0, padx=20, pady=5)
        self.aboutbutton = customtkinter.CTkButton(self, text="关于")
        self.aboutbutton.grid(row=8, column=0, padx=20, pady=20, sticky="s")


class PerfFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.sheet = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.fileframe = customtkinter.CTkFrame(self, height=60)
        self.fileframe.grid(row=1, column=0, padx=20, sticky="sew")
        self.fileframe.grid_columnconfigure(1, weight=1)
        self.fileframe.grid_columnconfigure(0, weight=1)
        self.filepath = customtkinter.CTkTextbox(self.fileframe, height=20, width=1000)
        self.filepath.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.aboutbutton = customtkinter.CTkButton(self.fileframe, text="选择文件", command=self.getres)
        self.aboutbutton.grid(row=0, column=1, padx=20, pady=20, sticky="e")

    def getres(self):
        path = filedialog.askopenfilename(filetypes=[("日志文件", [".xml"])])
        # path = "CCTC-AK-2023-0002-0228173951.xml"
        self.filepath.delete(1.0, tkinter.END)
        self.filepath.insert(tkinter.END, path)
        res = getperf.get_perf(path)
        self.sheet = tksheet.Sheet(self, headers=["测试项", "源数据", "结果"], height=750, width=648,
                                   show_x_scrollbar=False,
                                   vertical_grid_to_end_of_window=True,
                                   horizontal_grid_to_end_of_window=True)
        self.sheet.enable_bindings()
        self.sheet.font(("Times New Roaman", 16, "normal"))
        self.sheet.header_font(("Times New Roaman", 16, "bold"))
        self.sheet.grid(row=0, column=0, padx=40, pady=40, sticky="ns")
        for i in range(3):
            self.sheet.column_width(column=i, width=200)
            self.sheet.set_column_data(i, values=res[i], add_rows=True, redraw=False)


class RandomFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(self, master, **kwargs)

        print(1)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.func = None
        self.title('MuTools')
        self.minsize(1440, 960)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.side = SideFrame(master=self)
        self.side.grid_rowconfigure(8, weight=1)
        self.side.grid(row=0, column=0, sticky="nsew")

    def ShowPerf(self):
        self.func = PerfFrame(master=self)
        self.func.grid(row=0, column=1, sticky="nsew")

    def randomtest(self):
        self.random = RandomFrame(mster=self)
        self.random.grid(row=0, column=1, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
