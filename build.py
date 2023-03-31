import tkinter as tk

import pandas

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


button1 = tk.Button(text="Click Me", command=hello, bg="brown", fg="white")
canvas1.create_window(150, 150, window=button1)


root.mainloop()
