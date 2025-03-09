"""
这是一个用于可以翻译中文-人造语言的编译器py脚本
"""

__author__ = "温茶"
__copyright__ = "Copyright (C) 2025, ranrylios"
__license__ = None
__version__ = "Alpha 0.1"
__email__ = "ranrylios15c@gmail.com"

#添加需要的路径
import SearchPath as SP
#tk 脚本
import tkinter as tk
from tkinter import messagebox

import My_Dict  # 导入词典
import jieba  # 用于更好的分词处理（针对中文）

# 重新加载词典
def reload_dict():
    global languages_dict
    languages_dict = My_Dict.load_dict()

# **优化分词**（支持中文）
def tokenize(sentence):
    return list(jieba.cut(sentence))  # 中文分词

# **获取名词冠词**
def get_article(word, lang):
    if lang in languages_dict and "noun" in languages_dict[lang]:
        if word in languages_dict[lang]["noun"]:
            gender = languages_dict[lang]["noun"][word].get("gender", "")
            return {"m": "der", "f": "die", "n": "das"}.get(gender, "")
    return ""

# **识别单词类别**
def get_word_category(word, lang):
    for category in ["noun", "v", "adj", "adv"]:
        if word in languages_dict.get(lang, {}).get(category, {}):
            return category
    return None

# **优化动词变位** 要改
def conjugate_verb(verb, subject, tense):
    # 过去式和将来式处理
    if tense == "past":
        return f"{verb}ed"
    elif tense == "future":
        return f"will {verb}"

    # 现在时，进行人称变位
    if subject.lower() in ["he", "she", "it"]:
        return f"{verb}s"
    
    return verb

# **自动识别时态** 要改
def detect_tense(words):
    past_indicators = {"昨天", "以前", "曾经"}
    future_indicators = {"明天", "将来", "以后"}
    
    if any(word in past_indicators for word in words):
        return "past"
    if any(word in future_indicators for word in words):
        return "future"
    return "present"

# **优化句子翻译** 要改
def translate_sentence(sentence, lang):
    words = tokenize(sentence)
    tense = detect_tense(words)
    subjects, verbs, objects = [], [], []
    
    for word in words:
        translated_word = translate(word, lang)
        category = get_word_category(word, lang)
        
        if category == "noun":
            article = get_article(word, lang)
            translated_word = f"{article} {translated_word}".strip()
            if not subjects:
                subjects.append(translated_word)  # 默认第一个名词是主语
            else:
                objects.append(translated_word)  # 其余名词是宾语
        elif category == "v":
            verbs.append(translated_word)
        else:
            objects.append(translated_word)  # 其他归入宾语

    # **调整动词变位**
    if verbs and subjects:
        verbs[0] = conjugate_verb(verbs[0], subjects[0], tense)

    # **组装 SVO 语序**
    return ' '.join(subjects + verbs + objects)

# **单词翻译函数**
def translate(word, lang):
    if lang in languages_dict:
        for category in languages_dict[lang]:
            if word in languages_dict[lang][category]:
                return languages_dict[lang][category][word]['translation']
    
    ask_for_translation(word, lang)
    return word  # 词典里没有的词，暂时保留原词

# **优化添加单词（支持所有词性）**
def ask_for_translation(word, lang):
    def save_translation():
        new_translation = entry_translation.get()
        category = category_var.get()
        if not new_translation:
            messagebox.showwarning("警告", "翻译不能为空！")
            return
        
        My_Dict.add_word(lang, category, word, new_translation)
        messagebox.showinfo("成功", f"已添加：{word} → {new_translation}")
        add_window.destroy()
        reload_dict()
    
    add_window = tk.Toplevel(root)
    add_window.title("添加新翻译")
    
    tk.Label(add_window, text=f"添加 '{word}' 的翻译：").pack()
    entry_translation = tk.Entry(add_window)
    entry_translation.pack()
    
    # **用户选择词性**
    category_var = tk.StringVar(value="noun")
    tk.Label(add_window, text="选择词性：").pack()
    word_types = [("名词", "noun"), ("动词", "v"), ("形容词", "adj"), ("副词", "adv")]
    for text, value in word_types:
        tk.Radiobutton(add_window, text=text, variable=category_var, value=value).pack()

    tk.Button(add_window, text="保存", command=save_translation).pack()

# **优化GUI界面**
root = tk.Tk()
root.title("通用语翻译器")
root.geometry("900x500")

tk.Label(root, text="请输入句子：", font=("Arial", 14)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), width=50)
entry.pack(pady=10)

language_var = tk.StringVar(value="zh")
tk.Label(root, text="选择输入语言：", font=("Arial", 14)).pack(pady=5)
tk.Radiobutton(root, text="中文", variable=language_var, value="zh").pack()
tk.Radiobutton(root, text="通用语", variable=language_var, value="created").pack()

# **改进翻译结果显示**
result_text = tk.Text(root, font=("Arial", 14), height=5, wrap="word")
result_text.pack(pady=10)

def show_translation():
    sentence = entry.get()
    lang = language_var.get()
    translated_sentence = translate_sentence(sentence, lang)
    result_text.delete(1.0, tk.END)  # 清空旧的翻译结果
    result_text.insert(tk.END, translated_sentence)  # 显示新翻译

tk.Button(root, text="翻译", font=("Arial", 14), command=show_translation).pack(pady=20)

# **优化：加载词典**
languages_dict = My_Dict.load_dict()
root.mainloop()