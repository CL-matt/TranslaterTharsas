# "": {"en": {"word": "", "pos": "", "gender": None}, "created": {"word": "", "pos": "", "gender": ""}},
# "en" English "ch" 中文 
# word 单词原型 
# pos 词类 noun adj adv v
# gender 词性 der-masculine die-feminine das-neuter 默认英语没有

# 按词性分类的字典，名词包含性别和复数形式信息
import json
import os
from datetime import datetime
import shutil

# 获取当前脚本（My_Dict.py）所在目录
current_dir_dic = os.path.dirname(os.path.abspath(__file__))

# 设定 JSON 文件存储路径（相对路径：../Dicts/My_Dict.json）
DICT_FILE = os.path.join(current_dir_dic, "..", "Dicts", "My_Dict.json")
BACKUP_FILE = os.path.join(current_dir_dic, "..", "Dicts", "My_Dict_Backup.json")

# 确保 Dicts 目录存在
DICT_DIR = os.path.dirname(DICT_FILE)
if not os.path.exists(DICT_DIR):
    os.makedirs(DICT_DIR)

languages_dict = {
    "zh": {
        "noun": {
            "水": {"translation": "Aqua", "gender": "n", "plural": ""},
            
        },
        "adj": {
            "大": "",
            
        },
        "adv": {
            "快速地": "",
        },
        "v": {
            "吃": "",
        }
    },
    "created": {
        "noun": {
            "Aqua": {"translation": "水", "gender": "n", "plural": "Aquas"},
        },
        "adj": {
            "zuri": "大",
        },
        "adv": {
            "taza": "",
        },
        "v": {
            "taza": "123",
        }
    }
}

# 加载 JSON 数据
def load_dict():
    global languages_dict
    try:
        with open(DICT_FILE, "r", encoding="utf-8") as f:
            languages_dict = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        languages_dict = {}  # 如果 JSON 文件不存在，则创建一个空字典
    return languages_dict

# 备份 JSON 数据
def backup_dict():
    if os.path.exists(DICT_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 获取当前时间戳
        backup_filename = f"E:\\OneDrive - UPV\\Thalassar\\Colangs\\Dicts\\My_Dict_backup_{timestamp}.json"
        shutil.copy(DICT_FILE, backup_filename)
        print(f"✅ 备份已创建: {backup_filename}")

# 删除多余备份,最多保留五个
def clean_old_backups(max_files=5):
    """先调用 `backup_dict()`，然后调用 `clean_old_backups(n)` 保留 n 个最近的备份"""
    backup_files = sorted(
        [f for f in os.listdir(DICT_DIR) if f.startswith("My_Dict_backup_")],
        key=lambda f: os.path.getmtime(os.path.join(DICT_DIR, f)),
        reverse=True
    )

    for old_file in backup_files[max_files:]:  # 删除多余的备份
        os.remove(os.path.join(DICT_DIR, old_file))
        print(f"🗑️ 已删除旧备份: {old_file}")

# 保存到 JSON
def save_dict():
    with open(DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(languages_dict, f, ensure_ascii=False, indent=4)

# 添加单词（修改词典时自动保存）
def add_word(lang, category, word, translation, gender=None, plural=None):
    if lang not in languages_dict:
        languages_dict[lang] = {}
    if category not in languages_dict[lang]:
        languages_dict[lang][category] = {}

    languages_dict[lang][category][word] = {
        "translation": translation
    }
    if gender:
        languages_dict[lang][category][word]["gender"] = gender
    if plural:
        languages_dict[lang][category][word]["plural"] = plural

    save_dict()  # **每次修改后自动保存！**

# 删除单词（修改后自动保存）
def delete_word(lang, word):
    if lang in languages_dict:
        for category in languages_dict[lang]:  # 遍历所有类别
            if word in languages_dict[lang][category]:
                del languages_dict[lang][category][word]
                save_dict()  # **修改后保存**
                return True
    return False  # 如果找不到单词，返回 False

# 恢复
def restore_backup():
    """恢复备份，将 My_Dict_backup.json 复制回 My_Dict.json"""
    if os.path.exists(BACKUP_FILE):
        shutil.copy(BACKUP_FILE, DICT_FILE)
        print("✅ 词典已从备份恢复")
    else:
        print("⚠️ 没有找到备份文件！")

# 调用 restore_backup() 可恢复备份

# **初始化：启动时加载 JSON**
load_dict()
#backup_dict()