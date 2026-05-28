"""
知识库
"""

import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

embedding_model = OllamaEmbeddings(model="nomic-embed-text-v2-moe:latest")

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
        # 如果文件夹不存在则创建,如果存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name, # 数据库的表名
            embedding_function=embedding_model,
            persist_directory=config.persist_directory, # 数据库本地存储文件夹
        ) # 向量存储的实例 Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap, # 连续文本段之间的字符重叠数量
            separators=config.separators, # 段落划分的符号
            length_function=len, # 长度统计使用什么函数
            
        ) # 文本分割器的对象

    def upload_by_str(self, data:str, filename:str):
        """
        将传入的字符串向量化.存入到向量数据库中
        """
        md5_hex = convert_to_md5(data)
        if(check_md5(md5_hex)):
            return "内容已经存在知识库中"
        knowledge_chunks: list[str] = []
        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            "operator": "Fei",

        }
        # 内容加载到向量数据库
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        # 记录数据已存储
        save_md5(md5_hex)
        return "[Success] 内容成功载入向量数据库"

if __name__ == "__main__":
    ks = KnowledgeBaseService()
    r = ks.upload_by_str("州街道", "testfile")
    print(r)
