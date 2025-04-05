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
def get_article(word, lang, target_lang):
    # 只有在目标语言是通用语且源语言是中文时才添加冠词
    if target_lang == "created" and lang == "zh":
        if target_lang in languages_dict and "noun" in languages_dict[target_lang]:
            if word in languages_dict[target_lang]["noun"]:
                gender = languages_dict[target_lang]["noun"][word].get("gender", "")
                return {"m": "der", "f": "die", "n": "das"}.get(gender, "")
    return ""

# **识别单词类别**
def get_word_category(word, lang):
    for category in ["noun", "v", "adj", "adv"]:
        if word in languages_dict.get(lang, {}).get(category, {}):
            return category
    return None

# **优化动词变位**0311
def conjugate_verb(verb, subject, tense):
    # 获取动词词根，假设动词以 -ar, -er, -ir 结尾
    if verb.endswith('ar'):
        verb_root = verb[:-2]  # 去掉末尾的 'ar'
        ending_type = '-ar'
    elif verb.endswith('er'):
        verb_root = verb[:-2]  # 去掉末尾的 'er'
        ending_type = '-er'
    elif verb.endswith('ir'):
        verb_root = verb[:-2]  # 去掉末尾的 'ir'
        ending_type = '-ir'
    else:
        # 如果动词不符合结尾规则，返回原动词
        return verb

    # 根据时态和主语选择正确的变位
    if tense == "present":
        conjugation_table = {
            "Jo": {"-ar": "o", "-er": "e", "-ir": "e"},
            "Tu": {"-ar": "as", "-er": "as", "-ir": "as"},
            "Er": {"-ar": "a", "-er": "a", "-ir": "a"},
            "Sie": {"-ar": "a", "-er": "a", "-ir": "a"},
            "Nou": {"-ar": "am", "-er": "em", "-ir": "em"},
            "Vou": {"-ar": "ís", "-er": "ís", "-ir": "ís"},
            "lou": {"-ar": "an", "-er": "an", "-ir": "an"}
        }
    elif tense == "past":
        conjugation_table = {
            "Jo": {"-ar": "é", "-er": "é", "-ir": "é"},
            "Tu": {"-ar": "ast", "-er": "ast", "-ir": "ast"},
            "Er": {"-ar": "ó", "-er": "ó", "-ir": "ó"},
            "Sie": {"-ar": "ó", "-er": "ó", "-ir": "ó"},
            "Nou": {"-ar": "ams", "-er": "ams", "-ir": "ams"},
            "Vou": {"-ar": "ás", "-er": "ás", "-ir": "ás"},
            "lou": {"-ar": "án", "-er": "én", "-ir": "én"}
        }
    elif tense == "future":
        conjugation_table = {
            "Jo": {"-ar": "é", "-er": "é", "-ir": "é"},
            "Tu": {"-ar": "ás", "-er": "ás", "-ir": "ás"},
            "Er": {"-ar": "á", "-er": "á", "-ir": "á"},
            "Sie": {"-ar": "á", "-er": "á", "-ir": "á"},
            "Nou": {"-ar": "ám", "-er": "ám", "-ir": "ám"},
            "Vou": {"-ar": "áis", "-er": "áis", "-ir": "áis"},
            "lou": {"-ar": "án", "-er": "án", "-ir": "án"}
        }
    else:
        # 如果时态未知，直接返回原动词
        return verb

    # 获取主语对应的变位
    if subject in conjugation_table:
        ending = conjugation_table[subject][ending_type]
        return f"{verb_root}{ending}"
    else:
        # 如果主语未知，直接返回原动词
        return verb

# **自动识别时态** 要改
def detect_tense(words):
    past_indicators = {"昨天", "以前", "曾经", "过去"}
    future_indicators = {"明天", "将来", "以后", "未来"}
    
    if any(word in past_indicators for word in words):
        return "past"
    if any(word in future_indicators for word in words):
        return "future"
    return "present"

# **优化句子翻译**
def translate_sentence(sentence, lang, target_lang):
    words = tokenize(sentence)
    tense = detect_tense(words)
    subjects, verbs, objects = [], [], []
    
    for word in words:
        translated_word = translate(word, lang, target_lang)
        category = get_word_category(word, lang)
        
        if category == "noun":
            article = get_article(word, lang, target_lang)
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

# **添加不规则动词**
def add_irregular_verb():
    def save_irregular_verb():
        verb = entry_verb.get()
        tense = tense_var.get()
        subject = subject_var.get()
        conjugation = entry_conjugation.get()
        
        if verb and tense and subject and conjugation:
            if verb not in irregular_verbs:
                irregular_verbs[verb] = {}
            if tense not in irregular_verbs[verb]:
                irregular_verbs[verb][tense] = {}
            irregular_verbs[verb][tense][subject] = conjugation
            
            messagebox.showinfo("成功", f"已添加不规则动词：{verb} 在 {tense} 时态下，{subject} 的变位为 {conjugation}")
            add_window.destroy()
        else:
            messagebox.showwarning("警告", "请填写所有字段！")
    
    add_window = tk.Toplevel(root)
    add_window.title("添加不规则动词")
    
    tk.Label(add_window, text="动词：").grid(row=0, column=0)
    entry_verb = tk.Entry(add_window)
    entry_verb.grid(row=0, column=1)
    
    tk.Label(add_window, text="时态：").grid(row=1, column=0)
    tense_var = tk.StringVar(value="present")
    tense_options = ["present", "past", "future"]
    tense_menu = tk.OptionMenu(add_window, tense_var, *tense_options)
    tense_menu.grid(row=1, column=1)
    
    tk.Label(add_window, text="主语：").grid(row=2, column=0)
    subject_var = tk.StringVar(value="Jo")
    subject_options = ["Jo", "Tu", "Er", "Sie", "Nou", "Vou", "lou"]
    subject_menu = tk.OptionMenu(add_window, subject_var, *subject_options)
    subject_menu.grid(row=2, column=1)
    
    tk.Label(add_window, text="变位：").grid(row=3, column=0)
    entry_conjugation = tk.Entry(add_window)
    entry_conjugation.grid(row=3, column=1)
    
    tk.Button(add_window, text="保存", command=save_irregular_verb).grid(row=4, column=0, columnspan=2)

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

# **添加不规则动词按钮**
tk.Button(root, text="添加不规则动词", command=add_irregular_verb).pack(pady=10)

# **优化：加载词典**
languages_dict = My_Dict.load_dict()
root.mainloop()