# Claude Code 操作指南

## 简介

这是一个关于 [Claude Code](https://claude.ai/code) CLI 工具、桌面应用和相关功能的详细操作文档。

---

## 📋 目录

1. [什么是 Claude Code](#什么是 claude-code)
2. [常用命令速查](#常用命令速查)
3. [文件操作](#文件操作)
4. [代码搜索与探索](#代码搜索与探索)
5. [执行命令](#执行命令)
6. [Agent 任务](#agent 任务)
7. [任务和计划模式](#任务和计划模式)
8. [定时任务](#定时任务)
9. [AI 技能](#ai 技能)
10. [记忆管理](#记忆管理)
11. [快捷键](#快捷键)
12. [权限管理](#权限管理)

---

## 什么是 Claude Code

Claude Code 是 Anthropic 官方推出的智能编程助手工具集合，包括：

- **CLI 命令行工具**: 在终端中交互使用
- **桌面应用**: Mac/Windows/Mobile 桌面客户端
- **Web 应用**: claud.ai/code 访问
- **IDE 扩展**: VS Code 和 JetBrains 插件扩展

---

## 常用命令速查

| 命令 | 功能 |
|------|------|
| `\simplify` | 重构和简化代码 |
| `/commit` | 提交代码到 Git |
| `/review-pr` | 审查 PR |
| `/v<skill-name>` | 使用 AI 技能（如`/vupdate-config`） |
| `/help` | 获取帮助 |
| `/clear` | 清空对话历史 |

---

## 文件操作

### Read
读取文件内容，支持：
- 完整读取（默认）
- 指定范围（`offset` 和 `limit` 参数）
- 查看 PDF 和 Jupyter Notebook

**示例：**
```
Read(file_path="D:\Users\fei\workspace\README.md")
```

### Glob
通过通配符搜索文件，格式：`**/*.js`

**示例：**
```
Glob(pattern="**/*.py", path="D:\Users\fei\workspace")
```

### Grep
使用 ripgrep 进行代码内容搜索

**示例：**
```
Grep(pattern="function.*init", path="D:\Users\fei\workspace", glob="*.py")
```

### Write
创建或覆盖文件内容

**示例：**
```
Write(file_path="D:\Users\fei\workspace\new.txt", content="Hello")
```

### Edit
编辑文件，需要先用 Read 工具打开文件
- 支持行级精确替换
- 可替换所有匹配项（`replace_all` 参数）

**示例：**
```
Edit(file_path="...", old_string="old", new_string="new")
```

---

## 代码搜索与探索

### Bash
执行终端命令

**重要提示：**
- 优先使用专用工具（Read/Glob/Grep）代替 bash 命令
- 使用 Bash 的场景：系统命令、npm install、git 操作、编译构建等

### Agent
创建子代理执行复杂任务

**可配置的代理类型：**

| 类型 | 用途 |
|------|------|
| `general-purpose` | 通用代理，复杂多步任务 |
| `Explore` | 快速探索代码库，文件搜索，关键词查找 |
| `Plan` | 软件架构设计，返回实施计划 |
| `claude-code-guide` | 解答关于 Claude Code 的问题 |

**示例：**
```
Agent(description="知识库代码审查", 
      prompt="审查迁移脚本 0042_user_schema.sql 的安全性...")
```

---

## 执行命令

### 基础用法
```
Bash(command="npm install", timeout=120000)
```

### 高级选项

| 参数 | 说明 |
|------|------|
| `timeout` | 最大执行时间（毫秒，默认 120000） |
| `description` | 命令的简短描述，便于用户跟踪 |
| `run_in_background` | 后台运行，完成时通知 |

**示例：**
```
Bash(command="git commit -m 'Add feature'", 
     description="提交新功能到 Git")
```

### Git 操作
- 优先使用新提交而非 amend
- 禁止破坏性操作（除非用户明确要求）
- 自动处理 pre-commit hook

**示例：**
```
Bash(command="git add .")
Bash(command="git commit -m \"feat: add new feature\"")
Bash(command="git push origin main")
```

---

## Agent 任务

### 创建任务

**TaskCreate:** 创建结构化任务列表
```
TaskCreate(subject="修复认证 bug", description="修复登录流程中的认证问题")
```

**参数：**
- `subject`: 简明任务标题（祈使句）
- `description`: 详细需求描述
- `activeForm`: 进行中形式的描述（可选）
- `metadata`: 元数据（可选）

### 获取和更新任务

**TaskGet:** 通过任务 ID 获取任务详情
**TaskList:** 列出所有待处理任务
**TaskUpdate:** 更新任务状态
- 完成任务后标记为 `completed`
- 支持设置依赖关系（blocks/blockedBy）

### TaskStop
停止后台运行的任务

---

## 任务和计划模式

### EnterPlanMode
在开始实现非平凡任务时进入计划模式
- 用于探索代码库和设计实施方案
- 需获得用户批准才能继续实施
- 避免用户请求中的歧义或浪费的工作

### ExitPlanMode
完成计划后退出
- 将计划写入文件
- 请求用户批准

### Plan: 软件架构代理
- 实施规划
- 识别关键文件
- 考虑架构权衡

---

## 定时任务

### CronCreate
定时触发任务

**参数：**

| 参数 | 说明 |
|------|------|
| `cron` | 标准 5 字段 crontab 表达式 |
| `prompt` | 触发时执行的提示 |
| `recurring` | 是否重复（默认 true，true 则 7 天后自动过期） |
| `durable` | 是否持久化（默认 false，仅当前会话） |

**示例：**
```
CronCreate(cron="30 9 * * *", 
            prompt="每周检查部署", 
            recurring=true)
```

### CronDelete
删除已计划的定时任务

### CronList
列出所有定时任务

---

## AI 技能

### Skill: 技能工具
执行预定义的技能命令

**可用技能：**
- `update-config`: 配置 Claude Code 工具
- `keybindings-help`: 重新绑定快捷键
- `simplify`: 简化代码
- `loop`: 设置定时任务
- `claude-api`: 构建 Claude API 应用

**示例：**
```
Skill(skill="update-config", args="--help")
```

---

## 记忆管理

### MEMORY.md
系统文件，存放各种类型的记忆

### Memory: 记忆类型

| 类型 | 说明 | 保存时机 |
|------|------|----------|
| `user` | 用户角色、目标、偏好 | 了解新信息时保存 |
| `feedback` | 用户反馈和偏好 | 用户纠正或确认时保存 |
| `project` | 进行中工作、目标、任务 | 了解上下文时保存 |
| `reference` | 外部系统资源的指针 | 了解新资源时保存 |

### 如何保存记忆
1. 使用 `Write` 工具创建记忆文件
2. 使用标准 frontmatter 格式：
   ```markdown
   ---
   name: 记忆名称
   description: 一句话描述
   type: 用户/反馈/项目/参考
   ---
   
   记忆内容
   ```

### 如何删除记忆
- 使用 Edit 工具将记忆文件内容替换为空

---

## 快捷键

### keybindings-help
重新绑定快捷键

常用绑定：
- `Ctrl+S` - 提交回答
- 其他默认绑定

---

## 权限管理

### permissions.json
配置权限设置

### update-config
通过 `Skill` 工具或 `settings.json` 配置权限

**示例设置：**
```json
{
  "permissions": {
    "editFiles": true,
    "readFiles": true,
    "runShell": true,
    "writeFiles": true
  }
}
```

---

## 最佳实践

1. **使用专用工具**: 优先使用 Read/Glob/Grep 而不是 Bash 命令
2. **先理解后修改**: 修改文件前先使用 Read 了解内容
3. **任务列表**: 复杂任务创建任务列表跟踪进度
4. **记忆系统**: 及时保存用户偏好和项目上下文
5. **Git 安全**: 避免使用破坏性命令，正确处理 hooks
6. **后台任务**: 长时间运行任务使用 `run_in_background=true`
7. **权限最小化**: 只请求完成任务所需的权限

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 命令超时 | 增加 `timeout` 参数或后台运行 |
| 权限被拒绝 | 检查 `permissions.json`,更新设置 |
| Hook 失败 | 检查 pre-commit hooks,修复问题 |
| 记忆丢失 | 确认 `durable=true` (如需持久化) |

---

希望这份指南能帮助你更好地使用 Claude Code！
