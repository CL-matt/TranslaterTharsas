import sys
import os

def setup_paths():
    """自动添加需要导入的目录到 sys.path"""
    # 获取当前脚本路径（Traductor）
    current_path = os.path.dirname(os.path.abspath(__file__))

    # 规范化路径，确保是绝对路径
    modulos_path = os.path.abspath(os.path.join(current_path, '..', 'Modulos'))
    dict_path = os.path.abspath(os.path.join(current_path, '..', 'Dicts'))
    
    # 将目录添加到 Python 搜索路径
    sys.path.append(modulos_path)
    sys.path.append(dict_path)
    
    # 查看路径
    print(f"已添加 Modulos 目录: {modulos_path}")
    print(f"已添加 Dicts 目录: {dict_path}")

# 让其他文件能调用此脚本时也能执行路径设置
setup_paths()
