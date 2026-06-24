md5_path = "./md5.txt"
collection_name = "rag"
persist_directory = "ai_agent/project/demo1/chroma_db"

chunk_size = 1000 # 分割后的文本段最大长度
chunk_overlap = 100 # 连续文本段之间的字符重叠数量
separators = ["\n\n", ".", "!", "?", "。", "！"] # 段落划分的符号
max_split_char_number = 1000 # 文本分隔的阈值

similarity_threshold = 2 # 检索返回匹配的文档数量

embedding_model = "nomic-embed-text-v2-moe:latest"