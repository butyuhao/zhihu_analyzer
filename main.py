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
from enum import Enum
import crawler
from app_context import AppCtx
import os
import define

# class pipeline(Enum):
#     START = 1
#     CRAWLER = 2

# is_finish = False
# next_step = pipeline.START
# def switch(case):
#     return {
#         pipeline.START : start,
#     }.get(case, -1)

# def start:

#instantiate app context object
app_ctx = AppCtx()

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
#=========
#  TAB1
#=========
# LabelFrame using tab1 as the parent
frame_download_page = ttk.LabelFrame(tab1, text='键入待分析知乎问题URL，并缓存数据。')
frame_download_page.grid(column=0, row=0, padx=0, pady=10)

# Modify adding a Label using frame_download_page as the parent instead of win
a_label = ttk.Label(frame_download_page, text="待分析知乎问题URL：")
a_label.grid(column=0, row=0, sticky='W')

# Modified Button Click Function

def _click():
    split_url = url_entered.get().split('/')
    is_url_valid = False
    for w in split_url:
        if w == 'question':
            is_url_valid = True
            continue
        if (is_url_valid is True):
            app_ctx.question_id = w
            break
    if not is_url_valid:
        result_label['text'] = '网址有误，请重新输入。'
    else:
        result_label['text'] = '正在缓存...'
        crawler.run(app_ctx)
        result_label['text'] = '缓存完成'


# Adding a Textbox Entry widget
name = tk.StringVar()
url_entered = ttk.Entry(frame_download_page, width=12, textvariable=name)
url_entered.grid(column=0, row=1, sticky='W')               # align left/West

# Adding a Button
action = ttk.Button(frame_download_page, text="缓存", command=_click)
action.grid(column=1, row=1)

# Modify adding a Label using frame_download_page as the parent instead of win
result_label = ttk.Label(frame_download_page, text="")
result_label.grid(column=0, row=2, sticky='W')

label_filter = ttk.Label(frame_download_page, text="关键词过滤(使用;分隔)：")
label_filter .grid(column=0, row=3, sticky='W')

label_filter = ttk.Label(frame_download_page, text="正选")
label_filter .grid(column=0, row=4, sticky='W')

# Adding a Textbox Entry widget
name = tk.StringVar()
keyword_include= ttk.Entry(frame_download_page, width=12, textvariable=name)
keyword_include.grid(column=1, row=4, sticky='W')              

label_filter = ttk.Label(frame_download_page, text="反选")
label_filter .grid(column=0, row=5, sticky='W')

# Adding a Textbox Entry widget
name = tk.StringVar()
keyword_not_include = ttk.Entry(frame_download_page, width=12, textvariable=name)
keyword_not_include.grid(column=1, row=5, sticky='W')            

def _action_filter():
    try:
        if keyword_include.get() != '':
            for w in keyword_include.get().split(';'):
                app_ctx.keyword_include.append(w)
        if keyword_not_include.get() != '':
            for w in keyword_not_include.get().split(';'):
                app_ctx.keyword_not_include.append(w)
    finally:
        if define.test_mode:
            print('keyword_include', app_ctx.keyword_include)
            print('keyword_not_include', app_ctx.keyword_not_include)
        pass

# Adding a Button
action_filter = ttk.Button(frame_download_page, text="筛选", command=_action_filter)
action_filter.grid(column=0, row=6)


#=========
#  TAB2
#=========
# LabelFrame using tab1 as the parent
frame_text_reader = ttk.LabelFrame(tab2, text='查看并标记喜欢的内容')
frame_text_reader.grid(column = 0, row = 0)
# Add text box
text = tk.Text(frame_text_reader,width = 80,height = 32)
text.pack(side = tk.LEFT, fill = tk.Y)

#滚动条
scroll = tk.Scrollbar(frame_text_reader)
scroll.pack(side = tk.RIGHT, fill = tk.Y)
#滚动条与窗体相互绑定
scroll.config(command = text.yview)
text.config(yscrollcommand = scroll.set)
def _action_start_mark():
    text.delete(0.0,tk.END)
    if(app_ctx.is_crawler_finish is True or os.path.exists(define.comments_path)):
        app_ctx._load_comments(define.comments_path)
        text.insert(tk.INSERT,app_ctx.comments[app_ctx.cur_comment])
    else:
        text.insert(tk.INSERT,'请先在Step1中缓存页面数据...')

frame_button_bar = ttk.LabelFrame(tab2)
frame_button_bar.grid(column = 0, row = 1)
#增加按键
action1 = ttk.Button(frame_button_bar, text="开始标记", command=_action_start_mark)
action1.grid(column = 0, row = 0)

def _action_next_comment():
    if app_ctx.cur_comment + 1 < len(app_ctx.comments):
        app_ctx.cur_comment += 1
        text.delete(0.0,tk.END)
        text.insert(tk.INSERT,app_ctx.comments[app_ctx.cur_comment])

def _action_previous_comment():
    if app_ctx.cur_comment - 1 >= 0:
        app_ctx.cur_comment -= 1
        text.delete(0.0,tk.END)
        text.insert(tk.INSERT,app_ctx.comments[app_ctx.cur_comment])
def _action_like():
    if not app_ctx.cur_comment in app_ctx.like_list:
        app_ctx.like_list.append(app_ctx.cur_comment)

#增加按键
action2 = ttk.Button(frame_button_bar, text="上一个", command=_action_previous_comment)
action2.grid(column = 1, row = 0)

#增加按键
action3 = ttk.Button(frame_button_bar, text="下一个", command=_action_next_comment)
action3.grid(column = 2, row = 0)

#增加按键
action4 = ttk.Button(frame_button_bar, text="喜欢", command=_action_like)
action4.grid(column = 3, row = 0)


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
# ======================
# Start GUI
# ======================
win.mainloop()
