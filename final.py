import tkinter
from tkinter import *
from tkinter import filedialog

import customtkinter
import tksheet
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import getperf

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
        self.filepath = unsuitable_Textbox(self, width=250, height=20)
        self.filepath.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.selectbutton = customtkinter.CTkButton(self, text="选择文件", command=lambda: self.filepath.new_insert(filedialog.askopenfilename()))
        self.selectbutton.grid(row=0, column=1, padx=20, pady=20, sticky="e")


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
        self.button2 = customtkinter.CTkButton(self, text="曲线读取", command=master.ShowReadTrace)
        self.button2.grid(row=2, column=0, padx=20, pady=5)
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


class ReadTraceFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # 曲线组件
        graphFrame = tkinter.Frame(self)  # 创建图表控件
        graphFrame.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        global tempGraphLabel
        tempGraphLabel = tempGraph(graphFrame, 13.5, 5)
        # 曲线信息组件
        info_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color='#EEEEEE')
        info_frame.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")

        # trace_name_label = customtkinter.CTkLabel(info_frame, width=50, text="曲线名称: ")
        # trace_name_label.grid(row=0, column=0, padx=(0, 0), pady=(20, 20), sticky="nsew")
        # trace_name = customtkinter.CTkTextbox(info_frame, width=50, height=20, fg_color='#EEEEEE')
        # trace_name.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # 文件选择组件
        self.file_frame = FileFrame(self)
        self.file_frame.grid(row=3, column=0, padx=(20, 0), pady=(0, 0), sticky="sew")


        number_of_points_label = customtkinter.CTkLabel(info_frame, width=50, text="点数: ")
        number_of_points_label.grid(row=0, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.number_of_points = unsuitable_Textbox(info_frame, width=150, height=20, fg_color='#EEEEEE')
        self.number_of_points.grid(row=0, column=3, padx=(0, 0), pady=(20, 20), sticky="nsew")
        self.number_of_points.new_insert("0")

        number_of_trace_label = customtkinter.CTkLabel(info_frame, width=50, text="曲线数: ")
        number_of_trace_label.grid(row=0, column=4, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.number_of_trace = unsuitable_Textbox(info_frame, width=100, height=20, fg_color='#EEEEEE')
        self.number_of_trace.grid(row=0, column=5, padx=(0, 0), pady=(20, 20), sticky="nsew")
        self.number_of_trace.new_insert("0")

        pc_length_label = customtkinter.CTkLabel(info_frame, width=50, text="明密文长度: ")
        pc_length_label.grid(row=0, column=6, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.pc_length = unsuitable_Textbox(info_frame, width=50, height=20, fg_color='#EEEEEE')
        self.pc_length.grid(row=0, column=7, padx=(0, 0), pady=(20, 20), sticky="nsew")
        self.pc_length.new_insert("0")

        trace_number_label = customtkinter.CTkLabel(info_frame, width=50, text="曲线编号: ")
        trace_number_label.grid(row=0, column=8, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.now_trace = customtkinter.CTkTextbox(info_frame, width=150, height=20)
        self.now_trace.grid(row=0, column=9, padx=(0, 0), pady=(20, 20), sticky="nsew")
        self.now_trace.insert(1.0, "0")
        select_button = customtkinter.CTkButton(info_frame, text="跳转", width=10, command=lambda: self.show_trace())
        select_button.grid(row=0, column=10, padx=(0, 0), pady=(20, 20), sticky="nsew")

        # 明密文组件
        pc_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color='#EEEEEE')
        pc_frame.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")
        pc_label = customtkinter.CTkLabel(pc_frame, width=50, text="明密文: ")
        pc_label.grid(row=0, column=0, padx=(20, 0), pady=(0, 20), sticky="nsew")
        self.pc = unsuitable_Textbox(pc_frame, width=750, height=60)
        self.pc.grid(row=0, column=1, padx=(0, 0), pady=(0, 20), sticky="nsew")

    def show_trace(self):
        path = self.file_frame.filepath.get(1.0, END).strip()
        if path:
            try:
                # 读取文件中的16进制数据
                with open(path, 'rb') as file:
                    temp = file.readline().hex()
                    # 16进制转ASCII
                    # we = bytes.fromhex(temp[0:4]).decode('utf-8')
                    # 提取曲线数量
                    nt = (int(temp[10:12], 16) << 24) + (int(temp[8:10], 16) << 16) + (
                            int(temp[6:8], 16) << 8) + int(
                        temp[4:6], 16)
                    # 提取点数量
                    np = (int(temp[22:24], 16) << 24) + (int(temp[20:22], 16) << 16) + (
                            int(temp[18:20], 16) << 8) + int(temp[16:18], 16)
                    # 提取明密文长度
                    pclen = (int(temp[36:38], 16) << 8) + int(temp[34:36], 16)
                    # 显示曲线
                    self.number_of_points.new_insert(str(np))
                    self.number_of_trace.new_insert(str(nt))
                    self.pc_length.new_insert(str(pclen))
                    # 显示曲线
                    self.draw_trace(int(self.now_trace.get(1.0, END).strip()))
                file.close()
            except:
                self.file_frame.filepath.new_insert("Read Failed")

    def draw_trace(self, trace_number):
        try:
            path = self.file_frame.filepath.get(1.0, END).strip()
            pclen = int(self.pc_length.get(1.0, END).strip())
            np = int(self.number_of_points.get(1.0, END).strip())
            file = open(path, 'rb')
            # 读取明密文数据
            file.seek(39 + ((pclen + np) * trace_number), 0)
            pcData = file.read(pclen).hex()
            self.pc.new_insert(pcData)
            # 读取曲线数据
            trace = []
            for i in range(np):
                point = file.read(1)
                point = int.from_bytes(point, byteorder='big', signed=True)
                trace.append(point)
            tempGraphLabel.updateMeltGraph(np, trace)
        except:
            self.pc.delete(1.0, END)
            self.pc.insert(1.0, "export performance failed")


class unsuitable_Textbox(customtkinter.CTkTextbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def new_insert(self, string):
        self.configure(state='normal')
        super().delete(1.0, END)
        super().insert(1.0, string)
        self.configure(state='disabled')


class tempGraph():
    def __init__(self, root, xlen, ylen):
        self.line11 = None
        self.fig11 = None
        self.root = root  # 主窗体
        self.canvas = tkinter.Canvas()  # 创建一块显示图形的画布
        self.figure = self.create_matplotlib(xlen, ylen)  # 返回matplotlib所画图形的figure对象
        self.showGraphIn(self.figure)  # 将figure显示在tkinter窗体上面

    '''生成fig'''

    def create_matplotlib(self, xlen, ylen):
        # 创建绘图对象f
        f = plt.figure(num=2, figsize=(xlen, ylen), dpi=100, edgecolor='green', frameon=True)
        # 创建一副子图
        self.fig11 = plt.subplot(1, 1, 1)
        self.line11, = self.fig11.plot([], [])
        # 绘制曲线图
        plt.rcParams['font.sans-serif'] = ['FangSong']
        # 正确显示连字符
        plt.rcParams['axes.unicode_minus'] = False

        def setLabel(fig, title, titleColor="red"):
            fig.set_title(title + "曲线", color=titleColor)  # 设置标题
            fig.set_xlabel('点')  # 设置x轴标签
            fig.set_ylabel("电压")  # 设置y轴标签

        setLabel(self.fig11, "设备1")
        # fig1.set_yticks([-1, -1 / 2, 0, 1 / 2, 1])  # 设置坐标轴刻度
        f.tight_layout()  # 自动紧凑布局
        return f

    '''把fig显示到tkinter'''

    def showGraphIn(self, figure):
        # 把绘制的图形显示到tkinter窗口上
        self.canvas = FigureCanvasTkAgg(figure, self.root)
        self.canvas.draw()  # 以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
        self.canvas.get_tk_widget().pack(side=tkinter.TOP)  # , fill=tk.BOTH, expand=1

    '''更新fig'''

    def updateMeltGraph(self, x, Data):
        x = [i for i in range(len(Data))]
        self.line11.set_xdata(x)  # x轴也必须更新
        self.line11.set_ydata(Data)  # 更新y轴数据
        #  更新x数据，但未更新绘图范围。当我把新数据放在绘图上时，它完全超出了范围。解决办法是增加：
        self.fig11.relim()
        self.fig11.autoscale_view()
        plt.draw()
        # self.canvas.draw_idle()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.ReadTrace = None
        self.func = None
        self.title("MuTools")
        self.geometry(f"{1100}x{580}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.side = SideFrame(master=self)
        self.side.grid_rowconfigure(8, weight=1)
        self.side.grid(row=0, column=0, sticky="nsew")

    def ShowPerf(self):
        self.func = PerfFrame(master=self)
        self.func.grid(row=0, column=1, sticky="nsew")

    def ShowReadTrace(self):
        self.ReadTrace = ReadTraceFrame(master=self)
        self.ReadTrace.grid(row=0, column=1, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
