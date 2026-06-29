# OpenCode 操作文档

## 简介

OpenCode 是一个开源的 AI 编码代理，帮助你使用 AI 工具进行高效开发。

![GitHub Stars](https://img.shields.io/github/stars/anomalyco/opencode)
![License](https://img.shields.io/badge/license-MIT-blue)

## 安装

### 使用 curl (推荐)

```bash
curl -fsSL https://opencode.ai/install | bash
```

### 使用 Homebrew (macOS/Linux)

```bash
brew install opencode
```

### 使用 npm

```bash
npm install -g opencode
```

### 使用 pip

```bash
pip install opencode
```

## 主要功能

### 1. LSP 支持

- 自动为 LLM 加载正确的 LSP
- 提供代码智能提示和语法检查

### 2. 多会话支持

- 在同一项目中并行启动多个代理
- 提高开发效率

### 3. 共享链接

- 分享任何会话用于参考或调试

### 4. GitHub Copilot

- 登录 GitHub 使用你的 Copilot 账户

### 5. ChatGPT Plus/Pro

- 登录 OpenAI 使用 Plus 或 Pro 账户

### 6. 任意模型

- 通过 Models.dev 支持 75+ LLM 提供商
- 包括本地模型

### 7. 任意编辑器

- 终端界面
- Desktop 应用
- IDE 扩展

## 快速开始

### 基本命令

```bash
# 运行 OpenCode
opencode

# 运行特定任务
opencode "帮我写一个 Python 爬虫"

# 运行自定义指令
opencode --agent "general" "创建 REST API"
```

### 环境变量

```bash
# 设置 AI 模型
export OPCODE_API_KEY=your_key
export OPCODE_MODEL=your_preferred_model

# 使用 GitHub Copilot
export GITHUB_TOKEN=your_github_token

# 调试模式
export OPCODE_DEBUG=true
```

## 配置

### opencode.json 配置

```json
{
  "model": "gpt-4",
  "apiKey": "your_api_key",
  "agents": {
    "general": {
      "description": "通用代理",
      "tools": ["bash", "edit", "read", "glob", "grep", "write", "task"]
    },
    "explorer": {
      "description": "代码探索代理",
      "tools": ["task"]
    }
  },
  "permissions": {
    "shell": true,
    "read": true,
    "write": true,
    "typecheck": false
  }
}
```

### 权限配置

```json
{
  "permissions": {
    "shell": {
      "enabled": true,
      "timeout": 120000,
      "workdir": "."
    },
    "file": {
      "read": true,
      "write": true,
      "create": true,
      "edit": true,
      "delete": false
    }
  }
}
```

## CLI 命令

### Bash 工具

```bash
# 执行命令
opencode --tool=bash "ls -la"

# 设置超时
opencode --tool=bash --timeout=30000 "npm install"
```

### 文件操作工具

```bash
# 读取文件
opencode --tool=read --filePath="src/main.py"

# 写入文件
opencode --tool=write --content="print('hello')" --filePath="test.py"

# 编辑文件（替换文本）
opencode --tool=edit --filePath="src.py" --oldString="old" --newString="new"
```

### 搜索工具

```bash
# Glob 搜索
opencode --tool=glob --pattern="**/*.py"

# Grep 搜索
opencode --tool=grep --pattern="function" --include="*.py"
```

### Web 工具

```bash
# 网页获取
opencode --tool=webfetch --url="https://api.github.com"
```

## Skills 系统

### 加载 Skills

```bash
# 加载特定技能
opencode --skill=customize-opencode "配置代理设置"

# 可用 skills
- customize-opencode: 配置 OpenCode 自身 (opencode.json 等)
- explore: 代码探索
- general: 通用任务
- task: 多步骤任务
- question: 用户提问
- webfetch: 网页获取
- edit: 文件编辑
- write: 文件写入
- read: 文件读取
- glob: 文件搜索
- grep: 内容搜索
```

## 多代理系统

### 创建自定义代理

```bash
# 创建配置目录
mkdir -p ~/.config/opencode/agents

# 创建自定义代理
cat > ~/.config/opencode/agents/my-agent.json <<EOF
{
  "name": "my-python-expert",
  "description": "Python 开发专家",
  "skills": ["customize-opencode", "task", "bash", "write"],
  "tools": ["bash", "edit", "read", "glob", "grep", "write"]
}
EOF
```

### 使用不同代理

```bash
# 通用代理
opencode --agent general "帮我重构这段代码"

# 代码探索代理
opencode --agent explorer "查找所有的 bug"

# 自定义代理
opencode --agent "custom-agent-name" "执行我的命令"
```

## 最佳实践

### 1. 使用 Task 工具处理复杂任务

```python
# 任务描述应清晰具体
task = task(
    description="编写单元测试",
    prompt="为 src/calculator.py 创建完整的测试",
    subagent_type="general"
)
```

### 2. 保持 Todo 列表

```python
# 使用 todowrite 管理任务
todowrite(todos=[
    {"content": "创建数据库模型", "status": "pending", "priority": "high"},
    {"content": "编写 API 路由", "status": "in_progress", "priority": "high"},
    {"content": "添加单元测试", "status": "pending", "priority": "medium"}
])
```

### 3. 文件操作模式

```python
# 先搜索再修改
# 1. 使用 glob 或 grep 理解代码结构
pattern = "**/*.{py,js,ts}"
files = glob(pattern)

# 2. 读取现有文件了解上下文
content = read(filePath="src/main.py")

# 3. 使用 edit 进行精确修改
edit(
    filePath="src/main.py",
    oldString="old_code",
    newString="new_code"
)

# 4. 写入新文件
write(
    content="print('hello')",
    filePath="src/new_file.py"
)
```

### 4. Git 操作

```bash
# 检查状态
status = bash(command="git status")

# 检查差异
diff = bash(command="git diff")

# 提交更改
bash(command="git add .")
bash(command="git commit -m '完成新功能'")

# 创建 Pull Request
pr = bash(command="gh pr create --title '新功能' --body '详细描述'")
```

### 5. 测试验证

```bash
# 运行 lint
bash(command="npm run lint")

# 运行类型检查
bash(command="npm run typecheck")

# 运行测试
bash(command="npm test")
```

## 安全性

### 数据隐私

- OpenCode 不会存储任何代码或上下文数据
- 可在安全敏感环境使用
- 所有数据在本地处理

### Shell 安全

```json
{
  "permissions": {
    "shell": {
      "enabled": true,
      "safeCommands": ["npm install", "git add", "git commit"],
      "dangerousCommands": ["rm -rf", "format", "dd"]
    }
  }
}
```

## 故障排除

### 常见问题

#### Q: 代理无法连接到模型

```bash
# 检查 API 密钥
export OPCODE_API_KEY=your_key

# 检查网络
curl https://api.anthropic.com/v1/models
```

#### Q: 工具调用失败

```bash
# 检查配置文件
cat ~/.config/opencode/opencode.json

# 查看日志
tail -f ~/.config/opencode/logs/*.log
```

#### Q: 任务超时

```bash
# 增加超时时间
opencode --command "npm install" --timeout=300000
```

## 参考文档

- [官方文档](https://opencode.ai/docs)
- [GitHub 仓库](https://github.com/anomalyco/opencode)
- [Discord 社区](https://discord.gg/opencode)
- [Changelog](https://opencode.ai/changelog)

## API 参考

### webfetch

```javascript
// 基本用法
fetch(url)

// 指定格式
fetch(url, { format: "markdown | text | html" })

// 设置超时
fetch(url, { timeout: 60000 })
```

### write

```javascript
// 写入文件
write({
  content: string,
  filePath: string
})

// 追加内容
write({
  content: string,
  filePath: string,
  append: true
})
```

### edit

```javascript
// 编辑文件 (单处)
edit({
  filePath: string,
  oldString: string,
  newString: string
})

// 编辑多处
edit({
  filePath: string,
  oldString: string,
  newString: string,
  replaceAll: true
})
```

### read

```javascript
// 读取文件
read({
  filePath: string,
  offset?: number,
  limit?: number
})

// 读取目录
read({
  filePath: string,        // 目录路径
})
```

### glob

```javascript
// 模式匹配
glob({
  pattern: "**/*.py",
  path?: string
})
```

### grep

```javascript
// 内容搜索
grep({
  pattern: "regex.*pattern",
  path?: string,
  include?: "*.py"
})
```

### task

```javascript
// 创建任务
task({
  description: string,     // 短描述 (3-5 词)
  prompt: string,          // 任务详情
  subagent_type: string,   // 代理类型
  task_id?: string         // 任务 ID (续传)
})
```

### question

```javascript
// 用户提问
question({
  questions: [
    {
      question: string,
      header: string,
      options: [
        { label: string, description: string }
      ],
      multiple?: boolean
    }
  ]
})
```

## 性能优化

### 1. 批量读取文件

```python
# 并发读取文件
tasks = [
    read(filePath=f) 
    for f in file_list[:batch_size]
]
```

### 2. 使用 task 自动管理

```python
# 复杂任务自动管理上下文
task({
    description: "优化性能",
    prompt: "分析代码并优化",
    subagent_type: "general"
})
```

### 3. 缓存搜索结果

```python
# 缓存 glob 结果
cache_path = ".opencode-cache"
if not exists(cache_path):
    files = glob(pattern="**/*.py")
    save(cache_path, files)
else:
    files = load(cache_path)
```

## 高级用法

### 自定义代理定义

```json
{
  "name": "fullstack-dev",
  "description": "全栈开发专家",
  "skills": [
    "customize-opencode",
    "explore",
    "general", 
    "task",
    "question",
    "shell",
    "file-ops"
  ],
  "tools": ["bash", "glob", "grep", "read", "edit", "write", "write"],
  "preferences": {
    "defaultAgent": "general",
    "maxTools": 5
  }
}
```

### 扩展工具支持

```python
# 通过 MCP 服务器扩展
task({
    prompt: "使用 MCP 服务器查询数据库",
    subagent_type: "general",
    mcpServers: {
        "postgres": {
            "command": "docker",
            "args": ["run", "-i", "-e", "POSTGRES_PASSWORD=pass", "-p", "5432:5432", "postgres:alpine"],
            "env": {"POSTGRES_PASSWORD": "pass"}
        }
    }
})
```

### 工作流自动化

```python
# 定义工作流
workflow = [
    task(description="分析需求", prompt="..."),
    task(description="设计架构", prompt="..."),
    task(description="实现代码", prompt="..."),
    task(description="编写测试", prompt="..."),
    task(description="文档", prompt="...")
]

# 执行工作流
for step in workflow:
    run(step)
    if not step.succeeded:
        retry(step)
```

## 贡献指南

1. Fork 仓库
2. 创建特性分支
3. 提交 PR

```bash
git checkout -b feature/amazing-feature
git commit -m "add amazing feature"
git push origin feature/amazing-feature
```

## 许可证

MIT License

Copyright © 2024 Anomaly

---

**提示**: 实际使用时请参考官方文档获取最新信息。
