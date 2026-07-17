
from langchain_chroma import Chroma
from utils.config_handler import chroma_config
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.path_tool import get_abs_path
from langchain_core.documents import Document

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_config["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
        )

    def get_retriver(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})
    

    def load_document(self):
        """
        从数据文件夹内读取数据文件, 转为向量存储向量库
        要计算文件的md5做去重
        :return: None
        """
        md5_hex_file_path = get_abs_path(chroma_config["md5_hex_store"])
        def check_md5_check(md5_for_check: str):
            # md5_hex_file_path = get_abs_path(chroma_config["md5_hex_store"])
            if not os.path.exists(md5_hex_file_path):
                # 创建文件
                open(md5_hex_file_path, 'w', encoding='utf-8').close()
                return False
            
            with open(md5_hex_file_path, 'w', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True # 处理过
                return False # 没处理过
        
        def save_md5_hex(md5_for_check:str):
            with open(md5_hex_file_path, 'a', encoding='utf-8') as f:
                f.write(md5_for_check + "\n")
        
        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader
            elif read_path.endswith(".pdf"):
                return pdf_loader
            
            return []
        
        allowed_files_path = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allow_knowledge_file_type"]))

        for path in allowed_files_path:
            # 获取文件的md5
            md5_hex = get_file_md5_hex(path)
            if check_md5_check(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在于知识库中, 跳过")
                continue
            
            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容, 跳过")
                    continue

                splite_document: list[Document] = self.spliter.split_documents(documents)
                if not splite_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容, 跳过")
                    continue

                # 将内容存储到向量数据库中
                self.vector_store.add_documents(splite_document)

                # 记录这个已经处理好的文件的md5值, 避免重复存入
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功")
            except Exception as e:
                # exc_info=True会记录详细的error堆栈，如果为False只会记录保存信息本身
                logger.error(f"[加载知识库]{path}加载失败: {str(e)}", exc_info=True)



if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()
    retriver = vs.get_retriver()

    res = retriver.invoke("迷路")

    for r in res:
        print(r.page_content)
        print("="*20)