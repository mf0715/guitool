import customtkinter
import tkinter
import tksheet
import getperf
import SM3
from tkinter import filedialog

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("light")

path = ""


def tk_center():
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    width = 400
    height = 300
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    size = '{}x{}+{}+{}'.format(width, height, x, y)
    return size


class AboutWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(tk_center())
        self.title("关于")
        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)
        self.wm_attributes('-topmost', 1)


class FileFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.filepath = customtkinter.CTkTextbox(self, height=20)
        self.filepath.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.selectbutton = customtkinter.CTkButton(self, text="选择文件", command=self.FileSelect)
        self.selectbutton.grid(row=0, column=1, padx=20, pady=20, sticky="e")

    def FileSelect(self):
        global path
        path = filedialog.askopenfilename()
        self.filepath.delete(1.0, tkinter.END)
        self.filepath.insert(tkinter.END, path)


class inputFrame(customtkinter.CTkFrame):
    def __init__(self, input_name, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text=input_name, height=20)
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        self.input_box = customtkinter.CTkTextbox(self)
        self.input_box.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")


class SideFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.about_window = None
        self.label1 = customtkinter.CTkLabel(self, text="工具箱")
        self.label1.grid(row=0, column=0, padx=20, pady=20)
        self.button1 = customtkinter.CTkButton(self, text="性能提取", command=master.ShowPerf)
        self.button1.grid(row=1, column=0, padx=20, pady=5)
        self.button2 = customtkinter.CTkButton(self, text="随机数检测", command=master.randomtest)
        self.button2.grid(row=2, column=0, padx=20, pady=5)
        self.button3 = customtkinter.CTkButton(self, text="SM3算法", command=master.SM3Hash)
        self.button3.grid(row=3, column=0, padx=20, pady=5)
        self.button4 = customtkinter.CTkButton(self, text="文本处理", command=master.SM3Hash)
        self.button4.grid(row=4, column=0, padx=20, pady=5)
        self.aboutbutton = customtkinter.CTkButton(self, text="关于", command=self.open_about)
        self.aboutbutton.grid(row=8, column=0, padx=20, pady=20, sticky="s")

    def open_about(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(self)


class PerfFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.sheet = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.files = FileFrame(self, height=60)
        self.files.grid(row=1, column=0, padx=20, sticky="sew")

        self.start = customtkinter.CTkButton(self, text="开始", command=self.getres)
        self.start.grid(row=0, pady=20, padx=40, sticky="se")

    def getres(self):
        global path
        res = getperf.get_perf(path)
        self.sheet = tksheet.Sheet(self, headers=["测试项", "源数据", "结果"], height=750, width=648,
                                   show_x_scrollbar=False,
                                   vertical_grid_to_end_of_window=True,
                                   horizontal_grid_to_end_of_window=True)
        self.sheet.enable_bindings()
        self.sheet.font(("Times New Roman", 16, "normal"))
        self.sheet.header_font(("Times New Roman", 16, "bold"))
        self.sheet.grid(row=0, column=0, padx=40, pady=40, sticky="nsw")
        for i in range(3):
            self.sheet.column_width(column=i, width=200)
            self.sheet.set_column_data(i, values=res[i], add_rows=True, redraw=False)


class RandomFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        print("random")


class SM3Frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.message_input = inputFrame("消息原文", master=self)
        self.message_input.grid(row=0, column=0, sticky="nsew")
        self.key_input = inputFrame("HMAC密钥", master=self)
        self.key_input.grid(row=0, column=1, sticky="nsew")
        self.hash_output = inputFrame("HASH结果", master=self)
        self.hash_output.grid(row=1, column=0, sticky="nsew")
        self.hash_output = inputFrame("HMAC结果", master=self)
        self.hash_output.grid(row=1, column=1, sticky="nsew")

        print("sm3")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.sm3 = None
        self.random = None
        self.func = None
        self.title('MuTools')
        self.minsize(960, 720)
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
        self.random = RandomFrame(master=self)
        self.random.grid(row=0, column=1, sticky="nsew")

    def SM3Hash(self):
        self.sm3 = SM3Frame(master=self, corner_radius=0)
        self.sm3.grid(row=0, column=1, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
