import sys
import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 添加其他文件夹到 sys.path
project_dir = os.path.abspath(os.path.join(current_dir,"pinyin"))
project_dir_1 = os.path.abspath(os.path.join(current_dir,"installer"))
sys.path.append(project_dir)
sys.path.append(project_dir_1)
# 现在可以导入项目中的其他模块
import pypinyin
import tkinter as tk
from tkinter import messagebox

def reverse_pinyin_translation(chinese_text):
    # 获取拼音（带声调符号）
    pinyin_list = pypinyin.pinyin(chinese_text, style=pypinyin.Style.TONE)
    
    # 将拼音列表转换为字符串
    pinyin_str = ''.join([item[0] for item in pinyin_list])
    
    # 反转拼音字符串
    reversed_pinyin = pinyin_str[::-1]
    
    return reversed_pinyin

def translate_text():
    chinese_input = entry.get()
    if not chinese_input:
        messagebox.showwarning("输入错误", "请输入中文文本！")
        return
    translated_output = reverse_pinyin_translation(chinese_input)
    result_label.config(text=f"翻译结果: {translated_output}")

# 创建 GUI 界面
root = tk.Tk()
root.title("阿弥诺斯语翻译器")
root.geometry("500x300")

tk.Label(root, text="请输入中文:").pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

translate_button = tk.Button(root, text="翻译", command=translate_text)
translate_button.pack(pady=5)

result_label = tk.Label(root, text="翻译结果:")
result_label.pack(pady=10)

root.mainloop()
