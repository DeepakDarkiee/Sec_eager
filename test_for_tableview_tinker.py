# pyinstaller --noconsole --onefile keylogger.py # Convert py to exe
import tkinter
from tkinter import *
from tkinter import ttk
# import only asksaveasfile from filedialog # used to save file in any extension
from tkinter.filedialog import asksaveasfile
import requests
from bs4 import BeautifulSoup
import urllib 
import time
import pandas as pd
import sqlite3
import datetime
db = sqlite3.connect('sec_db.db')
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS sec_data(nameOfIssuer TEXT,entry_date DATE , titleOfClass TEXT, symbol TEXT, value TEXT, sshPrnamt TEXT, sshPrnamtType TEXT, investmentDiscretion TEXT, otherManager TEXT, VA_Sole TEXT, VA_Shared TEXT, VA_None TEXT)")
db.commit()
data_to_csv = []
connt = sqlite3.connect('sec_db.db')
cursor = connt.cursor()
company_name = ""
global f4

def show():
    # print("Function Called")
    clear()
    global f4
    cursor = connt.cursor()
    company_name = ""
    company_name = c_name.get()
    c_name.set(company_name)
    if company_name == "":
        if from_date == "" and (t_date.get() == "" or t_date.get() == "YYYY-MM-DD"):
            query = "SELECT DISTINCT * FROM sec_data ORDER BY entry_date DESC"
        elif from_date == t_date:
            query = "SELECT DISTINCT * FROM sec_data WHERE entry_date ='" + from_date + "' ORDER BY entry_date DESC"
        elif from_date != to_date:
            query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + str(company_name) + "%' AND entry_date BETWEEN '" + str(from_date.get()) + "' AND '" + str(t_date.get()) + "' ORDER BY entry_date DESC"
    else:
        if from_date == "" and (t_date.get() == "" or t_date.get() == "YYYY-MM-DD"):
            query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + company_name + "%' ORDER BY entry_date DESC"
        elif from_date == t_date:
            query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + company_name + "%' and entry_date ='" + from_date + "' ORDER BY entry_date DESC"
        elif from_date != to_date:
            query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + str(company_name) + "%' AND entry_date BETWEEN '" + str(from_date.get()) + "' AND '" + str(t_date.get()) + "' ORDER BY entry_date DESC"
    # print(query)
    cursor.execute(query)

    f4 = Frame(fd, bg="white", borderwidth=0)
    f4.pack(fill="x")
    i = 0
    for r in cursor.fetchall():
        # print(r)
        if i > 8:
            break
        i = i + 1
        c1 = Label(f4, text=str(r[0]), bg="white", anchor=W, width=22, wraplength=150)
        c1.grid(row=i, column=0)
        c2 = Label(f4, text=r[2], bg="white", anchor=W, width=15)
        c2.grid(row=i, column=1)
        c3 = Label(f4, text=r[3], bg="white", anchor=W, width=10)
        c3.grid(row=i, column=2)
        c4 = Label(f4, text=r[4], bg="white", anchor=W, width=6)
        c4.grid(row=i, column=3)
        c5 = Label(f4, text=r[5], bg="white", anchor=W, width=10)
        c5.grid(row=i, column=4)
        c6 = Label(f4, text=r[6], bg="white", anchor=W, width=9)
        c6.grid(row=i, column=5)
        c7 = Label(f4, text=r[7], bg="white", anchor=W, width=9)
        c7.grid(row=i, column=6)
        c8 = Label(f4, text=r[8], bg="white", anchor=W, width=10)
        c8.grid(row=i, column=7)
        c9 = Label(f4, text=r[9], bg="white", anchor=W, width=7)
        c9.grid(row=i, column=8)
        c10 = Label(f4, text=r[10], bg="white", anchor=W, width=8)
        c10.grid(row=i, column=9)
        c11 = Label(f4, text=r[11], bg="white", anchor=W, width=7)
        c11.grid(row=i, column=10)
        c12 = Label(f4, text=r[1], bg="white", anchor=W, width=13)
        c12.grid(row=i, column=11)



def download():
    try:
        cursor = connt.cursor()
        company_name = ""
        company_name = c_name.get()
        c_name.set(company_name)
        if company_name == "":
            if from_date == "" and (t_date.get() == "" or t_date.get() == "YYYY-MM-DD"):
                query = "SELECT DISTINCT * FROM sec_data ORDER BY entry_date DESC"
            elif from_date == t_date:
                query = "SELECT DISTINCT * FROM sec_data WHERE entry_date ='" + from_date + "'"
            elif from_date != to_date:
                query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + str(
                    company_name) + "%' AND entry_date BETWEEN '" + str(from_date.get()) + "' AND '" + str(
                    t_date.get()) + "' "
        else:
            if from_date == "" and (t_date.get() == "" or t_date.get() == "YYYY-MM-DD"):
                query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + company_name + "%'"
            elif from_date == t_date:
                query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + company_name + "%' and entry_date ='" + from_date + "'"
            elif from_date != to_date:
                query = "SELECT DISTINCT * FROM sec_data WHERE symbol LIKE '%" + str(
                    company_name) + "%' AND entry_date BETWEEN '" + str(from_date.get()) + "' AND '" + str(
                    t_date.get()) + "' "

        # print(query)
        cursor.execute(query)

        data_to_csv = []
        for r in cursor.fetchall():
            data_to_csv.append(r)
        columns = ['nameOfIssuer', 'entry_date', 'titleOfClass', 'symbol', 'value', 'sshPrnamt', 'sshPrnamtType',
                   'investmentDiscretion', 'otherManager', 'VA_Sole', 'VA_Shared', 'VA_None']

        df = pd.DataFrame(data_to_csv, columns=columns)

        files = [('Comma Seperated Values', 'download.csv'),
                 ('Text Document', 'download.txt'),
                 ('All Files', '*.*')]

        file = asksaveasfile(filetypes=files, defaultextension=".csv")
        df.to_csv(file)
    except Exception as e:
        print("Error" + str(e))


# Function to set focus (cursor)
# def focus1(event):
#     form_field.focus_set()


def focus2(event, option=None):
    option.focus_set()


# Function for clearing the contents of text entry boxes
def clear():
    # name_field.delete(0, END)
    try:
        for widget in f4.winfo_children():
            widget.destroy()
        f4.pack_forget()
    except Exception as e:
        print("Error")


if __name__ == "__main__":
    root = Tk()
    # set the background colour of GUI window
    # root.configure(background='light green')
    # set the title of GUI window
    root.title("SEC-Edger")
    # set the configuration of GUI window
    root.geometry("1040x610")
    # In order to prevent the window from getting resized you will call 'resizable' method on the window
    root.resizable(0, 0)

    c_name = StringVar()
    f_type = StringVar()
    f_date = StringVar()
    t_date = StringVar()
    time_field = StringVar()
    time_duration = StringVar()

    f1 = Frame(root, borderwidth=6)
    f1.pack(side=TOP, fill="x", padx="150")

    heading = Label(f1, text="Form")
    heading.grid(row=0, column=1)

    company_name = Label(f1, text="Symbol", anchor=W, width=15)
    company_name.grid(row=1, column=0)

    # time = Label(f1, text="Time Duration",anchor=W, width=15)
    # time.grid(row=3, column=0)

    name_field = Entry(f1, textvariable=c_name, width=8)
    name_field.grid(row=1, column=1, ipadx="100")
    # name_field.bind("<Return>", focus1)

    f_filter = Frame(borderwidth=1)
    f_filter.pack(fill="x", padx="150")

    from_label = Label(f_filter, text="From-", width=4, wraplength=50)
    from_label.grid(row=1, column=1)
    from_date = Entry(f_filter, textvariable=f_date, width=1)
    f_date.set("2020-04-03")
    from_date.grid(row=1, column=2, ipadx="100")
    time = Label(f_filter, text="To-", anchor=W, width=3, wraplength=20)
    time.grid(row=1, column=3)
    to_date = Entry(f_filter, textvariable=t_date, width=1)
    t_date.set("YYYY-MM-DD")
    to_date.grid(row=1, column=4, ipadx="100")

    time = Label(f_filter, text="")
    time.grid(row=2, column=0)
    submit = Button(f_filter, text="Submit", width=10, fg="white", bg="Black", command=show)
    submit.grid(row=3, column=3, ipady="1")

    # Frame to Display Data
    f2 = Frame(root, bg="white", borderwidth=6)
    f2.pack(fill="x")
    f3 = Frame(f2, borderwidth=10)
    f3.pack(fill="x")
    c1 = Label(f3, text="Name_Of_Issuer", anchor=W, width=22, wraplength=150)
    c1.grid(row=0, column=0)
    c2 = Label(f3, text="Title_Of_Class", anchor=W, width=15)
    c2.grid(row=0, column=1)
    c3 = Label(f3, text="Symbol", anchor=W, width=10)
    c3.grid(row=0, column=2)
    c4 = Label(f3, text="value", anchor=W, width=6)
    c4.grid(row=0, column=3)
    c5 = Label(f3, text="ssh_Prnamt", anchor=W, width=10)
    c5.grid(row=0, column=4)
    c6 = Label(f3, text="ssh_Prnamt_Type", anchor=W, width=9, wraplength=62)
    c6.grid(row=0, column=5)
    c7 = Label(f3, text="investment_Discretion", anchor=W, width=9, wraplength=60)
    c7.grid(row=0, column=6)
    c8 = Label(f3, text="Other Manager", anchor=W, width=10, wraplength=65)
    c8.grid(row=0, column=7)
    c9 = Label(f3, text="VA_Sole", anchor=W, width=7)
    c9.grid(row=0, column=8)
    c10 = Label(f3, text="VA_Shared", anchor=W, width=8)
    c10.grid(row=0, column=9)
    c11 = Label(f3, text="VA_None", anchor=W, width=7)
    c11.grid(row=0, column=10)
    c12 = Label(f3, text="Date of Record", anchor=W, width=12)
    c12.grid(row=0, column=11)

    fd = Frame(f2, bg="white", borderwidth=6)
    fd.pack(fill="x")

    f5 = Frame(f2, bg="white", borderwidth=6)
    f5.pack(fill="x")
    submit = Button(f5, text="Download Data", fg="white", bg="Black", command=download)
    submit.grid(row=4, column=2, padx="860", pady="5")

    root.mainloop()
