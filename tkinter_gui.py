#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 技术支持：https://www.jianshu.com/u/69f40328d4f0 
# 技术支持 https://china-testing.github.io/
# https://github.com/china-testing/python-api-tesing/blob/master/practices/tk2.py

# CreateDate: 2018-11-27
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu

# Create instance
win = tk.Tk()   

# Add a title       
win.title("知乎话题分析器 by butyuhao")  

tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='Step1')      # Add the tab
tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='Step2')      # Make second tab visible

tabControl.pack(expand=2, fill="both")  # Pack to make visible

# LabelFrame using tab1 as the parent
mighty = ttk.LabelFrame(tab1, text='键入待分析知乎问题URL，并缓存数据。')
mighty.grid(column=0, row=0, padx=0, pady=4)

# Modify adding a Label using mighty as the parent instead of win
a_label = ttk.Label(mighty, text="待分析知乎问题URL：")
a_label.grid(column=0, row=0, sticky='W')

# Modified Button Click Function
def _click(): 
    split_url = url_entered.get().split('/')
    is_url_valid = False
    for w in split_url:
        if w == 'question':
            is_url_valid = True
            continue
        if is_url_valid is True:
            question_id = w
            break
    if not is_url_valid:
        result_label['text'] = '网址有误，请重新输入。'
    else:
        result_label['text'] = '正在缓存...'
    #action.configure(text='正在缓存...', state="disabled")
# Modify adding a Label using mighty as the parent instead of win
result_label = ttk.Label(mighty, text="")
result_label.grid(column=0, row=2, sticky='W')

# Adding a Textbox Entry widget
name = tk.StringVar()
url_entered = ttk.Entry(mighty, width=12, textvariable=name)
url_entered.grid(column=0, row=1, sticky='W')               # align left/West

# Adding a Button
action = ttk.Button(mighty, text="缓存", command=_click)   
action.grid(column=1, row=1)                                

# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit() 

# Creating a Menu Bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

# Add menu items
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add another Menu to the Menu Bar and an item
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)


url_entered.focus()      # Place cursor into name Entry
#======================
# Start GUI
#======================
win.mainloop()