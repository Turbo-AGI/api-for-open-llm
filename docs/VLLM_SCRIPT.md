## docker 镜像

构建镜像

```shell
docker build -f docker/Dockerfile.vllm -t llm-api:vllm .
```

## docker 启动模型

### 环境变量含义

+ `MODEL_NAME`: 模型名称，如 `qwen`、`baichuan-13b-chat` 等


+ `MODEL_PATH`: 开源大模型的文件所在路径


+ `TRUST_REMOTE_CODE`: 是否使用外部代码


+ `TOKENIZE_MODE`（可选项）: `tokenizer` 的模式，默认为 `auto`


+ `TENSOR_PARALLEL_SIZE`（可选项）: `GPU` 数量，默认为 `1`


+ `PROMPT_NAME`（可选项）: 使用的对话模板名称，如果不指定，则将根据模型名找到对应的模板


模型启动命令统一为

```shell
docker run -it -d --gpus all --ipc=host --net=host -p 7891:8000 --name=vllm-server \
    --ulimit memlock=-1 --ulimit stack=67108864 \
    -v `pwd`:/workspace \
    llm-api:vllm \
    python api/vllm_server.py
```

**不同模型只需要将 [.env.vllm.example](../.env.vllm.example) 文件内容复制到 `.env` 文件中，然后修改 `.env` 文件中环境变量**

**修改内容参考下面的模型**


### Qwen-7b-chat

Qwen/Qwen-7B-Chat:


```shell
MODEL_NAME=qwen
MODEL_PATH=Qwen/Qwen-7B-Chat # 模型所在路径，若使用docker，则为在容器内的路径
```

### InternLM

internlm-chat-7b:

```shell
MODEL_NAME=internlm
MODEL_PATH=internlm/internlm-chat-7b
```

### Baichuan-13b-chat

baichuan-inc/Baichuan-13B-Chat:

```shell
MODEL_NAME=baichuan-13b-chat
MODEL_PATH=baichuan-inc/Baichuan-13B-Chat
TENSOR_PARALLEL_SIZE=2
```