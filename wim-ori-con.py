#!/usr/bin/env python3


"""
Copyright Andrew Wang, 2019
Distributed under the terms of the GNU General Public License.

This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This file is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""


#                                                              7MBMBL
#                                                              BBMBM:
#                                                             OBMBM,
#                                                             BMBM.
#                                                            OMBM,
#                             :uBBBR               s0H;     .MBM.
#                          ;DBMBMBMB,             MBMBM     RBM,
#                       :MBMBMBMBBB:             MBMBB     .BM:
#                     7BMBH sBMBMB,            :MBBBM      BM:
#                   UMBM,   BBBMB:            2MBBBM       r.
#                 vBMO     BMBMBi            BBBBBM                  rEBMBR,
#                 uS      BMBMBr           :BMBMBM                .RBMBMBMBM
#                        BMBMB7           SBMBMBB.               FMB    :BMB
#                       BMBMBs          :MBMBMBB.               BMB       ,
#                      BMBMBF          EMBMBMBM,               FMBM
#                     MBBMBX         iBMBMBBBM:                MBBBS
#                    OMBMB0        .MBM:uBBBB;                 OMBMB:
#                   DMBMBM        RBB7 ;BMBM;                   BMBMB
#                  ZMBMBB       DBM1  ;BMBMr      r.            cBMBMS
#                 1MBMBM      WMBS   ;BBBMc     sBB:             RBMBD
#                JMBMBM    :MBBK    ;BMBMc    JBMB.               BBMc
#               rBBMBB   iBMBS     ,BMBMS  .RMBM:                 BMB
#              ;MBBBMBZBMBMJ      .BBBMBZUBBMR.        .MBM:    .BMZ
#             :MBMBMBMBMB;       .BMBBBMBMB7           RBBBMBFPMBB,
#            .MBMBMBMBX.         BMBBBBM7               RBMBBBM0.
#            MBMB:;:.             i;:                      .
#           BBMO
#          MBMO
#         MBBB
#        MBBB
#       RBMB;
#      WBMBR
#     EBBBM.
#    UBMBMB                                         「叶え！みんなの夢――」
#   2BMBBB3
#  uBMBMBZ
# LBBBMB;
# :GSr.


import base64
import csv
import datetime
import hashlib
import imghdr
import json
import os
import shutil
import ssl
import struct
import tarfile
import urllib.request
import webbrowser
from itertools import cycle
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


# Setting this flag to True will disable checking for update.
DEBUG = False
# Incrementing this variable will force a call to first_time_run.
# Do this when dependency update is required.
VERSION = "20190901"
# GitHub repository for checking for update.
REPO = "WorldIsMonkey/orientation-lts"
QUESTION_TYPES = {
    "mc": {
        "num_questions": 40,
        "title": "选择题",
    },
    "sq": {
        "num_questions": 20,
        "title": "简答题",
    },
    "music": {
        "num_questions": 40,
        "title": "音乐题",
    },
    "tf": {
        "num_questions": 15,
        "title": "是非题",
    },
    "pic1": {
        "num_questions": 10,
        "title": "图片题 (遮挡)",
    },
    "pic2": {
        "num_questions": 10,
        "title": "图片题 (马赛克)",
    },
    "fc": {
        "num_questions": 0,
        "title": "冲刺题",
    },
}


class MultiListbox(Frame):
    def __init__(self, master=None, columns=2, data=[], row_select=True, **kwargs):
        '''makes a multicolumn listbox by combining a bunch of single listboxes
        with a single scrollbar
        :columns:
          (int) the number of columns
          OR (1D list or strings) the column headers
        :data:
          (1D iterable) auto add some data
        :row_select:
          (boolean) When True, clicking a cell selects the entire row
        All other kwargs are passed to the Listboxes'''
        Frame.__init__(self, master, borderwidth=1, highlightthickness=1, relief=SUNKEN)
        self.rowconfigure(1, weight=1)
        self.columns = columns
        if isinstance(self.columns, (list, tuple)):
            for col, text in enumerate(self.columns):
                Label(self, text=text).grid(row=0, column=col)
            self.columns = len(self.columns)

        self.boxes = []
        for col in range(self.columns):
            box = Listbox(self, exportselection=not row_select, **kwargs)
            if row_select:
                box.bind('<<ListboxSelect>>', self.selected)
            box.grid(row=1, column=col, sticky='nsew')
            self.columnconfigure(col, weight=1)
            self.boxes.append(box)
        vsb = Scrollbar(self, orient=VERTICAL,
            command=multiple(*[box.yview for box in self.boxes]))
        vsb.grid(row=1, column=col+1, sticky='ns')
        for box in self.boxes:
            box.config(yscrollcommand=scroll_to_view(vsb.set,
                *[b.yview for b in self.boxes if b is not box]))
        self.add_data(data)

    def selected(self, event=None):
        row = event.widget.curselection()[0]
        for lbox in self.boxes:
            lbox.select_clear(0, END)
            lbox.select_set(row)

    def add_data(self, data=[]):
        '''takes a 1D list of data and adds it row-wise
        If there is not enough data to fill the row, then the row is
        filled with empty strings
        these will not be back filled; every new call starts at column 0'''
        # it is essential that the listboxes all have the same length.
        # because the scroll works on "percent" ...
        # and 100% must mean the same in all cases
        boxes = cycle(self.boxes)
        idx = -1
        for idx, (item, box) in enumerate(zip(data, boxes)):
            box.insert(END, item)
        for _ in range(self.columns - idx%self.columns - 1):
            next(boxes).insert(END, '')

    def __getitem__(self, index):
        '''get a row'''
        return [box.get(index) for box in self.boxes]

    def __delitem__(self, index):
        '''delete a row'''
        [box.delete(index) for box in self.boxes]

    def curselection(self):
        '''get the currently selected row'''
        selection = self.boxes[0].curselection()
        return selection[0] if selection else None


def multiple(*func_list):
    '''run multiple functions as one'''
    # I can't decide if this is ugly or pretty
    return lambda *args, **kw: [func(*args, **kw) for func in func_list]; None


def scroll_to_view(scroll_set, *view_funcs):
    ''' Allows one widget to control the scroll bar and other widgets
    scroll set: the scrollbar set function
    view_funcs: other widget's view functions
    '''
    def closure(start, end):
        scroll_set(start, end)
        for func in view_funcs:
            func('moveto', start)
    return closure


def mkdir(path):
    os.makedirs(path, exist_ok=True)


def load_navigation_config():
    result = []
    for i in range(len(QUESTION_TYPES) - 1):
        result.append(False)
    try:
        file = open("data/navigation.config")
        count = 0
        for line in file:
            for bit in line:
                if bit == "1":
                    result[count] = True
                count += 1
        file.close()
        return result
    except FileNotFoundError:
        return result


def save_navigation_config(a, b, c):
    if not os.path.exists("data"):
        os.makedirs("data")
    with open("data/navigation.config", "w", encoding="utf-8", newline="\n") as navigation_config_file:
        for i in range(len(var)):
            value = str(IntVar.get(var[i]))
            if value == "0":
                set_btn_group_state(B[i], "disabled")
            else:
                set_btn_group_state(B[i], "normal")
            navigation_config_file.write(value)


def set_btn_group_state(btns, state):
    if isinstance(btns, tuple):
        for btn in btns:
            btn.config(state=state)
    else:
        btns.config(state=state)


def refresh_main_window():
    check_set(BGL, "data/bg.jpg")
    if os.path.exists("data/navigation.config"):
        enable = load_navigation_config()
        for i in range(len(enable)):
            if enable[i]:
                C[i].select()
    else:
        for v in var:
            v.set(0)


def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height


def check_dir_existance(question_type):
    mkdir("data/" + question_type + "/media")


def add_media(elem, question_type, filename, description, file_type, width=None, height=None, button=None, button_txt=None):
    selected = select_file(description, file_type)
    if selected:
        if (not width and not height) or check_image_size(selected, width, height):
            check_dir_existance(question_type)
            target = "data/" + question_type + "/media/" + filename
            shutil.copy(selected, target)
            check_set(elem, target, button, button_txt, question_type, filename)
            messagebox.showinfo("", "设定成功!")
        else:
            messagebox.showerror("", "图片分辨率必须为 {} x {}.".format(width, height))


def remove_media(elem, question_type, filename, button=None, button_txt=None):
    target = "data/" + question_type + "/media/" + filename
    os.remove(target)
    check_set(elem, target, button, button_txt, question_type, filename)


def select_file(description, file_type):
    root.update()
    filename = filedialog.askopenfilename(filetypes=[(description, file_type)])
    return filename


def check_image_size(filename, width, height):
    size = get_image_size(filename)
    return size == (width, height)


def select_bg():
    filename = select_file("JPG Files", "*.jpg")
    if filename:
        if check_image_size(filename, 1280, 800):
            if not os.path.exists("data"):
                os.makedirs("data")
            shutil.copy(filename, "data/bg.jpg")
            messagebox.showinfo("", "设定成功!")
        else:
            messagebox.showerror("", "图片分辨率必须为 1280 x 800.")
        check_set(BGL, "data/bg.jpg")


def check_set(label, file, button=None, button_txt=None, question_type=None, filename=None):
    if os.path.exists(file):
        label.config(text="已设定")
        label.config(fg="#4CAF50")
        if button:
            button.config(text="移除图片", command=lambda: remove_media(label, question_type, filename, button, button_txt))
    else:
        label.config(text="未设定")
        label.config(fg="red")
        if button:
            button.config(text=button_txt, command=lambda: add_media(label, question_type, filename, "JPG Files", "*.jpg", 256, 256, button, button_txt))


def update_question_list(question_type, ls):
    for i in range(QUESTION_TYPES[question_type]["num_questions"] + 1):
        ls.__delitem__(0)

    for i in range(QUESTION_TYPES[question_type]["num_questions"] + 1):
        try:
            with open("data/{}/{}.config".format(question_type, i), encoding="utf-8") as file:
                question = file.readline()
        except FileNotFoundError:
            question = ""

        try:
            time_modified = metadata[question_type][str(i)]
        except:
            time_modified = ""

        ls.add_data(["[{}] {}".format("规则文本" if i == 0 else i, question), time_modified])


def parse_multiple_choice(filename):
    mkdir("data/mc")
    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            i = i + 1
            question = line[0]
            option_a = line[1]
            option_b = line[2]
            option_c = line[3]
            option_d = line[4]
            correct_answer = ord(line[5]) - ord('A') + 1
            with open("data/mc/%s.config" % i, "wb") as config_file:
                string = "%s\n\n%s\n%s\n%s\n%s\n%s\n" % (question, option_a, option_b, option_c, option_d, correct_answer)
                config_file.write(string.encode("utf-8"))
            update_time_modified("mc", i)


def parse_short_answer(filename):
    mkdir("data/sq")
    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            i += 1
            question = line[0]
            answer = line[1]
            configString = "{0}\n\n{1}\nN/A\nN/A\nN/A\n-1".format(question, answer)
            with open("data/sq/{}.config".format(i), "w", encoding="utf-8", newline="\n") as config_file:
                config_file.write(configString)
            update_time_modified("sq", i)


def parse_true_or_false(filename):
    mkdir("data/tf")
    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            i += 1
            question = line[0]
            answer_string = line[1]
            if answer_string in {"T", "对"}:
                answer = "1"
            else:
                answer = "2"
            config_string = "{}\n\nN/A\nN/A\nN/A\nN/A\n{}\n".format(question, answer)
            with open("data/tf/{}.config".format(i), "w", encoding="utf-8", newline="\n") as config_file:
                config_file.write(config_string)
            update_time_modified("tf", i)


def import_csv(question_type, ls):
    selected = select_file("CSV Files", "*.csv")

    try:
        if not selected:
            return
        elif question_type == "mc":
            parse_multiple_choice(selected)
        elif question_type == "sq":
            parse_short_answer(selected)
        elif question_type == "tf":
            parse_true_or_false(selected)
        else:
            raise Exception("Unsupported question type")
    except Exception as e:
        messagebox.showerror("", str(e))

    update_question_list(question_type, ls)


def show_edit_title_window():
    title_edit = Tk()
    title_edit.title("")

    with open("data/title.config", encoding="utf-8", newline="\n") as file:
        TV = []
        for next_line in file:
            new_SV = StringVar(title_edit)
            new_SV.set(next_line.strip())
            TV.append(new_SV)

    T1 = Entry(title_edit, textvariable=TV[0])
    T2 = Entry(title_edit, textvariable=TV[1])
    T3 = Entry(title_edit, textvariable=TV[2])
    T4 = Entry(title_edit, textvariable=TV[3])
    T5 = Entry(title_edit, textvariable=TV[4])
    T6 = Entry(title_edit, textvariable=TV[5])

    T1.pack()
    T2.pack()
    T3.pack()
    T4.pack()
    T5.pack()
    T6.pack()

    saveBtn = Button(title_edit, text="Save", command=lambda: save_title(TV, title_edit))
    saveBtn.pack()

    title_edit.mainloop()


def save_title(TV, window):
    with open("data/title.config", "w", encoding="utf-8", newline="\n") as file:
        for e in TV:
            file.write(e.get())
            file.write("\n")

    window.destroy();


def show_question_list_window(question_type):
    num_questions = QUESTION_TYPES[question_type]["num_questions"]
    title = QUESTION_TYPES[question_type]["title"]

    window = Tk()
    window.title(title)

    ls = MultiListbox(window, ["Question", "Time Modified"], width=40)
    update_question_list(question_type, ls)

    frame = Frame(window)
    Button(frame, text="Edit", command=lambda: edit_question(question_type, ls)).pack(side=LEFT)
    if question_type in {"mc", "sq", "tf"}:
        Button(frame, text="Import CSV", command=lambda: import_csv(question_type, ls)).pack(side=LEFT)
        help = Label(frame, text="Help?", fg="blue", cursor="hand2")
        help.bind("<Button-1>", lambda e: open_browser("https://github.com/" + REPO + "/blob/master/QuestionReviewGuideline.md"))
        help.pack(side=LEFT)
        tip_text = "Tip: 你可以拖拽边缘来缩放本窗口."
    elif "pic" in question_type:
        tip_text = "Tip: 若图片不符合尺寸,请将图片进行缩放/剪裁,或在图片四周添加透明像素."
    elif question_type == "music":
        tip_text = "Tip: 请截取歌曲副歌部分."
    else:
        tip_text = ""
    Label(frame, text=tip_text, anchor="e").pack(fill=X)
    frame.pack(anchor="w", fill=X)
    ls.pack(fill=BOTH, expand=True)

    window.mainloop()


def edit_question(question_type, ls):
    index = ls.curselection()
    if index is None:
        return

    if index == 0:
        content = ""
        if os.path.exists("data/" + question_type + "/" + str(index) + ".config"):
            file = open("data/" + question_type + "/" + str(index) + ".config", encoding="utf-8")
            content = file.read()
            file.close()

        rule_edit = Tk()
        rule_edit.title("编辑 [规则文本]")

        box = Text(rule_edit)
        box.pack()
        box.insert(INSERT, content)

        save_btn = Button(rule_edit, text="Save", command=lambda: save_rule(question_type, box.get("1.0", END), rule_edit, ls))
        save_btn.pack()

        rule_edit.mainloop()
    else:
        content = None
        if os.path.exists("data/" + question_type + "/" + str(index) + ".config"):
            file = open("data/" + question_type + "/" + str(index) + ".config", encoding="utf-8")
            content = file.readlines()
            file.close()

        question_edit = Tk()
        question_edit.title("编辑 [第" + str(index) + "题]")

        SV = []
        IV = IntVar(question_edit)
        for i in range(7):
            if i < 6:
                SV.append(StringVar(question_edit))
            try:
                if content:
                    if i == 6:
                        IV.set(int(content[i].strip()))
                    else:
                        SV[i].set(content[i].strip())
            except IndexError:
                pass

        if question_type in {"mc", "sq", "tf"}:
            pic1_filename = str(index) + ".jpg"
            F1L = Label(question_edit)
            F1 = Button(question_edit)
            F1.grid(row=0, column=1)
            F1L.grid(row=0, column=0)
            check_set(F1L, "data/" + question_type + "/media/" + pic1_filename, F1, "添加图片 (optional, jpg, 256 x 256)", question_type, pic1_filename)

            L0 = Label(question_edit, text="问题第 1 行")
            L0.grid(row=1, column=0)
            E0 = Entry(question_edit, textvariable=SV[0])
            E0.grid(row=1, column=1)

            L1 = Label(question_edit, text="问题第 2 行")
            L1.grid(row=2, column=0)
            E1 = Entry(question_edit, textvariable=SV[1])
            E1.grid(row=2, column=1)
        elif question_type == "music":
            L0 = Label(question_edit, text="番名")
            L0.grid(row=1, column=0)
            E0 = Entry(question_edit, textvariable=SV[0])
            E0.grid(row=1, column=1)

            L1 = Label(question_edit, text="歌名")
            L1.grid(row=2, column=0)
            E1 = Entry(question_edit, textvariable=SV[1])
            E1.grid(row=2, column=1)
        elif question_type in {"pic1", "pic2"}:
            L0 = Label(question_edit, text="答案")
            L0.grid(row=1, column=0)
            E0 = Entry(question_edit, textvariable=SV[0])
            E0.grid(row=1, column=1)
            L1 = Label(question_edit, text="字号")
            L1.grid(row=2, column=0)
            if not IV.get():
                IV.set(48)
            font_size = Scale(question_edit, variable=IV, orient=HORIZONTAL, length=150, from_=16, to=48)
            font_size.grid(row=2, column=1)

        if question_type == "sq":
            L2 = Label(question_edit, text="答案")
            L2.grid(row=3, column=0)
            E2 = Entry(question_edit, textvariable=SV[2])
            E2.grid(row=3, column=1)

        if question_type == "mc":
            L2 = Label(question_edit, text="A 选项")
            L2.grid(row=3, column=0)
            E2 = Entry(question_edit, textvariable=SV[2])
            E2.grid(row=3, column=1)

            L3 = Label(question_edit, text="B 选项")
            L3.grid(row=4, column=0)
            E3 = Entry(question_edit, textvariable=SV[3])
            E3.grid(row=4, column=1)

            L4 = Label(question_edit, text="C 选项")
            L4.grid(row=5, column=0)
            E4 = Entry(question_edit, textvariable=SV[4])
            E4.grid(row=5, column=1)

            L5 = Label(question_edit, text="D 选项")
            L5.grid(row=6, column=0)
            E5 = Entry(question_edit, textvariable=SV[5])
            E5.grid(row=6, column=1)

            L5 = Label(question_edit, text="答案")
            L5.grid(row=7, column=0)
            R1 = Radiobutton(question_edit, text="A", variable=IV, value=1)
            R2 = Radiobutton(question_edit, text="B", variable=IV, value=2)
            R3 = Radiobutton(question_edit, text="C", variable=IV, value=3)
            R4 = Radiobutton(question_edit, text="D", variable=IV, value=4)
            R1.grid(row=7, column=1)
            R2.grid(row=8, column=1)
            R3.grid(row=9, column=1)
            R4.grid(row=10, column=1)
        elif question_type == "music":
            L5 = Label(question_edit, text="出现位置")
            L5.grid(row=6, column=0)
            R1 = Radiobutton(question_edit, text="N/A", variable=IV, value=1)
            R2 = Radiobutton(question_edit, text="OP", variable=IV, value=2)
            R3 = Radiobutton(question_edit, text="ED", variable=IV, value=3)
            R4 = Radiobutton(question_edit, text="挿入歌", variable=IV, value=4)
            R1.grid(row=6, column=1)
            R2.grid(row=7, column=1)
            R3.grid(row=8, column=1)
            R4.grid(row=9, column=1)
        elif question_type == "tf":
            L5 = Label(question_edit, text="答案")
            L5.grid(row=7, column=0)
            R1 = Radiobutton(question_edit, text="True", variable=IV, value=1)
            R2 = Radiobutton(question_edit, text="False", variable=IV, value=2)
            R1.grid(row=7, column=1)
            R2.grid(row=8, column=1)

        if question_type == "music":
            audio_filename = str(index) + ".mp3"
            video_filename = str(index) + ".mp4"
            F1L = Label(question_edit)
            F2L = Label(question_edit)
            F1 = Button(question_edit, text="音频 (mp3, exactly 20s)", command=lambda: add_media(F1L, "music", audio_filename, "MP3 Files", "*.mp3"))
            F2 = Button(question_edit, text="视频 (mp4, 1280 x 720)", command=lambda: add_media(F2L, "music", video_filename, "MP4 Files", "*.mp4"))
            F1.grid(row=10, column=1)
            F2.grid(row=11, column=1)
            F1L.grid(row=10, column=0)
            F2L.grid(row=11, column=0)
            check_set(F1L, "data/" + question_type + "/media/" + audio_filename)
            check_set(F2L, "data/" + question_type + "/media/" + video_filename)
        elif question_type == "pic1":
            pic1_filename = str(index) + "-1.jpg"
            pic2_filename = str(index) + "-2.jpg"
            F1L = Label(question_edit)
            F2L = Label(question_edit)
            F1 = Button(question_edit, text="问题图 (jpg, 1280 x 720)", command=lambda: add_media(F1L, "pic1", pic1_filename, "JPG Files", "*.jpg", 1280, 720))
            F2 = Button(question_edit, text="答案图 (jpg, 1280 x 720)", command=lambda: add_media(F2L, "pic1", pic2_filename, "JPG Files", "*.jpg", 1280, 720))
            F1.grid(row=10, column=1)
            F2.grid(row=11, column=1)
            F1L.grid(row=10, column=0)
            F2L.grid(row=11, column=0)
            check_set(F1L, "data/" + question_type + "/media/" + pic1_filename)
            check_set(F2L, "data/" + question_type + "/media/" + pic2_filename)
        elif question_type == "pic2":
            pic1_filename = str(index) + "-1.jpg"
            pic2_filename = str(index) + "-2.jpg"
            pic3_filename = str(index) + "-3.jpg"
            pic4_filename = str(index) + "-4.jpg"
            F1L = Label(question_edit)
            F2L = Label(question_edit)
            F3L = Label(question_edit)
            F4L = Label(question_edit)
            F1 = Button(question_edit, text="最模糊图片 (jpg, 1280 x 720)", command=lambda: add_media(F1L, "pic2", pic1_filename, "JPG Files", "*.jpg", 1280, 720))
            F2 = Button(question_edit, text="图片2 (jpg, 1280 x 720)", command=lambda: add_media(F2L, "pic2", pic2_filename, "JPG Files", "*.jpg", 1280, 720))
            F3 = Button(question_edit, text="图片3 (jpg, 1280 x 720)", command=lambda: add_media(F3L, "pic2", pic3_filename, "JPG Files", "*.jpg", 1280, 720))
            F4 = Button(question_edit, text="原图 (jpg, 1280 x 720)", command=lambda: add_media(F4L, "pic2", pic4_filename, "JPG Files", "*.jpg", 1280, 720))
            F1.grid(row=10, column=1)
            F2.grid(row=11, column=1)
            F3.grid(row=12, column=1)
            F4.grid(row=13, column=1)
            F1L.grid(row=10, column=0)
            F2L.grid(row=11, column=0)
            F3L.grid(row=12, column=0)
            F4L.grid(row=13, column=0)
            check_set(F1L, "data/" + question_type + "/media/" + pic1_filename)
            check_set(F2L, "data/" + question_type + "/media/" + pic2_filename)
            check_set(F3L, "data/" + question_type + "/media/" + pic3_filename)
            check_set(F4L, "data/" + question_type + "/media/" + pic4_filename)

        save_btn = Button(question_edit, text="Save", command=lambda: save_question(question_type, index, SV, IV, question_edit, ls))
        save_btn.grid(row=99, columnspan=2)

        question_edit.mainloop()


def update_time_modified(question_type, index):
    now = str(datetime.datetime.now())
    metadata[question_type][str(index)] = now[:now.find(".")]
    with open("data/metadata.json", "w", encoding="utf-8", newline="\n") as metadata_file:
        metadata_file.write(json.dumps(metadata))


def save_question(question_type, index, SV, IV, window, ls):
    check_dir_existance(question_type)
    with open("data/{}/{}.config".format(question_type, index), "w", encoding="utf-8", newline="\n") as file:
        if question_type == "mc":
            for e in SV:
                file.write(e.get() + "\n")
        elif question_type == "sq":
            for i in range(len(SV)):
                if i > 2:
                    file.write("N/A\n")
                else:
                    file.write(SV[i].get() + "\n")
        elif question_type in {"music", "tf"}:
            for i in range(len(SV)):
                if i > 1:
                    file.write("N/A\n")
                else:
                    file.write(SV[i].get() + "\n")
        elif question_type in {"pic1", "pic2"}:
            for i in range(len(SV)):
                if i > 0:
                    file.write("N/A\n")
                else:
                    file.write(SV[i].get() + "\n")

        if question_type in {"mc", "music", "tf", "pic1", "pic2"}:
            file.write(str(IV.get()) + "\n")
        elif question_type == "sq":
            file.write("-1\n")

    update_time_modified(question_type, index)
    update_question_list(question_type, ls)
    window.destroy()


def save_rule(question_type, content, window, ls):
    check_dir_existance(question_type)

    with open("data/{}/0.config".format(question_type), "w", encoding="utf-8", newline="\n") as file:
        file.write(content)

    update_time_modified(question_type, 0)
    update_question_list(question_type, ls)
    window.destroy()


def open_browser(url):
    webbrowser.open(url)


def go_to_update():
    open_browser("https://github.com/" + REPO + "/archive/master.zip")
    root.destroy()


def export_data():
    filename = filedialog.asksaveasfilename(filetypes=[("GZ Files", "*.gz")], title="导出至...")
    if filename:
        shutil.make_archive(filename, 'gztar', 'data')


def set_str_var(root, strvar, text):
    strvar.set(text)
    root.update()


def first_time_run():
    root = Tk()
    root.title("")
    text = StringVar()
    label2 = Label(root, textvariable=text)
    label2.pack()
    set_str_var(root, text, "Starting...")

    bring_to_front(root)

    try:
        if not os.path.exists("tmp"):
            os.makedirs("tmp")
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
        except Exception as e:
            print(e)
        if sys.platform == "win32":
            set_str_var(root, text, "Downloading Adobe Flash Player...")
            download("https://fpdownload.macromedia.com/pub/flashplayer/updaters/32/flashplayer_32_sa_debug.exe", "flashplayer.exe")
        else:
            set_str_var(root, text, "Downloading Adobe Flash Player...")
            if sys.platform == "darwin":
                download("https://fpdownload.macromedia.com/pub/flashplayer/updaters/32/flashplayer_32_sa_debug.dmg", "tmp/flashplayer.dmg")
                set_str_var(root, text, "Extracting Adobe Flash Player...")
                os.system("hdiutil attach -nobrowse -mountpoint ./tmp/flashplayer ./tmp/flashplayer.dmg")
                if os.path.exists("Flash Player.app"):
                    shutil.rmtree("Flash Player.app")
                os.system("cp -r ./tmp/flashplayer/Flash\\ Player.app .")
                os.system("hdiutil detach ./tmp/flashplayer")
            else:
                download("https://fpdownload.macromedia.com/pub/flashplayer/updaters/32/flash_player_sa_linux_debug.x86_64.tar.gz", "tmp/flashplayer.tar.gz")
                set_str_var(root, text, "Extracting Adobe Flash Player...")
                extract_tar_gz("tmp/flashplayer.tar.gz", "tmp/")
                os.system("cp ./tmp/flashplayer ./flashplayer")

        set_str_var(root, text, "Removing temporary folder...")
        if os.path.exists("tmp"):
            shutil.rmtree("tmp")
        root.destroy()
    except Exception as e:
        print(e)
        global error
        error = True
        set_str_var(root, text, "初始化失败.")
        root.mainloop()
    else:
        with open("__version__", "w", encoding="utf-8", newline="\n") as file:
            file.write(VERSION)


def download(url, file, length=16*1024):
    req = urllib.request.urlopen(url)
    with open(file, 'wb') as fp:
        shutil.copyfileobj(req, fp, length)


def extract_tar_gz(file, target):
    tar = tarfile.open(file, "r:gz")
    tar.extractall(target)
    tar.close()


def bring_to_front(root):
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    if sys.platform == "darwin":
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')


def run_flash():
    flash_installed = True
    if os.path.exists("__version__"):
        with open("__version__", "r") as file:
            if file.read().strip() != VERSION:
                flash_installed = False
    else:
        flash_installed = False
    if not flash_installed:
        if messagebox.askyesno("", "需要安装 Adobe Flash Player 才能继续.\n你要下载并安装 Adobe Flash Player 吗?\nAdobe Flash Player 将被安装在本程序目录下."):
            first_time_run()
            flash_installed = True

    if flash_installed:
        if sys.platform == "darwin":
            os.system("open -a Flash\ Player orientation.swf")
        elif sys.platform == "win32":
            os.system('start flashplayer.exe "orientation.swf"')
        else:
            os.system("./flashplayer orientation.swf")


def import_data():
    selected = select_file("TAR GZ Files", "*.gz")
    if selected:
        if messagebox.askyesno("", "你确定要导入数据吗?\n导入的数据会与当前数据合并.\n如果导入的数据包含当前数据中已有的题目,\n导入的题目会覆盖当前的题目."):
            try:
                extract_tar_gz(selected, './data/')
                refresh_main_window()
                messagebox.showinfo("", "导入成功.")
            except:
                refresh_main_window()
                messagebox.showerror("", "导入失败.")


if (__name__ == "__main__"):
    error = False
    needs_update = False

    try:
        file = open("wim-ori-con.py", encoding="utf-8")
        file.close()
    except:
        error = True
        root = Tk()
        root.title("")
        text = "检测到 working directory 不是本程序所在目录.\n请 cd 至本程序所在目录后重试."
        label = Label(root, text=text)
        label.pack()
        bring_to_front(root)
        root.mainloop()

    if (not error) and (not DEBUG):
        try:
            with urllib.request.urlopen("https://raw.githubusercontent.com/" + REPO + "/master/wim-ori-con.py") as latest_code_reader:
                latest_code = latest_code_reader.read().decode("utf-8").strip()
            with open("wim-ori-con.py", encoding="utf-8") as current_code_reader:
                current_code = current_code_reader.read().strip()
            if latest_code != current_code:
                needs_update = True
            urllib.request.urlopen("http://andrewwang.ca/wim-ori-con")
        except Exception as e:
            print(e)

    if (not error) and needs_update:
        error = True
        root = Tk()
        root.title("")
        text = "检测到新版本，更新后才能继续使用.\n"
        label = Label(root, text=text)
        label.pack()
        button = Button(root, text="下载", command=go_to_update)
        button.pack()
        bring_to_front(root)
        root.mainloop()

    if not error:
        if not os.path.exists("data"):
            os.makedirs("data")
        try:
            navigation_config_file = open("data/navigation.config", encoding="utf-8", newline="\n")
            navigation_config_file.close()
        except FileNotFoundError:
            with open("data/navigation.config", "w", encoding="utf-8", newline="\n") as navigation_config_file:
                navigation_config_file.write("0" * (len(QUESTION_TYPES) - 1))

        try:
            with open("data/metadata.json", encoding="utf-8", newline="\n") as metadata_file:
                metadata = json.loads(metadata_file.read())
        except FileNotFoundError:
            with open("data/metadata.json", "w", encoding="utf-8", newline="\n") as metadata_file:
                metadata = {}
                for next_question_type in QUESTION_TYPES:
                    metadata[next_question_type] = {}
                metadata_file.write(json.dumps(metadata))

        try:
            with open("data/title.config", encoding="utf-8", newline="\n") as title_file:
                pass
        except FileNotFoundError:
            with open("data/title.config", "w", encoding="utf-8", newline="\n") as title_file:
                title_file.write("选择题\n简答题\n是非题\n图片题\n音乐题\n冲刺题\n")

        root = Tk()
        root.title("")

        B = []
        C = []
        var = []
        for i in range(len(QUESTION_TYPES) - 1):
            intvar = IntVar()
            intvar.trace("w", save_navigation_config)
            var.append(intvar)

        BGL = Label(root)
        BGL.grid(row=0, column=0)
        BGB = Button(root, text="背景图片 (jpg, 1280 x 800)", command=select_bg)
        BGB.grid(row=0, column=1)
        check_set(BGL, "data/bg.jpg")

        BTitle = Button(root, text="编辑板块标题", command=show_edit_title_window)
        BTitle.grid(row=1, column=1)

        B.append(Button(root, text="选择题", command=lambda: show_question_list_window("mc")))
        B[0].grid(row=2, column=1)
        C.append(Checkbutton(root, text="启用", variable=var[0]))
        C[0].grid(row=2, column=0)

        B.append(Button(root, text="简答题", command=lambda: show_question_list_window("sq")))
        B[1].grid(row=3, column=1)
        C.append(Checkbutton(root, text="启用", variable=var[1]))
        C[1].grid(row=3, column=0)

        B.append(Button(root, text="是非题", command=lambda: show_question_list_window("tf")))
        B[2].grid(row=4, column=1)
        C.append(Checkbutton(root, text="启用", variable=var[2]))
        C[2].grid(row=4, column=0)

        Bpic1 = Button(root, text="图片题 (遮挡/其他)", command=lambda: show_question_list_window("pic1"))
        Bpic1.grid(row=5, column=1)
        C.append(Checkbutton(root, text="启用", variable=var[3]))
        C[3].grid(row=5, column=0, rowspan=2)

        Bpic2 = Button(root, text="图片题 (马赛克)", command=lambda: show_question_list_window("pic2"))
        Bpic2.grid(row=6, column=1)
        B.append((Bpic1, Bpic2))

        B.append(Button(root, text="音乐题", command=lambda: show_question_list_window("music")))
        B[4].grid(row=7, column=1)
        C.append(Checkbutton(root, text="启用", variable=var[4]))
        C[4].grid(row=7, column=0)

        B.append(Button(root, text="冲刺题", command=lambda: show_question_list_window("fc")))
        B[5].grid(row=8, column=1)
        C.append(Checkbutton(root, text="启用", variable=var[5]))
        C[5].grid(row=8, column=0)

        space1 = Label(root, text="")
        space1.grid(row=9, columnspan=2)

        BExport = Button(root, text="导入/合并数据", command=import_data)
        BExport.grid(row=10, columnspan=2)
        BExport = Button(root, text="导出数据", command=export_data)
        BExport.grid(row=11, columnspan=2)

        BRun = Button(root, text="测试运行", command=run_flash)
        BRun.grid(row=12, columnspan=2)

        enable = load_navigation_config()
        for i in range(len(enable)):
            if enable[i]:
                C[i].select()
        save_navigation_config(None, None, None)

        bring_to_front(root)

        root.mainloop()
