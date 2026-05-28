md5_path = "./md5.txt"
collection_name = "rag"
persist_directory = "./chroma_db"

chunk_size = 1000 # 分割后的文本段最大长度
chunk_overlap = 100 # 连续文本段之间的字符重叠数量
separators = ["\n\n", ".", "!", "?", "。", "！"] # 段落划分的符号
max_split_char_number = 1000 # 文本分隔的阈值