from datetime import datetime
from tkinter import *
from pathlib import Path
from tkinter import filedialog, messagebox
import threading
import time
import pyperclip as pc
import os
import heapq




bak = "backup file"


name = ["ERROR", "dyy", "wyl", "wjh", "wrx", "yzy", "jtk", "rjj", "lty",
            "ljy", "yzy", "lxy", "lyz", "chz", "yh", "lzh", "zyh", "jck", "zcy",
            "hyz", "yjy", "xzs", "hjj", "mzy", "gyc", "xjq", "byh", "dfh", "mry",
            "wzy", "wzy", "fy", "yzx", "ssy", "lxy", "gx", "lxy", "lyl", "yx",
            "zzs", "cy", "sq", "hjy", "hjm", "xny", "xqx", "hkq", "sx", "jkl", "xfx"]


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return "assets/"+path

inputed_num = 0
scores = [ -114514 ]
for i in range(50):
    scores.append( -114514 )

def beautynum(a):
    if (int(a) != a):
        a = format(a, '.1f')
    else:
        a = int(a)
    return a

def log(level, content):
    
    res = "[" + datetime.now().strftime("%H:%M:%S") + "]"
    if level == 1: res += "[Info] "
    if level == 2: res += "[Warn] "
    if level == 3: res += "[Error]"
    print(res + content)
    res += content + "\n"
    entry_1.configure(state="normal")
    entry_1.insert("end",res)
    entry_1.configure(state="disabled")
    entry_1.yview_moveto(1)
    entry_1.update()

def deal_input(st):
        
    try:
        no, score = st.split()
        no = int(no)
        score = float(score)
    except:
        log(2, "数据不合法，无法识别学号和分数")
        messagebox.showwarning("警告", "数据不合法，请检查输入数据")
        return

    
    try:
        if (scores[no] == -114514):
            global inputed_num
            inputed_num += 1
        else:
            log(2, "数据发生覆盖，请三思！")
            log(2, str(no) + " " + str(scores[no]) + "->" + str(score))
        scores[no] = score
    except IndexError:
        log(2, "数据不合法，学号超出范围")
        messagebox.showwarning("警告", "数据不合法，请检查输入数据")
    except ValueError:
        log(2, "数据不合法，分数无法识别")
        messagebox.showwarning("警告", "数据不合法，请检查输入数据")
    else:
        log(1, "分数进入列表")
        
    
    canvas.itemconfig(tk_inputed_num,text=str(inputed_num))
    
    score_havescore = []
    for i in scores:
        if i != -114514:
            score_havescore.append(i)
    score_havescore.sort()
    
    mid = beautynum(score_havescore[int(len(score_havescore)/2)])
    avg = beautynum(sum(score_havescore)/len(score_havescore))
    Max = beautynum(score_havescore[-1])
    
    canvas.itemconfig(tk_avg_score,text=str(avg))
    canvas.itemconfig(tk_mid_score,text=str(mid))
    canvas.itemconfig(tk_max_score,text=str(Max))
    
    max_3 = list(map(scores.index, heapq.nlargest(3, scores)))
    
    res = ""
    
    if (max_3[0] == max_3[1]):
        for i in range(0, 50):
            if (scores[i] == scores[max_3[0]] and i != max_3[0]):
                max_3[1] = i
                break

    if (inputed_num > 3):
        res += "1) {} {}\n".format(name[max_3[0]], beautynum(scores[max_3[0]]))
        res += "2) {} {}\n".format(name[max_3[1]], beautynum(scores[max_3[1]]))
    
    if (inputed_num > 10): res += "10+ {} ↑\n".format(str(beautynum(score_havescore[10])))
    if (inputed_num > 20): res += "20+ {} ↑\n".format(str(beautynum(score_havescore[20])))
    if (inputed_num > 30): res += "30+ {} ↑\n".format(str(beautynum(score_havescore[30])))

    canvas.itemconfig(five_lines, text=res)
    
    pass


def submit(event):
    get = entry_2.get()
    log(1, "GUI输入 " + get)
    f = open(bak, "a")
    f.write(get + "\n")
    f.close()
    deal_input(get)
    entry_2.delete(0, END)
    return 'break'
    
def load_url(url):
    root = Tk()
    frame = th3.HtmlFrame(root, messages_enabled = False)
    frame.pack()
    frame.load_website(url)
    root.mainloop()

def import_bk_file():
    r = filedialog.askopenfilename(title='导入备份文件',
            filetypes=[('Text', '*.txt *.bak'), ('All files', '*')])
    log(1, "导入备份文件 " + r)
    with open(r) as f:
        read_data = f.read()
    log(1, "文件内容 " + read_data)
    for i in read_data.split('\n'):
        time.sleep(0.1)
        log(1, "备份输入 " + i)
        deal_input(i)

def export_bk_file():
    messagebox.showinfo("咕咕", "鸽")

def export_score():
    res = ""
    for i in range(1, 50):
        res += str(scores[i]) + "\n"
    pc.copy(res)
    messagebox.showinfo("Congratulations!", "分数信息已经逐行复制到剪贴板!")
    

master = Tk()
master.title("NeoScore [ Time 2022/08/30    Version 0.01 Beta    Author Iaraan ]")

menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label = "导入备份文件", command = import_bk_file)
filemenu.add_command(label = "导出备份文件", command = export_bk_file)
filemenu.add_command(label = "结束登分(手动)", command = export_score)
menubar.add_cascade(label = "文件", menu = filemenu)
master.configure(menu=menubar)
master.geometry("840x400")
master.configure(bg = "#C0CBE7")
master.resizable(False, False)
master.iconphoto(True, PhotoImage(file="icon.png"))

# Canvas
canvas = Canvas(master, bg = "#C0CBE7", height = 400, width = 840, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(524.0, 0.0, 830.0, 400.0, fill = "#D7F5D8", outline = "")

# 已输入个数
tk_inputed_num = canvas.create_text(60.0, 16.0, anchor = "nw", text = "--", fill = "#7B61FF", font = ("Microsoft Yahei", 90 * -1))
canvas.create_text(182.0, 57.0, anchor = "nw", text = "/49", fill = "#000000", font = ("Microsoft Yahei", 24 * -1))

# 中位
tk_mid_score = canvas.create_text(40.0, 131.0, anchor = "nw", text = "--", fill = "#000000", font = ("Microsoft Yahei", 56 * -1))
canvas.create_text(182.0, 153.0, anchor = "nw", text = "中位", fill = "#000000", font = ("Microsoft Yahei", 24 * -1))

# 平均
tk_avg_score = canvas.create_text(40.0, 213.0, anchor = "nw", text = "--", fill = "#000000", font = ("Microsoft Yahei", 56 * -1))
canvas.create_text(182.0, 235.0, anchor = "nw", text = "平均", fill = "#000000", font = ("Microsoft Yahei", 24 * -1))

# 最高
tk_max_score = canvas.create_text(40.0, 295.0, anchor = "nw", text = "--", fill = "#000000", font = ("Microsoft Yahei", 56 * -1))
canvas.create_text(182.0, 317.0, anchor = "nw", text = "最高", fill = "#000000", font = ("Microsoft Yahei", 24 * -1))

# 五行信息
five_lines = canvas.create_text(260.0, 37.0, anchor = "nw", text = "--", fill = "#000000", font = ("Consolas", 36 * -1))

# 日志
entry_image_1 = PhotoImage(file = relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(677.5, 161.5, image = entry_image_1)
entry_1 = Text(bd = 0, bg = "#C7FDCD", highlightthickness = 0, font = ("Microsoft Yahei", 12 * -1))
entry_1.configure(state = 'disabled')
entry_1.place(x = 556.0, y = 33.0, width = 243.0, height = 255.0, )

# 开源
canvas.create_text(307.0, 340.0, anchor = "nw", text = "Open Source Software\nWith The MIT License ", fill = "#5F6572", font = ("Consolas", 16 * -1))
opensource_image = PhotoImage(file = relative_to_assets("small.png"))
opensource_image_canvas = canvas.create_image(437.0, 290.0, image = opensource_image)

# 输入框
entry_image_2 = PhotoImage(file = relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(677.5, 328.5, image = entry_image_2)
entry_2 = Entry(bd = 0, bg = "#EEDCDC", highlightthickness = 0)
entry_2.bind("<Return>", submit)
entry_2.place(x = 556.0, y = 306.0, width = 243.0, height = 43.0)



bak = os.getcwd() + "\\Backup\\" + str(int(time.time())) + ".txt"

try:
    file = open(bak, 'w')
except FileNotFoundError:
    os.makedirs(os.getcwd() + "\\Backup")
    file = open(bak, 'w')

    
log(1, "新建备份文件 " + bak)


master.mainloop()
