import os
import json

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 设定输入词典文件路径
input_dict_file = os.path.join(current_dir, "My_Dict.json")

# 设定输出词典文件夹路径
output_dir = os.path.join(current_dir, "Split_Dicts")
os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

# 读取原始词典文件
with open(input_dict_file, "r", encoding="utf-8") as f:
    languages_dict = json.load(f)

# 遍历每种语言
for lang in languages_dict:
    # 遍历每个词类
    for category in languages_dict[lang]:
        # 创建新的词典结构
        new_dict = {lang: {category: languages_dict[lang][category]}}
        
        # 设置输出文件路径
        output_file = os.path.join(output_dir, f"My_Dict_{lang}_{category}.json")
        
        # 保存到新的 JSON 文件
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(new_dict, f, ensure_ascii=False, indent=4)
        
        print(f"已创建文件: {output_file}")

print("拆分完成！")