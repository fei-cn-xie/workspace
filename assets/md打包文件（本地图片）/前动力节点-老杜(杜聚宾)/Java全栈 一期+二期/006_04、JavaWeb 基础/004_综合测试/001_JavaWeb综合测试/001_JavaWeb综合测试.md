# JavaWeb综合测试

# 个人任务看板 - 考核题目

## 题目说明

请你实现一个**个人任务看板系统**，使用Servlet、Ajax(Axios)和三层架构。用户可以通过界面管理自己的任务，包括查看、添加、修改状态和删除任务。

## 功能需求

### 1. 任务显示与分类

- 页面分为三列显示不同状态的任务：**待处理**、**进行中**、**已完成**
- 每列顶部显示该状态下的任务数量
- 页面加载时自动从服务器获取所有任务并分类显示

### 2. 添加新任务

- 通过顶部表单输入任务标题
- 点击"添加任务"按钮提交到服务器
- 新任务默认状态为"待处理"
- 添加成功后任务显示在"待处理"列顶部

### 3. 修改任务状态

- 每个任务卡片显示当前状态和修改下拉框
- 通过下拉框可以直接改变任务状态
- 状态改变后任务自动移动到对应列

### 4. 删除任务

- 每个任务卡片有删除按钮
- 点击删除按钮移除对应任务

## 数据库设计

```sql
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    status ENUM('todo', 'doing', 'done') NOT NULL DEFAULT 'todo',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT DEFAULT 0
);
```

## 后端接口规范

### 1. 获取所有任务

- **URL:** `GET /tasks/list`
- **响应:** 返回所有有效任务的JSON数组

### 2. 添加新任务

- **URL:** `POST /tasks/add`
- **参数:** `title` (任务标题)
- **响应:** 返回新创建的任务对象

### 3. 更新任务状态

- **URL:** `POST /tasks/update`
- **参数:** `status` (新状态: todo/doing/done)
- **响应:** 返回更新后的任务对象

### 4. 删除任务

- **URL:** `POST /tasks/delete`
- **响应:** 返回操作结果

## 前端页面代码

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个人任务看板</title>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 30px;
            text-align: center;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .add-task-section {
            padding: 25px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }

        .task-form {
            display: flex;
            gap: 15px;
            max-width: 600px;
            margin: 0 auto;
        }

        #taskInput {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: all 0.3s;
        }

        #taskInput:focus {
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }

        #addTaskBtn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
        }

        #addTaskBtn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }

        .board {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 0;
            min-height: 600px;
        }

        .column {
            padding: 25px;
            position: relative;
        }

        .column::before {
            content: '';
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            width: 1px;
            background: linear-gradient(to bottom, transparent, #e9ecef, transparent);
        }

        .column:last-child::before {
            display: none;
        }

        .todo { background: #fff; }
        .doing { background: #f8f9fa; }
        .done { background: #f1f8e9; }

        .column-header {
            text-align: center;
            margin-bottom: 25px;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1.2em;
            position: relative;
            overflow: hidden;
        }

        .todo .column-header {
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            color: white;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        }

        .doing .column-header {
            background: linear-gradient(135deg, #4ecdc4, #44a08d);
            color: white;
            box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3);
        }

        .done .column-header {
            background: linear-gradient(135deg, #45b7d1, #96c93d);
            color: white;
            box-shadow: 0 5px 15px rgba(69, 183, 209, 0.3);
        }

        .task-list {
            min-height: 450px;
        }

        .task-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            border-left: 4px solid;
            transition: all 0.3s;
            position: relative;
        }

        .task-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }

        .todo .task-card { border-left-color: #ff6b6b; }
        .doing .task-card { border-left-color: #4ecdc4; }
        .done .task-card { border-left-color: #45b7d1; }

        .task-title {
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 10px;
            line-height: 1.4;
        }

        .task-meta {
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 12px;
        }

        .task-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .status-select {
            padding: 6px 12px;
            border: 1px solid #bdc3c7;
            border-radius: 15px;
            background: white;
            font-size: 12px;
            outline: none;
            cursor: pointer;
        }

        .delete-btn {
            background: #e74c3c;
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .delete-btn:hover {
            background: #c0392b;
            transform: scale(1.1);
        }

        .empty-message {
            text-align: center;
            color: #95a5a6;
            font-style: italic;
            padding: 40px 20px;
            background: rgba(255,255,255,0.7);
            border-radius: 10px;
            border: 2px dashed #bdc3c7;
        }

        .stats {
            text-align: center;
            padding: 20px;
            background: #2c3e50;
            color: white;
            font-size: 14px;
        }

        @media (max-width: 768px) {
            .board {
                grid-template-columns: 1fr;
            }
            
            .column::before {
                display: none;
            }
            
            .column {
                border-bottom: 1px solid #e9ecef;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 个人任务看板</h1>
            <div class="subtitle">高效管理您的日常任务</div>
        </header>
        <div class="add-task-section">
            <div class="task-form">
                <input type="text" id="taskInput" placeholder="请输入新任务内容..." maxlength="200">
                <button id="addTaskBtn">+ 添加任务</button>
            </div>
        </div>
        <div class="board">
            <!-- 待处理列 -->
            <div class="column todo">
                <div class="column-header">
                    ⏳ 待处理 (<span id="todoCount">0</span>)
                </div>
                <div class="task-list" id="todoList">
                    <div class="empty-message">暂无待处理任务</div>
                </div>
            </div>
            <!-- 进行中列 -->
            <div class="column doing">
                <div class="column-header">
                    🚀 进行中 (<span id="doingCount">0</span>)
                </div>
                <div class="task-list" id="doingList">
                    <div class="empty-message">暂无进行中任务</div>
                </div>
            </div>
            <!-- 已完成列 -->
            <div class="column done">
                <div class="column-header">
                    ✅ 已完成 (<span id="doneCount">0</span>)
                </div>
                <div class="task-list" id="doneList">
                    <div class="empty-message">暂无已完成任务</div>
                </div>
            </div>
        </div>
        <div class="stats">
            总任务数: <span id="totalCount">0</span> | 
            今日创建: <span id="todayCount">0</span>
        </div>
    </div>
    <script>
        // 任务管理应用
        const TaskManager = {
            // 初始化应用
            init() {
                this.bindEvents();
                this.loadTasks();
            },

            // 绑定事件
            bindEvents() {
                // 添加任务事件
                document.getElementById('addTaskBtn').addEventListener('click', () => {
                    this.addTask();
                });

                // 回车键添加任务
                document.getElementById('taskInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.addTask();
                    }
                });
            },

            // 加载所有任务
            async loadTasks() {
                try {
                    // TODO: 使用Axios从后端获取任务数据
                    console.log('从服务器加载任务数据...');
                    
                    // 模拟数据 - 实际开发中删除
                    const mockTasks = [
                        { id: 1, title: '学习Servlet和JSP', status: 'doing', created_time: '2024-01-15 10:00:00' },
                        { id: 2, title: '完成Ajax练习', status: 'todo', created_time: '2024-01-15 11:00:00' },
                        { id: 3, title: '准备项目演示', status: 'done', created_time: '2024-01-14 09:00:00' }
                    ];
                    
                    this.renderTasks(mockTasks);
                } catch (error) {
                    console.error('加载任务失败:', error);
                    alert('加载任务失败，请刷新页面重试');
                }
            },

            // 添加新任务
            async addTask() {
                const input = document.getElementById('taskInput');
                const title = input.value.trim();

                if (!title) {
                    alert('请输入任务内容');
                    input.focus();
                    return;
                }

                try {
                    // TODO: 使用Axios发送POST请求到后端
                    console.log('添加新任务:', title);
                    
                    // 模拟成功响应 - 实际开发中删除
                    const newTask = {
                        id: Date.now(),
                        title: title,
                        status: 'todo',
                        created_time: new Date().toISOString()
                    };
                    
                    this.addTaskToDOM(newTask);
                    input.value = '';
                    this.updateCounts();
                    
                } catch (error) {
                    console.error('添加任务失败:', error);
                    alert('添加任务失败，请重试');
                }
            },

            // 更新任务状态
            async updateTaskStatus(taskId, newStatus) {
                try {
                    // TODO: 使用Axios发送PUT请求到后端
                    console.log(`更新任务 ${taskId} 状态为: ${newStatus}`);
                    
                    // 在实际开发中，这里应该等待后端响应成功后再更新DOM
                    this.moveTaskToColumn(taskId, newStatus);
                    this.updateCounts();
                    
                } catch (error) {
                    console.error('更新任务状态失败:', error);
                    alert('更新失败，请重试');
                }
            },

            // 删除任务
            async deleteTask(taskId) {
                if (!confirm('确定要删除这个任务吗？')) {
                    return;
                }

                try {
                    // TODO: 使用Axios发送DELETE请求到后端
                    console.log('删除任务:', taskId);
                    
                    // 在实际开发中，这里应该等待后端响应成功后再删除DOM
                    this.removeTaskFromDOM(taskId);
                    this.updateCounts();
                    
                } catch (error) {
                    console.error('删除任务失败:', error);
                    alert('删除失败，请重试');
                }
            },

            // 渲染任务列表
            renderTasks(tasks) {
                // 清空所有列表
                document.getElementById('todoList').innerHTML = '';
                document.getElementById('doingList').innerHTML = '';
                document.getElementById('doneList').innerHTML = '';


                // 添加任务到对应列
                tasks.forEach(task => {
                    this.addTaskToDOM(task);
                });

                this.updateCounts();
            },

            // 添加任务到DOM
            addTaskToDOM(task) {
                const taskElement = this.createTaskElement(task);
                const targetList = document.getElementById(`${task.status}List`);
                
                // 移除空状态提示
                const emptyMsg = targetList.querySelector('.empty-message');
                if (emptyMsg) {
                    emptyMsg.remove();
                }
                
                targetList.appendChild(taskElement);
            },

            // 创建任务元素
            createTaskElement(task) {
                const taskDiv = document.createElement('div');
                taskDiv.className = 'task-card';
                taskDiv.dataset.taskId = task.id;

                const statusText = {
                    'todo': '待处理',
                    'doing': '进行中', 
                    'done': '已完成'
                };

                taskDiv.innerHTML = `
                    <div class="task-title">${this.escapeHtml(task.title)}</div>
                    <div class="task-meta">
                        创建时间: ${new Date(task.created_time).toLocaleString()}
                    </div>
                    <div class="task-actions">
                        <select class="status-select" onchange="TaskManager.updateTaskStatus(${task.id}, this.value)">
                            <option value="todo" ${task.status === 'todo' ? 'selected' : ''}>待处理</option>
                            <option value="doing" ${task.status === 'doing' ? 'selected' : ''}>进行中</option>
                            <option value="done" ${task.status === 'done' ? 'selected' : ''}>已完成</option>
                        </select>
                        <button class="delete-btn" onclick="TaskManager.deleteTask(${task.id})">×</button>
                    </div>
                `;

                return taskDiv;
            },

            // 移动任务到其他列
            moveTaskToColumn(taskId, newStatus) {
                const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
                if (!taskElement) return;

                // 更新选择框状态
                const select = taskElement.querySelector('.status-select');
                select.value = newStatus;

                // 移动到新列
                const newList = document.getElementById(`${newStatus}List`);
                const emptyMsg = newList.querySelector('.empty-message');
                if (emptyMsg) {
                    emptyMsg.remove();
                }
                newList.appendChild(taskElement);
            },

            // 从DOM中移除任务
            removeTaskFromDOM(taskId) {
                const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
                if (taskElement) {
                    taskElement.remove();
                    
                    // 检查列是否为空，如果为空显示提示信息
                    const columns = ['todo', 'doing', 'done'];
                    columns.forEach(status => {
                        const list = document.getElementById(`${status}List`);
                        if (list.children.length === 0) {
                            list.innerHTML = '<div class="empty-message">暂无任务</div>';
                        }
                    });
                }
            },

            // 更新任务计数
            updateCounts() {
                const todoCount = document.getElementById('todoList').querySelectorAll('.task-card').length;
                const doingCount = document.getElementById('doingList').querySelectorAll('.task-card').length;
                const doneCount = document.getElementById('doneList').querySelectorAll('.task-card').length;
                
                document.getElementById('todoCount').textContent = todoCount;
                document.getElementById('doingCount').textContent = doingCount;
                document.getElementById('doneCount').textContent = doneCount;
                document.getElementById('totalCount').textContent = todoCount + doingCount + doneCount;
                
                // 简单统计今日任务（模拟）
                document.getElementById('todayCount').textContent = Math.floor(Math.random() * 5);
            },

            // HTML转义防止XSS
            escapeHtml(unsafe) {
                return unsafe
                    .replace(/&/g, "&")
                    .replace(/</g, "<")
                    .replace(/>/g, ">")
                    .replace(/"/g, """)
                    .replace(/'/g, "'");
            }
        };

        // 页面加载完成后初始化应用
        document.addEventListener('DOMContentLoaded', function() {
            TaskManager.init();
        });
    </script>
</body>
</html>
```

## 技术要求

1. **必须使用三层架构**
  - Web层：Servlet处理HTTP请求
  - Service层：业务逻辑处理
  - DAO层：数据库操作
2. **前端技术要求**
  - 使用Axios进行所有Ajax请求
  - 实现无刷新操作（SPA体验）
  - 友好的用户交互和错误处理
3. **后端技术要求**
  - 使用JDBC连接数据库
  - 使用连接池管理数据库连接
  - 统一的JSON响应格式

## 评分标准（100分）

### 功能实现（60分）

- 任务显示和分类（15分）
- 添加任务功能（10分）
- 状态修改功能（15分）
- 删除任务功能（10分）
- 任务计数更新（10分）

### 技术规范（40分）

- 三层架构运用（15分）
- Ajax/Axios使用（10分）
- 代码质量与结构（10分）
- 数据库操作规范（5分）