__author__ = 'Chengze Li'
__version__ = '0.0.1'

# This library is only suitable for python3

import sys, time
from qrcode import *
from tkinter import *
from tkinter.messagebox import *

'''
1.Module xes can only be used in the Xueersi 
  programming community(code.xueersi.com) and 
  cannot be used in compilers such as IDLE.
2.All functions except module xes 
  can be used in compilers such as IDLE.
'''


class xes(object):
    def clean():
        sys.stdout.write("\033[2J\033[00H")

    def output(z):
        z = str(z)
        q = 0
        for i in z:
            q += 1
            time.sleep(0.025)
            print(i, end="")
        print()


class file(object):
    def txt_create(name, msg, path):
        if path is None:
            path = "C:\\Users\\Administrator\\Desktop\\"
        full_path = path + name + '.txt'
        file = open(full_path, 'w')
        file.write(msg)

    def doc_create(name, msg, path):
        # This function is recommended
        # to run under windows system
        if path is None:
            path = "C:\\Users\\Administrator\\Desktop\\"
        full_path = path + name + '.doc'
        file = open(full_path, 'w')
        file.write(msg)


# This function only supports mutual
# conversion between English and Chinese
def translate(content):
    url = "http://fanyi.youdao.com/translate?doctype=json&type=AUTO&i=" + content
    r = requests.get(url)
    result = r.json()
    return result["translateResult"][0][0]["tgt"]


# This function may be wrong
def qrcode(qrcode):
    qrcode = repr(qrcode)
    qr = QRCode()
    qr.add_data(qrcode)
    img = qr.make_image()
    img.show()


# This function is adapted from csdn
def calculator():
    root = Tk()
    root.geometry('300x200')
    root.title('oython calculator')
    num = StringVar()
    Entry(root, textvariable=num, bg="yellow").place(relx=0, rely=0, relwidth=1, relheight=0.2)

    def result():
        num.set(eval(num.get()))

    Button(root, text="1", command=lambda: num.set(num.get() + "1")).place(relx=0, rely=0.2, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="2", command=lambda: num.set(num.get() + "2")).place(relx=0.25, rely=0.2, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="3", command=lambda: num.set(num.get() + "3")).place(relx=0.5, rely=0.2, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="+", command=lambda: num.set(num.get() + "+")).place(relx=0.75, rely=0.2, relwidth=0.25,
                                                                           relheight=0.2)

    Button(root, text="4", command=lambda: num.set(num.get() + "4")).place(relx=0, rely=0.4, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="5", command=lambda: num.set(num.get() + "5")).place(relx=0.25, rely=0.4, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="6", command=lambda: num.set(num.get() + "6")).place(relx=0.5, rely=0.4, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="-", command=lambda: num.set(num.get() + "-")).place(relx=0.75, rely=0.4, relwidth=0.25,
                                                                           relheight=0.2)

    Button(root, text="7", command=lambda: num.set(num.get() + "7")).place(relx=0, rely=0.6, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="8", command=lambda: num.set(num.get() + "8")).place(relx=0.25, rely=0.6, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="9", command=lambda: num.set(num.get() + "9")).place(relx=0.5, rely=0.6, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="×", command=lambda: num.set(num.get() + "*")).place(relx=0.75, rely=0.6, relwidth=0.25,
                                                                           relheight=0.2)

    Button(root, text="0", command=lambda: num.set(num.get() + "0")).place(relx=0, rely=0.8, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text=".", command=lambda: num.set(num.get() + ".")).place(relx=0.25, rely=0.8, relwidth=0.25,
                                                                           relheight=0.2)
    Button(root, text="=", command=result).place(relx=0.5, rely=0.8, relwidth=0.25, relheight=0.2)
    Button(root, text="÷", command=lambda: num.set(num.get() + "/")).place(relx=0.75, rely=0.8, relwidth=0.25,
                                                                           relheight=0.2)
    root.mainloop()
