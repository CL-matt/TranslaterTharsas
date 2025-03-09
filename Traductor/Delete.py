import tkinter as tk
from tkinter import messagebox
import My_Dict  # 确保引入更新后的 My_Dict.py

# 重新加载词典
def reload_dict():
    global languages_dict
    languages_dict = My_Dict.load_dict()

# 查询单词
def search_translation():
    word = entry_delete.get()
    lang = language_var.get()

    if lang in languages_dict:
        for category in languages_dict[lang]:
            if word in languages_dict[lang][category]:
                data = languages_dict[lang][category][word]
                translation = data.get("translation", "未知")
                gender = data.get("gender", "未知")
                plural = data.get("plural", "未知")

                gender_map = {"m": "阳性 (der)", "f": "阴性 (die)", "n": "中性 (das)"}
                gender_str = gender_map.get(gender, "未知")

                messagebox.showinfo("查询结果", f"单词: {word}\n翻译: {translation}\n性别: {gender_str}\n复数: {plural}")
                return

    messagebox.showwarning("查询失败", f"单词 '{word}' 不在词典中")

# 删除单词
def delete_translation():
    word = entry_delete.get()
    lang = language_var.get()

    if My_Dict.delete_word(lang, word):
        messagebox.showinfo("成功", f"单词 '{word}' 已删除")
        delete_window.destroy()
        reload_dict()
    else:
        messagebox.showwarning("错误", f"单词 '{word}' 不存在于字典中")

# 创建 Tk 窗口
delete_window = tk.Tk()
delete_window.title("查询 / 删除单词")
delete_window.geometry("800x500")

tk.Label(delete_window, text="输入单词：", font=("Arial", 12)).pack(pady=5)
entry_delete = tk.Entry(delete_window, font=("Arial", 12))
entry_delete.pack(pady=5)

tk.Label(delete_window, text="选择语言：", font=("Arial", 12)).pack()
language_var = tk.StringVar(value="zh")
tk.Radiobutton(delete_window, text="中文", variable=language_var, value="zh").pack()
tk.Radiobutton(delete_window, text="通用语", variable=language_var, value="created").pack()

tk.Button(delete_window, text="查询单词", font=("Arial", 12), command=search_translation).pack(pady=5)
tk.Button(delete_window, text="删除单词", font=("Arial", 12), command=delete_translation).pack(pady=5)

delete_window.mainloop()
