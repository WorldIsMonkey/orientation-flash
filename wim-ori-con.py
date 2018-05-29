#!/usr/bin/env python3


"""
Copyright Andrew Wang, 201
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
import hashlib
import imghdr
import os
import shutil
import ssl
import struct
import tarfile
import urllib.request
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


DEBUG = False  # Setting this flag to True will disable checking for update
GREEN = "#C8E6C9"
YELLOW = "#FFF9C4"
RED = "#FFCDD2"
# Incrementing this variable will force a call to first_time_run.
# Do this when dependency update is required.
DEPENDENCY_VERSION = "20180530"


def sha1(fname):
    hash_sha1 = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


def load_main_config():
    result = []
    for i in range(8):
        result.append(False)
    try:
        file = open("data/main.config")
        count = 0
        for e in file:
            for ee in e:
                if ee == "1":
                    result[count] = True
                count += 1
        file.close()
        return result
    except FileNotFoundError:
        return result


def save_main_config(var):
    if not os.path.exists("data"):
        os.makedirs("data")
    file = open("data/main.config", "w")
    for e in var:
        file.write(str(IntVar.get(e)))
    file.close()
    messagebox.showinfo("", "主设置已保存.")


def initialize():
    if messagebox.askyesno("", "你确定要初始化数据吗?"):
        if messagebox.askyesno("", "你真的要初始化数据吗?\n这将清除所有已输入的数据!"):
            if os.path.exists("data"):
                try:
                    shutil.rmtree("data")
                    messagebox.showinfo("", "数据初始化成功!")
                except:
                    messagebox.showerror("", "数据初始化失败.")
            else:
                messagebox.showinfo("", "数据初始化成功!")


def submit(root):
    def upload(top, button, host, username, password):
        if messagebox.askyesno("", "你确定要将数据上传至服务器吗?"):
            button["state"] = DISABLED
            button["text"] = "正在连接..."
            top.update()

            try:
                import pexpect
                var_password = password
                var_command = ("scp -r ./data " + username + "@" + host + ":~")
                var_child = pexpect.spawn(var_command)
                i = var_child.expect(["password:", "yes/no", "denied", pexpect.EOF])

                button["text"] = "正在上传..."
                top.update()
                if i == 0:  # send password
                    var_child.sendline(var_password)
                    var_child.expect(pexpect.EOF)
                elif i == 1:
                    var_child.sendline("yes")
                    j = var_child.expect(["password:", pexpect.EOF])
                    if j == 0:
                        var_child.sendline(var_password)
                        var_child.expect(pexpect.EOF)
                elif i == 2:
                    raise Exception("用户名或密码错误.")
                else:
                    raise Exception("提交失败.")
                messagebox.showinfo("", "提交成功!")
            except Exception as e:
                messagebox.showerror("", str(e))
            finally:
                top.destroy()

    top = Toplevel()
    top.title = "使用SCP上传"
    host_label = Label(top, text="Host: ")
    host_label.grid(row=0, column=0)
    username_label = Label(top, text="Username: ")
    username_label.grid(row=1, column=0)
    password_label = Label(top, text="Password: ")
    password_label.grid(row=2, column=0)
    host = Entry(top)
    host.insert(0, "fissure.utsc.utoronto.ca")
    host.grid(row=0, column=1)
    username = Entry(top)
    username.grid(row=1, column=1)
    password = Entry(top)
    password.grid(row=2, column=1)
    button = Button(top,text="提交", command=lambda: upload(top, button, host.get(), username.get(), password.get()))
    button.grid(row=3, columnspan=2)
    top.mainloop()


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
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/" + question_type):
        os.makedirs("data/" + question_type)
    if not os.path.exists("data/" + question_type + "/media"):
        os.makedirs("data/" + question_type + "/media")


def add_media(elem, question_type, filename, description, file_type, width=None, height=None):
    selected = select_file(description, file_type)
    if selected:
        if (not width and not height) or check_image_size(selected, width, height):
            check_dir_existance(question_type)
            target = "data/" + question_type + "/media/" + filename
            shutil.copy(selected, target)
            check_set(elem, target)
            messagebox.showinfo("", "设定成功!")
        else:
            messagebox.showerror("", "图片分辨率必须为{0} x {1}.".format(width, height))

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
            messagebox.showerror("", "图片分辨率必须为1280 x 800.")
        check_set(BGL, "data/bg.jpg")


def check_set(element, file):
    if os.path.exists(file):
        element.config(text="已设定")
        element.config(fg="#4CAF50")
    else:
        element.config(text="未设定")
        element.config(fg="red")


def show_question_list_window(question_type):
    if question_type == "mc":
        num_questions = 40
        title = "选择题"
    elif question_type == "sq":
        num_questions = 20
        title = "简答题"
    elif question_type == "music":
        num_questions = 30
        title = "音乐题"
    elif question_type == "tf":
        num_questions = 15
        title = "判断题"
    elif question_type == "pic1":
        num_questions = 10
        title = "图片题 (遮挡)"
    elif question_type == "pic2":
        num_questions = 10
        title = "图片题 (马赛克)"
    elif question_type == "fc":
        num_questions = 0
        title = "冲刺题"
    mc = Tk()
    mc.title(title)
    ls = Listbox(mc, height=num_questions + 1)
    ls.insert(0, "规则文本")
    for i in range(1, num_questions + 1):
        ls.insert(i, str(i))

    check_question_completion(question_type, ls)

    edit_btn_top = Button(mc, text="Edit", command=lambda: edit_question(question_type, ls))
    edit_btn_top.pack()

    ls.pack()

    edit_btn_bottom = Button(mc, text="Edit", command=lambda: edit_question(question_type, ls))
    edit_btn_bottom.pack()

    ls.mainloop()


def edit_question(question_type, ls):
    if not ls.curselection():
        return
    index = ls.curselection()[0]
    if index == 0:
        content = ""
        if os.path.exists("data/" + question_type + "/" + str(index) + ".config"):
            file = open("data/" + question_type + "/" + str(index) + ".config", encoding="utf8")
            content = file.read()
            file.close()

        rule_edit = Tk()
        rule_edit.title("编辑[规则文本]")

        box = Text(rule_edit)
        box.pack()
        box.insert(INSERT, content)

        save_btn = Button(rule_edit, text="Save", command=lambda: save_rule(question_type, box.get("1.0", END), rule_edit, ls))
        save_btn.pack()

        rule_edit.mainloop()
    else:
        content = None
        if os.path.exists("data/" + question_type + "/" + str(index) + ".config"):
            file = open("data/" + question_type + "/" + str(index) + ".config", encoding="utf8")
            content = file.readlines()
            file.close()

        question_edit = Tk()
        question_edit.title("编辑[第" + str(index) + "题]")

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
            L0 = Label(question_edit, text="问题第 1 行")
            L0.grid(row=0, column=0)
            E0 = Entry(question_edit, textvariable=SV[0])
            E0.grid(row=0, column=1)

            L1 = Label(question_edit, text="问题第 2 行")
            L1.grid(row=1, column=0)
            E1 = Entry(question_edit, textvariable=SV[1])
            E1.grid(row=1, column=1)
        elif question_type == "music":
            L0 = Label(question_edit, text="番名")
            L0.grid(row=0, column=0)
            E0 = Entry(question_edit, textvariable=SV[0])
            E0.grid(row=0, column=1)

            L1 = Label(question_edit, text="歌名")
            L1.grid(row=1, column=0)
            E1 = Entry(question_edit, textvariable=SV[1])
            E1.grid(row=1, column=1)
        elif question_type in {"pic1", "pic2"}:
            L0 = Label(question_edit, text="答案")
            L0.grid(row=0, column=0)
            E0 = Entry(question_edit, textvariable=SV[0])
            E0.grid(row=0, column=1)

        if question_type == "sq":
            L2 = Label(question_edit, text="答案")
            L2.grid(row=2, column=0)
            E2 = Entry(question_edit, textvariable=SV[2])
            E2.grid(row=2, column=1)

        if question_type == "mc":
            L2 = Label(question_edit, text="A 选项")
            L2.grid(row=2, column=0)
            E2 = Entry(question_edit, textvariable=SV[2])
            E2.grid(row=2, column=1)

            L3 = Label(question_edit, text="B 选项")
            L3.grid(row=3, column=0)
            E3 = Entry(question_edit, textvariable=SV[3])
            E3.grid(row=3, column=1)

            L4 = Label(question_edit, text="C 选项")
            L4.grid(row=4, column=0)
            E4 = Entry(question_edit, textvariable=SV[4])
            E4.grid(row=4, column=1)

            L5 = Label(question_edit, text="D 选项")
            L5.grid(row=5, column=0)
            E5 = Entry(question_edit, textvariable=SV[5])
            E5.grid(row=5, column=1)

            L5 = Label(question_edit, text="答案")
            L5.grid(row=6, column=0)
            R1 = Radiobutton(question_edit, text="A", variable=IV, value=1)
            R2 = Radiobutton(question_edit, text="B", variable=IV, value=2)
            R3 = Radiobutton(question_edit, text="C", variable=IV, value=3)
            R4 = Radiobutton(question_edit, text="D", variable=IV, value=4)
            R1.grid(row=6, column=1)
            R2.grid(row=7, column=1)
            R3.grid(row=8, column=1)
            R4.grid(row=9, column=1)
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
            L5.grid(row=6, column=0)
            R1 = Radiobutton(question_edit, text="True", variable=IV, value=1)
            R2 = Radiobutton(question_edit, text="False", variable=IV, value=2)
            R1.grid(row=6, column=1)
            R2.grid(row=7, column=1)

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

            tip = Label(question_edit, text="\nTip:\n为了更好的观众体验，\n可在音频文件前后添加淡入和淡出，\n并对所有音频文件进行音量平衡.\n")
            tip.grid(row=14, columnspan=2)
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

            tip = Label(question_edit, text="\nTip:\n若图片不符合尺寸，\n请将图片进行缩放、剪裁，\n或在图片四周添加透明像素.\n")
            tip.grid(row=14, columnspan=2)
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

            tip = Label(question_edit, text="\nTip:\n若图片不符合尺寸，\n请将图片进行缩放、剪裁，\n或在图片四周添加透明像素.\n")
            tip.grid(row=14, columnspan=2)


        save_btn = Button(question_edit, text="保存", command=lambda: save_question(question_type, index, SV, IV, question_edit, ls))
        save_btn.grid(row=99, columnspan=2)

        question_edit.mainloop()


def save_question(question_type, index, SV, IV, window, ls):
    check_dir_existance(question_type)
    file = open("data/" + question_type + "/" + str(index) + ".config", "w", encoding="utf8", newline='\n')
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

    if question_type in {"mc", "music", "tf"}:
        file.write(str(IV.get()) + "\n")
    elif question_type == "sq":
        file.write("-1\n")
    file.close()
    window.destroy()
    check_question_completion(question_type, ls)


def save_rule(question_type, content, window, ls):
    check_dir_existance(question_type)
    file = open("data/" + question_type + "/0.config", "w", encoding="utf8")
    file.write(content);
    file.close()
    window.destroy()
    check_question_completion(question_type, ls)


def check_question_completion(question_type, ls):
    if question_type == "mc":
        num_questions = 40
    elif question_type == "sq":
        num_questions = 20
    elif question_type == "music":
        num_questions = 30
    elif question_type == "tf":
        num_questions = 15
    elif question_type in {"pic1", "pic2"}:
        num_questions = 10
    elif question_type == "fc":
        num_questions = 0
    greenlist = []
    for i in range(0, num_questions + 1):
        if i == 0:
            try:
                file = open("data/" + question_type + "/0.config", encoding="utf8")
                if file.read().strip():
                    ls.itemconfig(i, bg=GREEN)
                else:
                    ls.itemconfig(i, bg=RED)
                file.close()
            except:
                ls.itemconfig(i, bg=RED)
        else:
            if os.path.exists("data/" + question_type + "/" + str(i) + ".config"):
                ls.itemconfig(i, bg=GREEN)
                greenlist.append(i)
            else:
                ls.itemconfig(i, bg=RED)
    for e in greenlist:
        file = open("data/" + question_type + "/" + str(e) + ".config", encoding="utf8")
        empty = True
        count = 0
        for l in file:
            if not l.strip():
                if question_type == "music":
                    ls.itemconfig(e, bg=YELLOW)
                else:
                    if count != 1:  # 问题第二行可以为空
                        ls.itemconfig(e, bg=YELLOW)
            elif count == 6 and l.strip() == "0":
                ls.itemconfig(e, bg=YELLOW)
            else:
                empty = False
            count += 1
        if empty:
            ls.itemconfig(e, bg=RED)
        file.close()


def download_update(url):
    webbrowser.open(url)
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
    #label1 = Label(root, text="正在为首次运行做准备...")
    #label1.pack()
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
            download("https://fpdownload.macromedia.com/pub/flashplayer/updaters/29/flashplayer_29_sa.exe", "flashplayer.exe")
        else:
            #set_str_var(root, text, "Downloading ptyprocess...")
            #download("https://github.com/pexpect/ptyprocess/archive/0.5.1.tar.gz", "tmp/ptyprocess.tar.gz")
            #set_str_var(root, text, "Extracting ptyprocess...")
            #extract_tar_gz("tmp/ptyprocess.tar.gz", "tmp/")
            #os.system("cp -r ./tmp/ptyprocess-0.5.1/ptyprocess .")

            #set_str_var(root, text, "Downloading pexpect...")
            #download("https://github.com/pexpect/pexpect/archive/4.2.1.tar.gz", "tmp/pexpect.tar.gz")
            #set_str_var(root, text, "Extracting pexpect...")
            #extract_tar_gz("tmp/pexpect.tar.gz", "tmp/")
            #os.system("cp -r ./tmp/pexpect-4.2.1/pexpect .")

            set_str_var(root, text, "Downloading Adobe Flash Player...")
            if sys.platform == "darwin":
                download("https://fpdownload.macromedia.com/pub/flashplayer/updaters/29/flashplayer_29_sa.dmg", "tmp/flashplayer.dmg")
                set_str_var(root, text, "Extracting Adobe Flash Player...")
                os.system("hdiutil attach -nobrowse -mountpoint ./tmp/flashplayer ./tmp/flashplayer.dmg")
                os.system("cp -r ./tmp/flashplayer/Flash\\ Player.app .")
                os.system("hdiutil detach ./tmp/flashplayer")
            else:
                download("https://fpdownload.macromedia.com/pub/flashplayer/updaters/29/flash_player_sa_linux.x86_64.tar.gz", "tmp/flashplayer.tar.gz")
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
        with open("__version__", "w") as file:
            file.write(DEPENDENCY_VERSION)


def untar():
    tar = tarfile.open("path_to/test/sample.tar.bz2", "r:bz2")
    tar.extractall()
    tar.close()


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
            if file.read().strip() != DEPENDENCY_VERSION:
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
        if messagebox.askyesno("", "你确定要导入数据吗?\n如果要导入的数据会覆盖当前数据中的相同题目."):
            try:
                extract_tar_gz(selected, './data/')
                messagebox.showinfo("", "导入成功.")
            except:
                messagenbox.showerror("", "导入失败.")


if (__name__ == "__main__"):
    error = False
    needs_update = False

    try:
        file = open("wim-ori-con.py")
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
            with urllib.request.urlopen("https://raw.githubusercontent.com/A-Kun/wim-ori-con/master/wim-ori-con.py") as latest_code_reader:
                latest_code = latest_code_reader.read().decode("utf-8").strip()
            with open("wim-ori-con.py", encoding="utf8") as current_code_reader:
                current_code = current_code_reader.read().strip()
            if latest_code != current_code:
                needs_update = True
        except Exception as e:
            print(e)

    if (not error) and needs_update:
        error = True
        root = Tk()
        root.title("")
        text = "检测到新版本，更新后才能继续使用.\n"
        label = Label(root, text=text)
        label.pack()
        button = Button(root, text="下载", command=lambda: download_update("https://github.com/A-Kun/wim-ori-con/archive/master.zip"))
        button.pack()
        bring_to_front(root)
        root.mainloop()

    if not error:
        root = Tk()
        root.title("")

        B = []
        C = []
        var = []
        for i in range(8):
            B.append(None)
            C.append(None)
            var.append(IntVar())

        BGL = Label(root)
        BGL.grid(row=0, column=0)
        BGB = Button(root, text="背景图片 (jpg, 1280 x 800)", command=select_bg)
        BGB.grid(row=0, column=1)

        check_set(BGL, "data/bg.jpg")

        B[0] = Button(root, text="选择题", command=lambda: show_question_list_window("mc"))
        B[0].grid(row=1, columnspan=2)
        #C[0] = Checkbutton(root, text="启用", variable=var[0])
        #C[0].grid(row=1, column=1)

        B[1] = Button(root, text="简答题", command=lambda: show_question_list_window("sq"))
        B[1].grid(row=2, columnspan=2)
        #C[1] = Checkbutton(root, text="启用", variable=var[1])
        #C[1].grid(row=2, column=0)

        B[2] = Button(root, text="是非题", command=lambda: show_question_list_window("tf"))
        B[2].grid(row=3, columnspan=2)
        #C[2] = Checkbutton(root, text="启用", variable=var[2])
        #C[2].grid(row=3, column=0)

        B[3] = Button(root, text="图片题 (遮挡)", command=lambda: show_question_list_window("pic1"))
        B[3].grid(row=4, columnspan=2)
        #C[3] = Checkbutton(root, text="启用", variable=var[3])
        #C[3].grid(row=4, column=0)

        B[4] = Button(root, text="图片题 (马赛克)", command=lambda: show_question_list_window("pic2"))
        B[4].grid(row=5, columnspan=2)
        #C[3] = Checkbutton(root, text="启用", variable=var[3])
        #C[3].grid(row=4, column=0)

        #B[4] = Button(root, text="其他题", state=DISABLED)
        #B[4].grid(row=5, column=1)
        #C[4] = Checkbutton(root, text="启用", variable=var[4])
        #C[4].grid(row=5, column=0)

        B[5] = Button(root, text="音乐题", command=lambda: show_question_list_window("music"))
        B[5].grid(row=6, columnspan=2)
        #C[5] = Checkbutton(root, text="启用", variable=var[5])
        #C[5].grid(row=6, column=0)

        B[6] = Button(root, text="冲刺题", command=lambda: show_question_list_window("fc"))
        B[6].grid(row=7, columnspan=2)
        #C[6] = Checkbutton(root, text="启用", variable=var[6])
        #C[6].grid(row=7, column=0)

        space = Label(root, text="")
        space.grid(row=8, columnspan=2)

        #B[7] = Button(root, text="冲刺题B", state=DISABLED)
        #B[7].grid(row=8, column=1)
        #C[7] = Checkbutton(root, text="启用", variable=var[7])
        #C[7].grid(row=8, column=0)

        #BSave = Button(root, text="保存", command=lambda: save_main_config(var))
        #BSave.grid(row=9, columnspan=2)
        BExport = Button(root, text="导入数据", command=import_data)
        BExport.grid(row=10, columnspan=2)
        BExport = Button(root, text="导出数据", command=export_data)
        BExport.grid(row=11, columnspan=2)

        #if sys.platform == "win32":
            #BSubmit = Button(root, text="提交", state=DISABLED)
            #BRun = Button(root, text="测试运行", command=lambda: os.system('start flashplayer.exe "orientation.swf"'))
        #else:
            #BSubmit = Button(root, text="提交", command=lambda: submit(root))
            #BRun = Button(root, text="测试运行", command=run_flash)

        #BSubmit.grid(row=10, column=1)

        BRun = Button(root, text="测试运行", command=run_flash)
        BRun.grid(row=12, columnspan=2)

        BInit = Button(root, text="!数据初始化!", command=initialize)
        BInit.grid(row=13, columnspan=2)

        #enable = load_main_config()
        #for i in range(len(enable)):
            #if enable[i]:
                #C[i].select()

        bring_to_front(root)
        root.mainloop()
