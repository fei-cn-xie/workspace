"""
知识库
"""

import os
import config_data as config
import hashlib

def check_md5(md5_str: str):
    """检查传入的md5字符串是否已经被处理过了"""
    if not os.path.exists(config.md5_path):
        # 文件不存在
        open(config.md5_path, 'w', encoding="utf-8").close
        return False
    else:
        for line in open(config.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip() # 处理前后空格
            if line == md5_str:
                return True
        return False
    


def save_md5(md5_str: str):
    """
    将传入的md5字符串传入到文件内保存
    """
    with open(config.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + "\n")


def convert_to_md5(text:str, encoding:str="utf-8") -> str:
    """
    将传入的字符串转化为md5字符串
    """
    # 将字符转为字节流
    str_bytes = text.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes) 
    md5_hex = md5_obj.hexdigest() # 得到md5的16进制字符串
    return md5_hex

class KnowledgeBaseService(object):

    def __init__(self):
        self.chroma = None # 向量存储的实例 Chroma向量库对象
        self.spliter = None # 文本分割器的对象

    def upload_by_str(self, data:str, name:str):
        """
        将传入的字符串向量化.存入到向量数据库中
        """
        pass

if __name__ == "__main__":
    r = check_md5("7a8941058aaf4df5147042ce104568da")
    print(r)
    save_md5("7a8941058aaf4df5147042ce104568da")
    r = check_md5("7a8941058aaf4df5147042ce104568da")
    print(r)