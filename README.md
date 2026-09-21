## 使用hugging face下载模型

### 环境变量
```env
HF_ENDPOINT=https://hf-mirror.com
HF_HOME=D:\huggingface_modelhuggingface
HF_TOKEN=hf_xxxx
```

### 模型下载

```sh
pip install huggingface_hub
hf download hf://OBLITERATUS/Qwen3.8-27B-OBLITERATED/Qwen3.8-27B-OBLITERATED-Q6_K.gguf
hf download hf://empero-ai/Qwen3.8-9B-Distill-GGUF/Qwen3.8-9B-Q8_0.gguf
```


## llama启动
> https://llama.app/docs/cli
> https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

```sh
llama serve -m D:\huggingface_model\huggingface\hub\models--OBLITERATUS--Qwen3.8-27B-OBLITERATED\snapshots\a58c3b53b3ce71551eafde2ed5ec8df48e0f4ff8\Qwen3.8-27B-OBLITERATED-Q6_K.gguf

llama serve -m D:\huggingface_model\huggingface\hub\models--empero-ai--Qwen3.8-9B-Distill-GGUF\snapshots\760121cd70bb4c36b2b5ec58eb765e0df5987efe\Qwen3.8-9B-Q8_0.gguf --ctx-size 12288 --threads 6

llama serve -m D:\huggingface_model\huggingface\hub\models--empero-ai--Qwen3.8-9B-Distill-GGUF\snapshots\760121cd70bb4c36b2b5ec58eb765e0df5987efe\Qwen3.8-9B-Q8_0.gguf --ctx-size 0 --threads 6
```