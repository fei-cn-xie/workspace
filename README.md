

## 模型下载

```sh
pip install huggingface_hub
hf download ornith-ai/0rnith-1.0-9B-GGUF ornith-1.0-9b-04_K_M.gguf
```

## llama 启动

```sh
./llama-cli.exe -m "D:\models\ornith-1.0-9b-Q4_K_M.gguf" -p "你好，介绍一下你自己" -n 256 -c 4096 -ngl 99

llama-cli -m "D:\huggingface_model\huggingface\hub\models--ornith-ai--Ornith-1.0-9B-GGUF\snapshots\3296bc7a404871a72ac3f1903f561459c09b5c17\ornith-1.0-9b-Q4_K_M.gguf"

```


## 启动后台服务

```sh
llama-server -m 模型文件名

```

> ollama下载的模型，通过改后缀名称为.gguf，也可使用。