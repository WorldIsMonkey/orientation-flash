import os
from tkinter.filedialog import askopenfilename


def ask_file_name():
    return askopenfilename()


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
