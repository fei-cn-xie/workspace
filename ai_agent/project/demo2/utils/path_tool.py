"""
为整个工程提供统一的绝对路径
"""

import os

def get_project_root() -> str:
    """
    获取工程所在的根目录
    :return: 根目录
    """

    # 获取当前代码文件的绝对路径
    current_file = os.path.abspath(__file__)

    # 获取工程的根目录，先获取utils目录
    current_dir = os.path.dirname(current_file)
    # 获取工程的根目录
    project_root = os.path.dirname(current_dir)

    return project_root

def get_abs_path(relative_path: str) -> str:
    """
    根据相对路径获取绝对路径
    """
    return os.path.join(get_project_root(), relative_path)


if __name__ == "__main__":
    print(get_abs_path("config/config.txt"))