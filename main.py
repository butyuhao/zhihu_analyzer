import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from enum import Enum
import crawler
from app_context import AppCtx
import os
import define
from plot_word_cloud import generate_wordcloud
from word2vec import get_similar_doc

app_ctx = AppCtx()

win = tk.Tk()
win.title("知乎话题分析器 by butyuhao")
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Step1')
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Step2')
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='分析')
tab4 = ttk.Frame(tabControl)
tabControl.add(tab4, text='推荐')

tabControl.pack(expand=2, fill="both") 
# =========
#  TAB1
# =========

frame_download_page = ttk.LabelFrame(tab1, text='键入待分析知乎问题URL，并缓存数据。')
frame_download_page.grid(column=0, row=0, padx=0, pady=10)

label_url = ttk.Label(frame_download_page, text="待分析知乎问题URL：")
label_url.grid(column=0, row=0, sticky='W')

def _click():
    split_url = entry_url_entered.get().split('/')
    is_url_valid = False
    for w in split_url:
        if w == 'question':
            is_url_valid = True
            continue
        if (is_url_valid is True):
            app_ctx.question_id = w
            break
    if not is_url_valid:
        label_download_result['text'] = '网址有误，请重新输入。'
    else:
        label_download_result['text'] = '正在缓存...'
        crawler.run(app_ctx)
        label_download_result['text'] = '缓存完成'

name = tk.StringVar()
entry_url_entered = ttk.Entry(frame_download_page, width=12, textvariable=name)
entry_url_entered.grid(column=0, row=1, sticky='W') 

button_download = ttk.Button(frame_download_page, text="缓存", command=_click)
button_download.grid(column=1, row=1)

label_download_result = ttk.Label(frame_download_page, text="")
label_download_result.grid(column=0, row=2, sticky='W')

label_filter1 = ttk.Label(frame_download_page, text="关键词过滤(使用;分隔)：")
label_filter1 .grid(column=0, row=3, sticky='W')

label_filter2 = ttk.Label(frame_download_page, text="正选")
label_filter2.grid(column=0, row=4, sticky='W')

name = tk.StringVar()
keyword_include = ttk.Entry(frame_download_page, width=12, textvariable=name)
keyword_include.grid(column=1, row=4, sticky='W')

label_filter3= ttk.Label(frame_download_page, text="反选")
label_filter3.grid(column=0, row=5, sticky='W')

name = tk.StringVar()
entry_keyword_exclude = ttk.Entry(frame_download_page, width=12, textvariable=name)
entry_keyword_exclude.grid(column=1, row=5, sticky='W')


def _button_download_filter():
    try:
        if keyword_include.get() != '':
            for w in keyword_include.get().split(';'):
                if not w in app_ctx.keyword_include:
                    app_ctx.keyword_include.append(w)
            filtered_comments = []
            for c in app_ctx.comments:
                for w in app_ctx.keyword_include:
                    if w in c['content']:
                        filtered_comments.append(c)
                        continue
            app_ctx.comments = filtered_comments

        if entry_keyword_exclude.get() != '':
            for w in entry_keyword_exclude.get().split(';'):
                if not w in app_ctx.keyword_exclude:
                    app_ctx.keyword_exclude.append(w)
            for c in app_ctx.comments:
                for w in app_ctx.keyword_exclude:
                    if w in c['content']:
                        app_ctx.comments.remove(c)
                        continue
    finally:
        if define.test_mode:
            print('keyword_include', app_ctx.keyword_include)
            print('entry_keyword_exclude', app_ctx.keyword_exclude)
            print('len(app_ctx.comments)', len(app_ctx.comments))
        pass

button_download_filter = ttk.Button(
    frame_download_page, text="筛选", command=_button_download_filter)
button_download_filter.grid(column=0, row=6)


# =========
#  TAB2
# =========

frame_text_reader = ttk.LabelFrame(tab2, text='查看并标记喜欢的内容')
frame_text_reader.grid(column=0, row=0)

text = tk.Text(frame_text_reader, width=80, height=32)
text.pack(side=tk.LEFT, fill=tk.Y)

scroll = tk.Scrollbar(frame_text_reader)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)


def _button_download_start_mark():
    '''
    如果当前comments中有数据就直接读出来
    如果当前comments没数据（程序刚运行），则如果有缓存好的
    数据，就直接读，否则提示用户缓存
    '''
    text.delete(0.0, tk.END)
    if app_ctx.comments is not None:
        text.insert(tk.INSERT, app_ctx.comments[app_ctx.cur_comment])
    elif(app_ctx.is_crawler_finish is True or os.path.exists(define.comments_path)):
        app_ctx._load_comments(define.comments_path)
        text.insert(tk.INSERT, app_ctx.comments[app_ctx.cur_comment])
    else:
        text.insert(tk.INSERT, '请先在Step1中缓存页面数据...')


frame_button_bar = ttk.LabelFrame(tab2)
frame_button_bar.grid(column=0, row=1)

button_download_start_mark = ttk.Button(frame_button_bar, text="开始标记", command=_button_download_start_mark)
button_download_start_mark.grid(column=0, row=0)


def _button_download_next_comment():
    if app_ctx.cur_comment + 1 < len(app_ctx.comments):
        app_ctx.cur_comment += 1
        text.delete(0.0, tk.END)
        text.insert(tk.INSERT, app_ctx.comments[app_ctx.cur_comment])


def _button_download_previous_comment():
    if app_ctx.cur_comment - 1 >= 0:
        app_ctx.cur_comment -= 1
        text.delete(0.0, tk.END)
        text.insert(tk.INSERT, app_ctx.comments[app_ctx.cur_comment])


def _button_download_like():
    if not app_ctx.cur_comment in app_ctx.like_list:
        app_ctx.like_list.append(app_ctx.cur_comment)


button_download_previous = ttk.Button(frame_button_bar, text="上一个",command=_button_download_previous_comment)
button_download_previous.grid(column=1, row=0)

# 增加按键
button_download_next = ttk.Button(frame_button_bar, text="下一个",command=_button_download_next_comment)
button_download_next.grid(column=2, row=0)

# 增加按键
button_download_like = ttk.Button(frame_button_bar, text="喜欢", command=_button_download_like)
button_download_like.grid(column=3, row=0)

# =========
#  TAB3
# =========

frame_result_reader = ttk.LabelFrame(tab3, text='查看分析结果')
frame_result_reader.grid(column=0, row=0)

text_result = tk.Text(frame_result_reader, width=80, height=32)
text_result.pack(side=tk.LEFT, fill=tk.Y)

scroll_text_result = tk.Scrollbar(frame_result_reader)
scroll_text_result.pack(side=tk.RIGHT, fill=tk.Y)

scroll_text_result.config(command=text_result.yview)
text_result.config(yscrollcommand=scroll_text_result.set)

frame_result_button_bar = ttk.LabelFrame(tab3)
frame_result_button_bar.grid(column=0, row=1)


def _button_download_analyse():
    generate_wordcloud(app_ctx)
    text_result.delete(0.0, tk.END)
    result_text = app_ctx.get_word_count_result(100)
    print(result_text)
    text_result.insert(tk.INSERT, app_ctx.get_word_count_result(100))


button_download_start_analyse = ttk.Button(
    frame_result_button_bar, text="开始分析", command=_button_download_analyse)
button_download_start_analyse.pack(side=tk.TOP, fill=tk.Y)

# =========
#  TAB4
# =========

frame_recommend_reader = ttk.LabelFrame(tab4, text='查看推荐结果')
frame_recommend_reader.grid(column=0, row=0)

text_recommend_result = tk.Text(frame_recommend_reader, width=80, height=32)
text_recommend_result.pack(side=tk.LEFT, fill=tk.Y)

scroll_text_recommend = tk.Scrollbar(frame_recommend_reader)
scroll_text_recommend.pack(side=tk.RIGHT, fill=tk.Y)

scroll_text_recommend.config(command=text_recommend_result.yview)
text_recommend_result.config(yscrollcommand=scroll_text_recommend.set)

frame_recommend_button_bar = ttk.LabelFrame(tab4)
frame_recommend_button_bar.grid(column=0, row=1)

def _button_download_get_recommend_result():
    app_ctx.init()
    get_similar_doc(app_ctx.like_list, 10, app_ctx)
    text_recommend_result.delete(0.0, tk.END)
    text_recommend_result.insert(
        tk.INSERT, app_ctx.comments[app_ctx.recommend_list[app_ctx.cur_recommend]])


button_get_recommend = ttk.Button(frame_recommend_button_bar, text="获取推荐结果", command=_button_download_get_recommend_result)
button_get_recommend.grid(column=0, row=0)

def _button_download_previous_recommend():
    if define.test_mode:
        print('推荐页面：上一个')
    if app_ctx.cur_recommend - 1 >= 0:
        app_ctx.cur_recommend -= 1
        text_recommend_result.delete(0.0, tk.END)
        text_recommend_result.insert(
            tk.INSERT, app_ctx.comments[app_ctx.recommend_list[app_ctx.cur_recommend]])

button_recommend_previous = ttk.Button(
    frame_recommend_button_bar, text="上一个", command=_button_download_previous_recommend)
button_recommend_previous.grid(column=1, row=0)

def _button_download_next_recommend():
    if define.test_mode:
        print('推荐页面：下一个')
        print('app_ctx.recommend_list', app_ctx.recommend_list)
        print('app_ctx.cur_recommend', app_ctx.cur_recommend)
    if app_ctx.cur_recommend + 1 < len(app_ctx.recommend_list):
        app_ctx.cur_recommend += 1
        text_recommend_result.delete(0.0, tk.END)
        text_recommend_result.insert(
            tk.INSERT, app_ctx.comments[app_ctx.recommend_list[app_ctx.cur_recommend]])

button_recommend_next = ttk.Button(
    frame_recommend_button_bar, text="下一个", command=_button_download_next_recommend)
button_recommend_next.grid(column=2, row=0)

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

entry_url_entered.focus()
# ======================
# Start GUI
# ======================
win.mainloop()
