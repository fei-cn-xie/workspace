# 60、强化学习之Q-Learning

## 什么是强化学习

强化学习（Reinforcement Learning）是机器学习中的一种方法，它通过与环境进行交互，学习如何利用其当前状态和行为来获得最大的奖励。

前面课程中讲的深度学习，它学习的是对错，比如图片中的数字是多少，是有标准答案的，而强化学习学习的是好坏，比如找到宝藏的路径没有对错，只有好坏，比如大模型输出的答案也没有对错，只有好坏。

## 什么是环境、状态、动作、奖励

- 环境（Environment）：比如下围棋，棋盘就是环境，比如自动驾驶，车以及车周围的物体就构成了环境。
- 状态（State）：比如棋盘中的棋子不同的摆放就对应了环境不同的状态，比如汽车行驶在不同的路口就对应了环境不同的状态
- 动作（Action）：上下左右移动、跳跃等等就是动作
- 奖励（Reward）：比如下棋赢了就会获得奖励，比如找到宝藏，就会获得奖励，比如汽车撞到了障碍物就会获得惩罚（负奖励）

## 什么是智能体

强化学习中的智能体指的是汽车、机器人、人等等，和我们现在流行讲的AI Agent有一点区别。

![default.png](images/Xy0WbguY9oEAAYxuFqDc21rYnub.png)

## 什么是Q-Learning

Q-Learning的核心就是学到一张Q表

## 什么是Q表

Q表是一个二维表，行表示不同的状态，列表示不同的动作，Q表中的每一个元素表示当前状态下执行当前动作的奖励，在训练过程中会不断更新Q表，从而使得智能体能够按照Q表来选择动作，从而获得奖励。

## 什么是当前奖励、未来奖励

当前奖励：当前状态执行当前动作立马得到的奖励
未来奖励：当前状态执行当前动作得到奖励后，还会得到一个新状态，新状态执行不同动作也可能会得到奖励，而这个奖励就是未来奖励，一般会乘以一个衰减因子，比如0.9

## Q-Learning的缺点是什么

Q-Learning存在维度灾难，状态很多、动作很多，Q 表就会非常大，这时就需要用到深度学习，也就出现了深度强化学习，后面讲到的DQN、A2C、PPO、GRPO都是深度强化学习

```python
# 一个简化的迷宫，N_STATES表示有6个位置
N_STATES = 6
env = ['-'] * (N_STATES - 1) + ['T']
env[0] = 'o'
interaction = ''.join(env)
print(interaction)
```

```plaintext
o----T
```

```python
# 只有两个动作，要么左移一步，要么右移一步
ACTIONS = ['left', 'right']
```

```python
# 和环境交互，得到环境的反馈
def get_env_feedback(current_state, action):
    if action == 'right':  # 向右走
        if current_state == N_STATES - 2:  # N_STATES - 2=4，已经在宝藏左边一个位置，下一步就到宝藏了
            next_s = 'terminal'
            reward = 1
        else:
            next_s = current_state + 1
            reward = 0
    else:  # 向左走
        reward = 0
        if current_state == 0:
            next_s = current_state  # 撞墙了，原地不动
        else:
            next_s = current_state - 1
    return next_s, reward
```

```python
get_env_feedback(0, 'right')
```

```plaintext
(1, 0)
```

```python
get_env_feedback(4, 'right')
```

```plaintext
('terminal', 1)
```

```python
# 根据当前状态，绘制出当前环境（游戏画面）
def print_env(current_state):
    env = ['-'] * (N_STATES - 1) + ['T']  # '---------T' 形象化环境
    env[current_state] = 'o'  # 用 'o' 代表探险家
    interaction = ''.join(env)
    print(interaction)
```

```python
print_env(2)
```

```plaintext
--o--T
```

```python
# 定义Q表，行为状态，列为动作，表示当前状态下的所有动作对应的奖励（Q值）

import pandas as pd
import numpy as np

q_table = pd.DataFrame(np.zeros((N_STATES, len(ACTIONS))), columns=ACTIONS)
q_table
```

|   | left | right |
| --- | --- | --- |
| 0 | 0.0 | 0.0 |
| 1 | 0.0 | 0.0 |
| 2 | 0.0 | 0.0 |
| 3 | 0.0 | 0.0 |
| 4 | 0.0 | 0.0 |
| 5 | 0.0 | 0.0 |

```python
EPSILON = 0.9  # 贪婪度：90%的时间选最优动作，10%随机探索

def choose_action(current_state):
    # 获取当前状态下的所有动作的Q值
    state_actions = q_table.iloc[current_state, :]

    # 如果所有动作都为0，则随机选择一个动作
    # 或者随机数大于贪婪度，则随机选择一个动作
    # np.random.uniform()会生成一个0-1之间的随机数
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):
        action = np.random.choice(ACTIONS)
    else:
        # 否则选择当前状态下Q值最大的动作
        action = state_actions.idxmax()
    return action
```

```python
# 开始训练

# 初始化Q表
q_table = pd.DataFrame(np.zeros((N_STATES, len(ACTIONS))), columns=ACTIONS)

# episode(尝试) epoch(回合)
for episode in range(1):
    current_state = 0

    # 步骤
    while current_state != 'terminal':

        # 当前状态下选择一个动作
        action = choose_action(current_state)

        # 和环境进行交互，获取下一个状态和奖励
        next_state, reward = get_env_feedback(current_state, action)

        # 打印游戏画面
        print_env(current_state)

        # 如果下一个状态是宝藏，则更新Q表，并退出while
        if next_state == 'terminal':
            q_table.loc[current_state, action] += reward
            break

        # 否则继续玩，直到拿到宝藏
        current_state = next_state
```

```plaintext
o----T
-o---T
o----T
o----T
-o---T
--o--T
---o-T
--o--T
-o---T
--o--T
---o-T
----oT
---o-T
--o--T
-o---T
--o--T
-o---T
o----T
-o---T
--o--T
-o---T
--o--T
---o-T
----oT
```

```python
q_table
```

|   | left | right |
| --- | --- | --- |
| 0 | 0.0 | 0.0 |
| 1 | 0.0 | 0.0 |
| 2 | 0.0 | 0.0 |
| 3 | 0.0 | 0.0 |
| 4 | 0.0 | 1.0 |
| 5 | 0.0 | 0.0 |

```python
# 初始化Q表
q_table = pd.DataFrame(np.zeros((N_STATES, len(ACTIONS))), columns=ACTIONS)
```

```python
# 开始训练
GAMMA = 0.9 # 未来奖励衰减因子

for episode in range(10):
    current_state = 0

    while current_state != 'terminal':
        action = choose_action(current_state)
        next_state, reward = get_env_feedback(current_state, action)
        # print_env(current_state)

        # 最后一步只有当前奖励，没有未来奖励
        if next_state == 'terminal':
            # 拿到了奖励要更新Q表
            q_target = reward
        else:
            # 其他步骤，有当前奖励和未来奖励，也就是下一个状态对应的所有步骤中所能得到的最大奖励
            future_reward = GAMMA * q_table.iloc[next_state, :].max()
            q_target = reward + future_reward

        # 实际奖励-预测奖励就是新获得的奖励
        q_table.loc[current_state, action] = q_target

        if next_state == 'terminal':
             break
        current_state = next_state
```

```python
q_table
```

|   | left | right |
| --- | --- | --- |
| 0 | 0.00000 | 0.6561 |
| 1 | 0.59049 | 0.7290 |
| 2 | 0.00000 | 0.8100 |
| 3 | 0.00000 | 0.9000 |
| 4 | 0.81000 | 1.0000 |
| 5 | 0.00000 | 0.0000 |

```python
# 推理阶段
s = 0
steps = []
while s != 'terminal':
    # 直接选择Q值最大的动作
    a = q_table.iloc[s, :].idxmax()
    steps.append(a)
    s, _ = get_env_feedback(s, a)
print(f"最优路径: {' -> '.join(steps)}")
```

```plaintext
最优路径: right -> right -> right -> right -> right
```