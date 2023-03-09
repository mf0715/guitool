import customtkinter
from tkinter import *
import SM3
import time
from tkinter import filedialog
from xml.etree import ElementTree as ET
from decimal import Decimal
from tksheet import Sheet


def get_perf(path):
    global resu
    perf_name = []
    perf_source = []
    perf_result = []
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
                    if name[2] not in ['1', '3', '4', '7']:
                        if ("加密" in name) | ("解密" in name):
                            res = res + "Kbps"
                        if ("签名" in name) | ("验签" in name):
                            res = res + "次/秒"
                        if ("密钥" in name) &  ("2" in name):
                            res = res + "对/秒"
                        if name == "随机数性能":
                            res = res + "Mbps"
                        if name == "对称密钥产生性能":
                            res = res + "组/秒"
                        if name == "非对称密钥产生性能":
                            res = res + "对/秒"
                        if "连接数" in name:
                            res = res + "条"
                        perf_name.append(name)
                        perf_source.append(res)
                        perf_result.append(res)

                    else:
                        perf_name.append(name)
                        perf_source.append(res)
                        res = str(Decimal(str(float(res) / 1024)).quantize(Decimal("0.01"),
                                                                           rounding="ROUND_HALF_UP")) + 'Mbps'
                        perf_result.append(res)
                resu = [perf_name, perf_source, perf_result]
        except:
            resu = ["ERROR"]
    else:
        resu = ["ERROR"]
    return resu


if __name__ == "__main__":
    print(get_perf("CCTC-AK-2023-0002-0228173951.xml"))
