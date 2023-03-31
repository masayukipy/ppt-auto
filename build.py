import os
import threading
import tkinter as tk

import pandas

import app

root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300)
canvas1.pack()


def hello():

    label1 = tk.Label(
        root, text="utils.Utils.a", fg="blue", font=("helvetica", 12, "bold")
    )
    df = pandas.DataFrame([1, 2, 3, 4])
    df.to_csv("out.csv")
    canvas1.create_window(150, 200, window=label1)


def run_all():
    # os.popen("'.venv/Scripts/python.exe' 'app.py'")
    all_thread = threading.Thread(target=app.all)
    hello_thread = threading.Thread(target=hello)
    hello_thread.start()
    all_thread.start()
    hello_thread.join()
    all_thread.join()
    return


button1 = tk.Button(text="Run All", command=run_all, bg="brown", fg="white")
canvas1.create_window(150, 150, window=button1)

entry1 = tk.Entry(root)
canvas1.create_window(200, 140, window=entry1)


root.mainloop()
